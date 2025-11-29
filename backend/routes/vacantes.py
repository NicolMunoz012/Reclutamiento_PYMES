"""
Vacante routes - Job posting endpoints
"""
from fastapi import APIRouter, HTTPException, Query
from models.vacante import VacantePublicada, VacanteDetalle
from database import get_db
from typing import Optional, List

router = APIRouter(prefix="/api/vacantes", tags=["Vacantes"])


@router.get("/publicadas")
async def obtener_vacantes_publicadas(
    ciudad: Optional[str] = Query(None, description="Filtrar por ciudad"),
    cargo: Optional[str] = Query(None, description="Filtrar por cargo"),
    modalidad: Optional[str] = Query(None, description="Filtrar por modalidad"),
    limit: int = Query(50, ge=1, le=100, description="Número máximo de resultados"),
    offset: int = Query(0, ge=0, description="Offset para paginación")
):
    """
    Get all published job postings with optional filters
    
    Query params:
    - ciudad: Filter by city (case-insensitive partial match)
    - cargo: Filter by job title (case-insensitive partial match)
    - modalidad: Filter by work modality (case-insensitive partial match)
    - limit: Maximum number of results (default: 50, max: 100)
    - offset: Offset for pagination (default: 0)
    
    Returns:
    - vacantes: List of published job postings with company info
    - total: Total number of matching vacantes
    - limit: Applied limit
    - offset: Applied offset
    """
    try:
        db = get_db()
        
        # Build query for vacantes
        query = db.table("vacantes").select(
            "id, titulo, ciudad, salario_min, salario_max, modalidad, habilidades_requeridas, fecha_publicacion, empresa_id",
            count="exact"  # Get total count
        ).eq("estado", "publicada")
        
        # Apply filters
        if ciudad:
            query = query.ilike("ciudad", f"%{ciudad}%")
        if cargo:
            query = query.ilike("titulo", f"%{cargo}%")
        if modalidad:
            query = query.ilike("modalidad", f"%{modalidad}%")
        
        # Apply pagination and ordering
        result = query.order("fecha_publicacion", desc=True).range(offset, offset + limit - 1).execute()
        
        # Get unique empresa_ids to fetch in batch
        empresa_ids = list(set(v["empresa_id"] for v in result.data))
        
        # Fetch all companies in one query (optimization)
        empresas_dict = {}
        if empresa_ids:
            empresas = db.table("empresas").select("id, nombre_empresa").in_("id", empresa_ids).execute()
            empresas_dict = {e["id"]: e["nombre_empresa"] for e in empresas.data}
        
        # Build response with company names
        vacantes_lista = []
        for vacante in result.data:
            empresa_nombre = empresas_dict.get(vacante["empresa_id"], "Empresa")
            
            vacantes_lista.append({
                "id": vacante["id"],
                "titulo": vacante["titulo"],
                "empresa_nombre": empresa_nombre,
                "ciudad": vacante["ciudad"],
                "salario_min": vacante.get("salario_min"),
                "salario_max": vacante.get("salario_max"),
                "modalidad": vacante["modalidad"],
                "habilidades_requeridas": vacante["habilidades_requeridas"],
                "fecha_publicacion": vacante.get("fecha_publicacion")
            })
        
        return {
            "vacantes": vacantes_lista,
            "total": result.count if hasattr(result, 'count') else len(vacantes_lista),
            "limit": limit,
            "offset": offset
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo vacantes: {str(e)}")


@router.get("/{vacante_id}/detalles")
async def obtener_detalle_vacante(vacante_id: str):
    """
    Get detailed information about a specific job posting
    
    Includes:
    - Full job posting details
    - Company information
    - Number of applications received
    - Approved questions for the position
    
    Path parameter:
    - vacante_id: UUID of the job posting
    
    Returns:
    - vacante: Complete job posting information
    - empresa: Company details
    - preguntas: List of approved questions
    - numero_aplicaciones: Count of applications received
    """
    try:
        db = get_db()
        
        # Get job posting
        vacante = db.table("vacantes").select("*").eq("id", vacante_id).execute()
        if not vacante.data:
            raise HTTPException(status_code=404, detail="Vacante no encontrada")
        
        vacante_data = vacante.data[0]
        
        # Verify it's published (optional - remove if you want to show draft vacantes too)
        if vacante_data["estado"] != "publicada":
            raise HTTPException(status_code=404, detail="Vacante no disponible")
        
        # Get company info
        empresa = db.table("empresas").select(
            "nombre_empresa, ciudad, industria, descripcion, tamaño_empresa"
        ).eq("id", vacante_data["empresa_id"]).execute()
        
        empresa_info = {}
        if empresa.data:
            empresa_info = {
                "nombre_empresa": empresa.data[0]["nombre_empresa"],
                "ciudad": empresa.data[0]["ciudad"],
                "industria": empresa.data[0]["industria"],
                "descripcion": empresa.data[0].get("descripcion"),
                "tamaño_empresa": empresa.data[0].get("tamaño_empresa")
            }
        
        # Get approved questions for this position
        preguntas = db.table("vacante_preguntas").select(
            "id, pregunta, tipo_pregunta"
        ).eq("vacante_id", vacante_id).eq("aprobada_por_empresa", True).execute()
        
        preguntas_lista = [
            {
                "id": p["id"],
                "pregunta": p["pregunta"],
                "tipo_pregunta": p["tipo_pregunta"]
            }
            for p in preguntas.data
        ]
        
        # Count applications for this position
        aplicaciones = db.table("aplicaciones").select("id", count="exact").eq("vacante_id", vacante_id).execute()
        numero_aplicaciones = aplicaciones.count if hasattr(aplicaciones, 'count') else len(aplicaciones.data)
        
        return {
            "vacante": {
                "id": vacante_data["id"],
                "titulo": vacante_data["titulo"],
                "descripcion": vacante_data["descripcion"],
                "cargo": vacante_data["cargo"],
                "tipo_contrato": vacante_data["tipo_contrato"],
                "modalidad": vacante_data["modalidad"],
                "habilidades_requeridas": vacante_data["habilidades_requeridas"],
                "experiencia_min": vacante_data["experiencia_min"],
                "experiencia_max": vacante_data.get("experiencia_max"),
                "salario_min": vacante_data.get("salario_min"),
                "salario_max": vacante_data.get("salario_max"),
                "ciudad": vacante_data["ciudad"],
                "numero_vacantes": vacante_data.get("numero_vacantes", 1),
                "beneficios": vacante_data.get("beneficios"),
                "fecha_publicacion": vacante_data.get("fecha_publicacion"),
                "fecha_cierre": vacante_data.get("fecha_cierre")
            },
            "empresa": empresa_info,
            "preguntas": preguntas_lista,
            "numero_aplicaciones": numero_aplicaciones
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo detalle de vacante: {str(e)}")
