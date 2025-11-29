"""
Configuration module - Loads environment variables
"""
import os
from typing import List
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Supabase
    supabase_url: str = os.getenv("SUPABASE_URL", "")
    supabase_key: str = os.getenv("SUPABASE_KEY", "")
    
    # Mantener compatibilidad con código antiguo
    @property
    def supabase_service_key(self):
        return self.supabase_key
    
    # Groq API (LLaMA 3.1)
    groq_api_key: str = os.getenv("GROQ_API_KEY", "")
    
    # Email
    smtp_host: str = os.getenv("SMTP_HOST", "smtp.gmail.com")
    smtp_port: int = int(os.getenv("SMTP_PORT", "587"))
    smtp_user: str = os.getenv("SMTP_USER", "")
    smtp_password: str = os.getenv("SMTP_PASSWORD", "")
    email_from: str = os.getenv("EMAIL_FROM", "")
    
    # General
    environment: str = os.getenv("ENVIRONMENT", "development")
    
    # CORS - Configuración dinámica para desarrollo y producción
    @property
    def cors_origins(self) -> List[str]:
        """
        Retorna lista de origins permitidos.
        En desarrollo: localhost
        En producción: agrega la URL del frontend desde variable de entorno
        """
        origins = [
            "http://localhost:3000",
            "http://localhost:5173",
            "http://localhost:5174",
        ]
        
        # Agregar frontend URL de producción si existe
        frontend_url = os.getenv("FRONTEND_URL", "")
        if frontend_url:
            origins.append(frontend_url)
            # También permitir sin trailing slash
            if frontend_url.endswith("/"):
                origins.append(frontend_url.rstrip("/"))
            else:
                origins.append(f"{frontend_url}/")
        
        return origins
    
    class Config:
        env_file = ".env"
        extra = "allow"


settings = Settings()

# Debug: Mostrar configuración al iniciar (útil para troubleshooting)
print(f"🌍 Environment: {settings.environment}")
print(f"🔐 CORS Origins: {settings.cors_origins}")
print(f"✅ Supabase URL: {settings.supabase_url[:30]}..." if settings.supabase_url else "❌ Supabase URL no configurada")
print(f"✅ Groq API Key: {'Configurada' if settings.groq_api_key else '❌ No configurada'}")