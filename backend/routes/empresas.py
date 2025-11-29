"""
Empresa routes - Company endpoints
"""
from fastapi import APIRouter, HTTPException
from models.empresa import EmpresaRegistro, EmpresaResponse
from models.vacante import VacanteCrear, VacanteConPreguntas, AprobarPreguntas
from models.candidato import AplicacionDetalle
from database import get_db
from services.ia_service import ia_service
import uuid
from datetime import datetime

router = APIRouter(prefix="/api/empresa", tags=["Empresas"])


@router.post("/registrar", response_model=EmpresaResponse)
async def registrar_empresa(empresa: EmpresaRegistro):
    """
    Register a new company
    
    Creates user and company records in database
    """
    try:
        db = get_db()
        
        # Create user record
        usuario_id = str(uuid.uuid4())
        usuario_data = {
            "id": usuario_id,
            "email": empresa.email,
            "tipo_usuario": "empresa",
            "fecha_registro": datetime.utcnow().isoformat()
        }
        
        db.table("usuarios").insert(usuario_data).execute()
        
        # Create company record
        empresa_id = str(uuid.uuid4())
        empresa_data = {
            "id": empresa_id,
            "usuario_id": usuario_id,
            "nombre_empresa": empresa.nombre_empresa,
            "nit": empresa.nit,
            "industria": empresa.industria,
            "tamaño_empresa": empresa.tamaño_empresa,
            "descripcion": empresa.descripcion,
            "ciudad": empresa.ciudad,
            "email": empresa.email,
            "fecha_registro": datetime.utcnow().isoformat()
        }
        
        db.table("empresas").insert(empresa_data).execute()
        
        return EmpresaResponse(
            empresa_id=empresa_id,
            mensaje="Empresa registrada exitosamente"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error registrando empresa: {str(e)}")


@router.post("/crear-vacante", response_model=VacanteConPreguntas)
async def crear_vacante(vacante: VacanteCrear):
    """
    Create a new job posting and generate AI questions
    
    1. Saves job posting as draft
    2. Generates intelligent questions using Claude AI
    3. Saves questions to database
    4. Returns questions for company approval
    """
    try:
        db = get_db()
        
        # Verify company exists
        empresa_check = db.table("empresas").select("id").eq("id", vacante.empresa_id).execute()
        if not empresa_check.data:
            raise HTTPException(status_code=404, detail="Empresa no encontrada")
        
        # Create job posting
        vacante_id = str(uuid.uuid4())
        vacante_data = {
            "id": vacante_id,
            "empresa_id": vacante.empresa_id,
            "titulo": vacante.titulo,
            "descripcion": vacante.descripcion,
            "cargo": vacante.cargo,
            "tipo_contrato": vacante.tipo_contrato,
            "modalidad": vacante.modalidad,
            "habilidades_requeridas": vacante.habilidades_requeridas,
            "experiencia_min": vacante.experiencia_min,
            "experiencia_max": vacante.experiencia_max,
            "salario_min": vacante.salario_min,
            "salario_max": vacante.salario_max,
            "ciudad": vacante.ciudad,
            "estado": "borrador",
            "fecha_creacion": datetime.utcnow().isoformat()
        }
        
        db.table("vacantes").insert(vacante_data).execute()
        
        # Generate questions using AI
        preguntas_ia = await ia_service.generar_preguntas_vacante(
            titulo=vacante.titulo,
            descripcion=vacante.descripcion,
            habilidades_requeridas=vacante.habilidades_requeridas,
            experiencia_min=vacante.experiencia_min
        )
        
        # Save questions to database
        preguntas_guardadas = []
        for pregunta_data in preguntas_ia:
            pregunta_id = str(uuid.uuid4())
            pregunta_record = {
                "id": pregunta_id,
                "vacante_id": vacante_id,
                "pregunta": pregunta_data["pregunta"],
                "tipo_pregunta": pregunta_data["tipo_pregunta"],
                "aprobada_por_empresa": False,
                "fecha_creacion": datetime.utcnow().isoformat()
            }
            
            db.table("vacante_preguntas").insert(pregunta_record).execute()
            
            preguntas_guardadas.append({
                "pregunta_id": pregunta_id,
                **pregunta_data
            })
        
        return VacanteConPreguntas(
            vacante_id=vacante_id,
            preguntas_sugeridas=preguntas_ia
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creando vacante: {str(e)}")


@router.post("/aprobar-preguntas")
async def aprobar_preguntas(aprobacion: AprobarPreguntas):
    """
    Approve/reject questions and publish job posting
    
    Updates question approval status and publishes the job
    """
    try:
        db = get_db()
        
        # Update each question's approval status
        for pregunta in aprobacion.preguntas_aprobadas:
            db.table("vacante_preguntas").update({
                "aprobada_por_empresa": pregunta.aprobada
            }).eq("id", pregunta.pregunta_id).execute()
        
        # Publish job posting
        db.table("vacantes").update({
            "estado": "publicada",
            "fecha_publicacion": datetime.utcnow().isoformat()
        }).eq("id", aprobacion.vacante_id).execute()
        
        return {
            "mensaje": "Vacante publicada exitosamente",
            "vacante_id": aprobacion.vacante_id
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error aprobando preguntas: {str(e)}")


@router.get("/{empresa_id}/aplicaciones")
async def obtener_aplicaciones(empresa_id: str):
    """
    Get all applications for company's job postings
    
    Returns list of applications with candidate info and scores
    """
    try:
        db = get_db()
        
        # Get applications for this company's job postings
        query = """
            SELECT 
                a.id as aplicacion_id,
                a.estado,
                a.fecha_aplicacion,
                a.puntuacion_ia,
                a.compatibilidad_porcentaje,
                c.nombre_anonimo as candidato_nombre,
                v.titulo as vacante_titulo
            FROM aplicaciones a
            JOIN candidatos c ON a.candidato_id = c.id
            JOIN vacantes v ON a.vacante_id = v.id
            WHERE v.empresa_id = '{}'
            ORDER BY a.fecha_aplicacion DESC
        """.format(empresa_id)
        
        result = db.rpc('exec_sql', {'query': query}).execute()
        
        if not result.data:
            # Fallback: manual join
            vacantes = db.table("vacantes").select("id").eq("empresa_id", empresa_id).execute()
            vacante_ids = [v["id"] for v in vacantes.data]
            
            if not vacante_ids:
                return {"aplicaciones": []}
            
            aplicaciones_data = []
            for vacante_id in vacante_ids:
                apps = db.table("aplicaciones").select("*").eq("vacante_id", vacante_id).execute()
                
                for app in apps.data:
                    candidato = db.table("candidatos").select("nombre_anonimo").eq("id", app["candidato_id"]).execute()
                    vacante = db.table("vacantes").select("titulo").eq("id", app["vacante_id"]).execute()
                    
                    aplicaciones_data.append({
                        "aplicacion_id": app["id"],
                        "candidato_nombre": candidato.data[0]["nombre_anonimo"] if candidato.data else "N/A",
                        "vacante_titulo": vacante.data[0]["titulo"] if vacante.data else "N/A",
                        "puntuacion_ia": app.get("puntuacion_ia"),
                        "compatibilidad_porcentaje": app.get("compatibilidad_porcentaje"),
                        "estado": app["estado"],
                        "fecha_aplicacion": app["fecha_aplicacion"]
                    })
            
            return {"aplicaciones": aplicaciones_data}
        
        return {"aplicaciones": result.data}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo aplicaciones: {str(e)}")
