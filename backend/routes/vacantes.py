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
    modalidad: Optional[str] = Query(None, description="Filtrar por modalidad")
):
    """
    Get all published job postings with optional filters
    
    Query params:
    - ciudad: Filter by city
    - cargo: Filter by job title
    - modalidad: Filter by work modality
    """
    try:
        db = get_db()
        
        # Build query
        query = db.table("vacantes").select(
            "id, titulo, ciudad, salario_min, salario_max, modalidad, habilidades_requeridas, fecha_publicacion, empresa_id"
        ).eq("estado", "publicada")
        
        # Apply filters
        if ciudad:
            query = query.ilike("ciudad", f"%{ciudad}%")
        if cargo:
            query = query.ilike("titulo", f"%{cargo}%")
        if modalidad:
            query = query.ilike("modalidad", f"%{modalidad}%")
        
        result = query.order("fecha_publicacion", desc=True).execute()
        
        # Enrich with company names
        vacantes_lista = []
        for vacante in result.data:
            empresa = db.table("empresas").select("nombre_empresa").eq("id", vacante["empresa_id"]).execute()
            empresa_nombre = empresa.data[0]["nombre_empresa"] if empresa.data else "Empresa"
            
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
        
        return {"vacantes": vacantes_lista}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo vacantes: {str(e)}")


@router.get("/{vacante_id}/detalles")
async def obtener_detalle_vacante(vacante_id: str):
    """
    Get detailed information about a specific job posting
    
    Includes company information and full job description
    """
    try:
        db = get_db()
        
        # Get job posting
        vacante = db.table("vacantes").select("*").eq("id", vacante_id).execute()
        if not vacante.data:
            raise HTTPException(status_code=404, detail="Vacante no encontrada")
        
        vacante_data = vacante.data[0]
        
        # Get company info
        empresa = db.table("empresas").select(
            "nombre_empresa, ciudad, industria, descripcion"
        ).eq("id", vacante_data["empresa_id"]).execute()
        
        empresa_info = {}
        if empresa.data:
            empresa_info = {
                "nombre_empresa": empresa.data[0]["nombre_empresa"],
                "ciudad": empresa.data[0]["ciudad"],
                "industria": empresa.data[0]["industria"],
                "descripcion": empresa.data[0].get("descripcion")
            }
        
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
                "empresa": empresa_info,
                "fecha_publicacion": vacante_data.get("fecha_publicacion")
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo detalle de vacante: {str(e)}")
