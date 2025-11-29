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
    # TODO: Configurar tus credenciales de Supabase aquí
    # Ve a Supabase → Settings → API
    supabase_url: str = os.getenv("SUPABASE_URL", "")
    supabase_service_key: str = os.getenv("SUPABASE_SERVICE_KEY", "")
    
    # Groq API (LLaMA 3.1)
    # TODO: Configurar Groq API key
    # Ve a https://console.groq.com
    groq_api_key: str = os.getenv("GROQ_API_KEY", "")
    
    # Email
    smtp_host: str = os.getenv("SMTP_HOST", "smtp.gmail.com")
    smtp_port: int = int(os.getenv("SMTP_PORT", "587"))
    smtp_user: str = os.getenv("SMTP_USER", "")
    smtp_password: str = os.getenv("SMTP_PASSWORD", "")
    email_from: str = os.getenv("EMAIL_FROM", "")
    
    # General
    environment: str = os.getenv("ENVIRONMENT", "development")
    cors_origins: List[str] = ["http://localhost:3000", "http://localhost:5173"]
    
    class Config:
        env_file = ".env"


settings = Settings()
