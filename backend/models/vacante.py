"""
Pydantic models for Vacante (Job Posting) entities
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class VacanteCrear(BaseModel):
    """Request model for creating a job posting"""
    empresa_id: str
    titulo: str = Field(..., min_length=5, max_length=200)
    descripcion: str = Field(..., min_length=20)
    cargo: str = Field(..., max_length=100)
    tipo_contrato: str = Field(..., max_length=50)
    modalidad: str = Field(..., max_length=50)
    habilidades_requeridas: List[str]
    experiencia_min: int = Field(..., ge=0, le=30)
    experiencia_max: Optional[int] = Field(None, ge=0, le=50)
    salario_min: Optional[float] = Field(None, ge=0)
    salario_max: Optional[float] = Field(None, ge=0)
    ciudad: str = Field(..., max_length=100)


class PreguntaSugerida(BaseModel):
    """Model for AI-generated question"""
    pregunta: str
    tipo_pregunta: str  # "abierta", "si_no", "escala"


class VacanteConPreguntas(BaseModel):
    """Response model with job posting and suggested questions"""
    vacante_id: str
    preguntas_sugeridas: List[PreguntaSugerida]


class PreguntaAprobacion(BaseModel):
    """Model for approving/rejecting a question"""
    pregunta_id: str
    aprobada: bool


class AprobarPreguntas(BaseModel):
    """Request model for approving questions"""
    vacante_id: str
    preguntas_aprobadas: List[PreguntaAprobacion]


class VacantePublicada(BaseModel):
    """Model for published job posting (public view)"""
    id: str
    titulo: str
    empresa_nombre: str
    ciudad: str
    salario_min: Optional[float]
    salario_max: Optional[float]
    modalidad: str
    habilidades_requeridas: List[str]
    fecha_publicacion: datetime


class VacanteDetalle(BaseModel):
    """Detailed job posting information"""
    id: str
    titulo: str
    descripcion: str
    cargo: str
    tipo_contrato: str
    modalidad: str
    habilidades_requeridas: List[str]
    experiencia_min: int
    experiencia_max: Optional[int]
    salario_min: Optional[float]
    salario_max: Optional[float]
    ciudad: str
    empresa: dict
    fecha_publicacion: Optional[datetime]
