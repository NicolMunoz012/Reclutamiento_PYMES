"""
Pydantic models for Candidato (Candidate) entities
"""
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime


class CandidatoAplicar(BaseModel):
    """Request model for candidate application (form data)"""
    vacante_id: str
    nombre_anonimo: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    telefono: str = Field(..., max_length=20)
    ciudad: str = Field(..., max_length=100)
    años_experiencia: int = Field(..., ge=0, le=50)


class PreguntaVacante(BaseModel):
    """Model for job posting question"""
    pregunta_id: str
    pregunta: str
    tipo_pregunta: str


class AplicacionConPreguntas(BaseModel):
    """Response after application with questions to answer"""
    candidato_id: str
    aplicacion_id: str
    preguntas: List[PreguntaVacante]


class RespuestaCandidato(BaseModel):
    """Model for candidate's answer to a question"""
    pregunta_id: str
    respuesta: str


class ResponderPreguntas(BaseModel):
    """Request model for submitting answers"""
    aplicacion_id: str
    respuestas: List[RespuestaCandidato]


class EvaluacionIA(BaseModel):
    """AI evaluation result"""
    puntuacion: int = Field(..., ge=0, le=100)
    compatibilidad: int = Field(..., ge=0, le=100)
    fortalezas: List[str]
    debilidades: List[str]


class AplicacionCompleta(BaseModel):
    """Response after completing application"""
    mensaje: str
    puntuacion_ia: int
    compatibilidad_porcentaje: int
    email_enviado: bool


class AplicacionDetalle(BaseModel):
    """Detailed application information for company view"""
    candidato_nombre: str
    vacante_titulo: str
    puntuacion_ia: Optional[int]
    compatibilidad_porcentaje: Optional[int]
    estado: str
    fecha_aplicacion: datetime  # Mapeado desde created_at
    aplicacion_id: str
