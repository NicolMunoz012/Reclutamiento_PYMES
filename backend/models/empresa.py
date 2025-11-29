"""
Pydantic models for Empresa (Company) entities
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class EmpresaRegistro(BaseModel):
    """Request model for company registration"""
    nombre_empresa: str = Field(..., min_length=2, max_length=200)
    nit: str = Field(..., min_length=5, max_length=50)
    industria: str = Field(..., max_length=100)
    tamaño_empresa: str = Field(..., max_length=50)
    descripcion: Optional[str] = None
    ciudad: str = Field(..., max_length=100)
    email: EmailStr


class EmpresaResponse(BaseModel):
    """Response model for company registration"""
    empresa_id: str
    mensaje: str


class EmpresaDetalle(BaseModel):
    """Detailed company information"""
    id: str
    nombre_empresa: str
    nit: str
    industria: str
    tamaño_empresa: str
    descripcion: Optional[str]
    ciudad: str
    email: str
    fecha_registro: datetime
