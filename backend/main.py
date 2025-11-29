"""
FastAPI Main Application - Recruitment System Backend
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import settings
from routes import empresas, candidatos, vacantes


# Initialize FastAPI app
app = FastAPI(
    title="Sistema de Reclutamiento Inteligente",
    description="Backend API para sistema de reclutamiento con IA",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(empresas.router)
app.include_router(candidatos.router)
app.include_router(vacantes.router)


@app.get("/")
async def root():
    """Root endpoint - API health check"""
    return {
        "message": "Sistema de Reclutamiento Inteligente API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "environment": settings.environment
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True if settings.environment == "development" else False
    )
