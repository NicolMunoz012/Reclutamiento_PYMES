"""
Candidato routes - Candidate endpoints
"""
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from typing import List
from models.candidato import (
    CandidatoAplicar,
    AplicacionConPreguntas,
    ResponderPreguntas,
    AplicacionCompleta,
    PreguntaVacante
)
from database import get_db
from services.pdf_service import pdf_service
from services.ia_service import ia_service
from services.storage_service import storage_service
from services.email_service import email_service
from services.chatbot_service import chatbot_service
import uuid
from datetime import datetime

router = APIRouter(prefix="/api/candidato", tags=["Candidatos"])


@router.post("/aplicar", response_model=AplicacionConPreguntas)
async def aplicar_vacante(
    vacante_id: str = Form(...),
    nombre_anonimo: str = Form(...),
    email: str = Form(...),
    telefono: str = Form(...),
    ciudad: str = Form(...),
    años_experiencia: int = Form(...),
    cv_pdf: UploadFile = File(...)
):
    """
    Apply to a job posting
    
    1. Upload CV PDF to storage
    2. Extract text from PDF
    3. Analyze CV with AI
    4. Create candidate and application records
    5. Return questions for candidate to answer
    """
    try:
        db = get_db()
        
        # Verify job posting exists and is published
        vacante = db.table("vacantes").select("*").eq("id", vacante_id).eq("estado", "publicada").execute()
        if not vacante.data:
            raise HTTPException(status_code=404, detail="Vacante no encontrada o no publicada")
        
        vacante_data = vacante.data[0]
        
        # Read PDF file
        pdf_bytes = await cv_pdf.read()
        
        # Extract text from PDF
        cv_text = await pdf_service.extract_text_from_pdf(pdf_bytes)
        
        # Analyze CV with AI
        cv_analisis = await ia_service.analizar_cv(cv_text)
        
        # Create user record
        usuario_id = str(uuid.uuid4())
        usuario_record = {
            "id": usuario_id,
            "email": email,
            "tipo_usuario": "candidato",
            "nombre_completo": nombre_anonimo,
            "telefono": telefono
            # created_at y updated_at se generan automáticamente
        }
        
        db.table("usuarios").insert(usuario_record).execute()
        
        # Create candidate record
        # IMPORTANTE: candidato_id es BIGINT autoincremental, NO se genera manualmente
        candidato_record = {
            "usuario_id": usuario_id,
            "nombre_anonimo": nombre_anonimo,
            "email": email,  # ✅ SÍ existe en candidatos
            "telefono": telefono,  # ✅ SÍ existe en candidatos
            "años_experiencia": años_experiencia,  # ✅ Con tilde
            "resumen_profesional": cv_analisis.get("resumen", "")  # ✅ SÍ existe
            # id se genera automáticamente (BIGINT autoincremental)
            # created_at se genera automáticamente
        }
        
        result = db.table("candidatos").insert(candidato_record).execute()
        candidato_id = result.data[0]["id"]  # Obtener el ID generado (BIGINT)
        
        # Upload CV to storage
        cv_url = await storage_service.upload_cv(
            file_bytes=pdf_bytes,
            candidato_id=candidato_id,
            filename=cv_pdf.filename
        )
        
        # Save document record
        documento_id = str(uuid.uuid4())
        file_size_kb = len(pdf_bytes) // 1024  # Convert bytes to KB
        
        documento_record = {
            "id": documento_id,
            "candidato_id": candidato_id,  # BIGINT (no TEXT)
            "tipo_documento": "cv",
            "nombre_archivo": cv_pdf.filename,
            "url_archivo": cv_url,
            "tamaño_kb": file_size_kb,
            "mime_type": cv_pdf.content_type or "application/pdf",
            "texto_extraido": cv_text[:5000]  # Store first 5000 chars
            # created_at se genera automáticamente con DEFAULT now()
        }
        
        db.table("documentos").insert(documento_record).execute()
        
        # Create application record
        aplicacion_id = str(uuid.uuid4())
        aplicacion_record = {
            "id": aplicacion_id,
            "vacante_id": vacante_id,
            "candidato_id": candidato_id,  # BIGINT (no TEXT, no UUID)
            "estado": "aplicado"
            # fecha_aplicacion, fecha_ultima_actualizacion y updated_at
            # se generan automáticamente con DEFAULT now()
        }
        
        db.table("aplicaciones").insert(aplicacion_record).execute()
        
        # Get approved questions for this job posting
        preguntas = db.table("vacante_preguntas").select("*").eq(
            "vacante_id", vacante_id
        ).eq("aprobada_por_empresa", True).execute()
        
        preguntas_lista = [
            PreguntaVacante(
                pregunta_id=p["id"],
                pregunta=p["pregunta"],
                tipo_pregunta=p["tipo_pregunta"]
            )
            for p in preguntas.data
        ]
        
        return AplicacionConPreguntas(
            candidato_id=candidato_id,
            aplicacion_id=aplicacion_id,
            preguntas=preguntas_lista
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error aplicando a vacante: {str(e)}")


@router.post("/responder", response_model=AplicacionCompleta)
async def responder_preguntas(respuestas_data: ResponderPreguntas):
    """
    Submit answers to job posting questions
    
    1. Save all answers to database
    2. Evaluate candidate compatibility with AI
    3. Update application with scores
    4. Send confirmation email
    """
    try:
        db = get_db()
        
        # Get application details
        aplicacion = db.table("aplicaciones").select("*").eq("id", respuestas_data.aplicacion_id).execute()
        if not aplicacion.data:
            raise HTTPException(status_code=404, detail="Aplicación no encontrada")
        
        aplicacion_data = aplicacion.data[0]
        candidato_id = aplicacion_data["candidato_id"]
        vacante_id = aplicacion_data["vacante_id"]
        
        # Get candidate info
        candidato = db.table("candidatos").select("*").eq("id", candidato_id).execute()
        candidato_data = candidato.data[0]
        
        # Email está en la tabla candidatos (no necesitamos buscar en usuarios)
        candidato_email = candidato_data.get("email", "")
        
        # Get job posting info
        vacante = db.table("vacantes").select("*").eq("id", vacante_id).execute()
        vacante_data = vacante.data[0]
        
        # Get CV text
        documento = db.table("documentos").select("texto_extraido").eq(
            "candidato_id", candidato_id
        ).eq("tipo_documento", "cv").execute()
        cv_text = documento.data[0]["texto_extraido"] if documento.data else ""
        
        # Save each answer
        respuestas_completas = []
        for respuesta in respuestas_data.respuestas:
            respuesta_id = str(uuid.uuid4())
            
            # Get question text
            pregunta = db.table("vacante_preguntas").select("pregunta").eq("id", respuesta.pregunta_id).execute()
            pregunta_texto = pregunta.data[0]["pregunta"] if pregunta.data else ""
            
            # NOTA: No existe tabla respuestas_candidato
            # Las respuestas se guardan en la evaluación final
            # Por ahora solo las acumulamos para la evaluación de IA
            
            # respuesta_record = {
            #     "id": respuesta_id,
            #     "aplicacion_id": respuestas_data.aplicacion_id,
            #     "pregunta_id": respuesta.pregunta_id,
            #     "respuesta": respuesta.respuesta
            # }
            # 
            # db.table("respuestas_candidato").insert(respuesta_record).execute()
            
            # Las respuestas se procesan pero no se guardan individualmente
            # Se guardarán en la tabla evaluaciones después de la evaluación de IA
            
            respuestas_completas.append({
                "pregunta": pregunta_texto,
                "respuesta": respuesta.respuesta
            })
        
        # Evaluate compatibility with AI
        evaluacion = await ia_service.evaluar_compatibilidad(
            cv_text=cv_text,
            respuestas=respuestas_completas,
            titulo=vacante_data["titulo"],
            habilidades_requeridas=vacante_data["habilidades_requeridas"],
            experiencia_min=vacante_data["experiencia_min"]
        )
        
        # Update application with scores
        db.table("aplicaciones").update({
            "puntuacion_ia": evaluacion["puntuacion"],
            "compatibilidad_porcentaje": evaluacion["compatibilidad"],
            "estado": "en_revision"
        }).eq("id", respuestas_data.aplicacion_id).execute()
        
        # Save evaluation to evaluaciones table
        evaluacion_record = {
            "entrevista_id": None,  # Puede vincularse después si hay entrevista
            "puntaje_general": evaluacion["puntuacion"],
            "fortalezas": evaluacion.get("fortalezas", []),
            "debilidades": evaluacion.get("debilidades", []),
            "evaluador_nombre": "IA - Groq LLaMA 3.1",
            "aspectos_positivos": evaluacion.get("fortalezas", []),
            "aspectos_negativos": evaluacion.get("debilidades", []),
            "decision_final": "Pendiente de revisión"
            # created_at se genera automáticamente
        }
        
        db.table("evaluaciones").insert(evaluacion_record).execute()
        
        # Get company info for email
        empresa = db.table("empresas").select("nombre_empresa").eq("id", vacante_data["empresa_id"]).execute()
        empresa_nombre = empresa.data[0]["nombre_empresa"] if empresa.data else "La empresa"
        
        # Send confirmation email
        email_enviado = await email_service.send_application_confirmation(
            to_email=candidato_email,  # Email está en tabla usuarios
            candidato_nombre=candidato_data["nombre_anonimo"],
            vacante_titulo=vacante_data["titulo"],
            empresa_nombre=empresa_nombre,
            puntuacion=evaluacion["puntuacion"]
        )
        
        return AplicacionCompleta(
            mensaje="Aplicación enviada exitosamente",
            puntuacion_ia=evaluacion["puntuacion"],
            compatibilidad_porcentaje=evaluacion["compatibilidad"],
            email_enviado=email_enviado
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error procesando respuestas: {str(e)}")



# ============================================================================
# CHATBOT ENDPOINTS - Conversational AI for candidate interviews
# ============================================================================

@router.post("/chatbot/iniciar")
async def iniciar_chatbot(
    aplicacion_id: str,
    candidato_nombre: str,
    vacante_titulo: str,
    preguntas: List[str]
):
    """
    Start a conversational chatbot session for candidate interview.
    
    Initializes a conversation with memory, greeting the candidate
    and asking the first question naturally.
    
    Request body:
    - aplicacion_id: Unique application identifier
    - candidato_nombre: Candidate's name for personalization
    - vacante_titulo: Job title for context
    - preguntas: List of questions to ask during interview
    
    Returns:
    - mensaje: Greeting and first question from chatbot
    - aplicacion_id: Application ID for tracking
    """
    try:
        mensaje = await chatbot_service.iniciar_conversacion(
            aplicacion_id=aplicacion_id,
            candidato_nombre=candidato_nombre,
            vacante_titulo=vacante_titulo,
            preguntas=preguntas
        )
        
        return {
            "mensaje": mensaje,
            "aplicacion_id": aplicacion_id,
            "estado": "iniciado"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al iniciar chatbot: {str(e)}"
        )


@router.post("/chatbot/siguiente")
async def siguiente_pregunta_chatbot(
    aplicacion_id: str,
    respuesta_anterior: str,
    preguntas_restantes: List[str]
):
    """
    Process candidate's answer and get next question from chatbot.
    
    Maintains conversation context using LangChain memory,
    acknowledging the previous response and naturally transitioning
    to the next question.
    
    Request body:
    - aplicacion_id: Application ID for conversation tracking
    - respuesta_anterior: Candidate's previous answer
    - preguntas_restantes: Remaining questions to ask
    
    Returns:
    - mensaje: Acknowledgment and next question
    - quedan_preguntas: Boolean indicating if more questions remain
    """
    try:
        mensaje = await chatbot_service.siguiente_pregunta(
            aplicacion_id=aplicacion_id,
            respuesta_anterior=respuesta_anterior,
            preguntas_restantes=preguntas_restantes
        )
        
        return {
            "mensaje": mensaje,
            "quedan_preguntas": len(preguntas_restantes) > 0,
            "preguntas_restantes": len(preguntas_restantes)
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error en chatbot: {str(e)}"
        )


@router.post("/chatbot/finalizar")
async def finalizar_chatbot(aplicacion_id: str):
    """
    Finalize chatbot conversation with closing message.
    
    Generates a professional farewell message and cleans up
    conversation memory to free resources.
    
    Request body:
    - aplicacion_id: Application ID to finalize
    
    Returns:
    - mensaje: Farewell message from chatbot
    - finalizado: Boolean indicating conversation ended
    """
    try:
        mensaje = await chatbot_service.finalizar_conversacion(aplicacion_id)
        
        return {
            "mensaje": mensaje,
            "finalizado": True,
            "aplicacion_id": aplicacion_id
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al finalizar chatbot: {str(e)}"
        )


@router.delete("/chatbot/limpiar/{aplicacion_id}")
async def limpiar_chatbot(aplicacion_id: str):
    """
    Clean up chatbot conversation memory.
    
    Useful for abandoned conversations or when resetting is needed.
    Frees up memory resources.
    
    Path parameter:
    - aplicacion_id: Application ID to clean up
    
    Returns:
    - mensaje: Confirmation message
    """
    try:
        chatbot_service.limpiar_conversacion(aplicacion_id)
        
        return {
            "mensaje": "Conversación limpiada exitosamente",
            "aplicacion_id": aplicacion_id
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al limpiar chatbot: {str(e)}"
        )
