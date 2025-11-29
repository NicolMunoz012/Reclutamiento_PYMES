"""
AI Service - Integration with Groq API (LLaMA 3.1) using LangChain
"""
import json
import os
from typing import List, Dict
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from config import settings

print("--- DEBUG GROQ KEY START ---")
print(f"GROQ_API_KEY value: {os.getenv('GROQ_API_KEY')}")
print("--- DEBUG GROQ KEY END ---")

class IAService:
    """
    Service for AI operations using Groq API (LLaMA 3.1) through LangChain.
    
    This service handles all AI-powered features:
    - Question generation for job postings
    - CV analysis and information extraction
    - Candidate-job compatibility evaluation
    
    Uses LangChain for better prompt management and chain composition.
    """
    
    def __init__(self):
        """Initialize LangChain Groq client with configuration"""
        if not settings.groq_api_key:
            raise ValueError(
                "Groq API key not configured. "
                "Please set GROQ_API_KEY in .env file"
            )
        
        # Configure Groq with LangChain
        # Modelo: llama-3.1-8b-instant (rápido y eficiente)
        self.llm = ChatGroq(
            model="llama-3.1-8b-instant",
            groq_api_key=settings.groq_api_key,
            max_tokens=2000,
            temperature=0.7
        )
    
    async def generar_preguntas_vacante(
        self,
        titulo: str,
        descripcion: str,
        habilidades_requeridas: List[str],
        experiencia_min: int
    ) -> List[Dict[str, str]]:
        """
        Generate intelligent questions for a job posting using LangChain.
        
        Uses a structured prompt template and LLMChain for better
        prompt management and consistency.
        
        Args:
            titulo: Job title
            descripcion: Job description
            habilidades_requeridas: Required skills list
            experiencia_min: Minimum years of experience
            
        Returns:
            List of questions with type (abierta, si_no, escala)
        """
        habilidades_str = ", ".join(habilidades_requeridas)
        
        # Define structured prompt template
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", """Eres un experto en reclutamiento de tecnología con 10+ años de experiencia.
Tu trabajo es generar preguntas inteligentes que evalúen de forma efectiva a los candidatos.

Las preguntas deben:
- Ser específicas al cargo y tecnologías
- Evaluar tanto habilidades técnicas como blandas
- Ser claras y directas
- Permitir al candidato demostrar su experiencia real
"""),
            ("user", """Genera 5-7 preguntas para esta vacante:

**Título:** {titulo}
**Descripción:** {descripcion}
**Habilidades requeridas:** {habilidades}
**Experiencia mínima:** {experiencia_min} años

Retorna ÚNICAMENTE un JSON válido con este formato exacto:
[
  {{
    "pregunta": "texto de la pregunta aquí",
    "tipo_pregunta": "abierta"
  }},
  {{
    "pregunta": "texto de la pregunta aquí",
    "tipo_pregunta": "si_no"
  }}
]

Tipos válidos: "abierta", "si_no", "escala"
No incluyas markdown, ni código, ni explicaciones. Solo el JSON.
""")
        ])
        
        # Create LangChain chain
        chain = prompt_template | self.llm
        
        try:
            # Execute chain asynchronously
            response = await chain.ainvoke({
                "titulo": titulo,
                "descripcion": descripcion,
                "habilidades": habilidades_str,
                "experiencia_min": experiencia_min
            })
            
            response_text = response.content.strip()
            
            # Parse JSON response
            preguntas = self._parse_json_response(response_text)
            return preguntas
            
        except Exception as e:
            print(f"Error generating questions with LangChain: {e}")
            # Fallback questions
            return self._get_fallback_questions(habilidades_requeridas, experiencia_min)
    
    async def analizar_cv(self, cv_text: str) -> Dict:
        """
        Analyze CV and extract key information using LangChain.
        
        Extracts structured data from CV text including skills,
        experience, education, and professional summary.
        
        Args:
            cv_text: Extracted text from PDF
            
        Returns:
            Dictionary with extracted information
        """
        # Define structured prompt template
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", """Eres un experto en análisis de CVs y perfiles profesionales.
Extrae información clave de forma precisa y estructurada."""),
            ("user", """Analiza este CV y extrae:

**CV:**
{cv_text}

Retorna ÚNICAMENTE un JSON con este formato:
{{
  "habilidades": ["Python", "React", "..."],
  "experiencia_años": 4,
  "educacion": "Ingeniería de Sistemas",
  "resumen": "Breve resumen profesional en 2-3 líneas"
}}

Si no encuentras algún dato, usa null o [] según corresponda.
No incluyas markdown ni explicaciones, solo el JSON.
""")
        ])
        
        # Create LangChain chain
        chain = prompt_template | self.llm
        
        try:
            # Limit CV text to avoid token limits
            cv_text_limited = cv_text[:4000]
            
            # Execute chain asynchronously
            response = await chain.ainvoke({"cv_text": cv_text_limited})
            
            response_text = response.content.strip()
            
            # Parse JSON response
            analisis = self._parse_json_response(response_text)
            return analisis
            
        except Exception as e:
            print(f"Error analyzing CV with LangChain: {e}")
            return {
                "habilidades": [],
                "experiencia_años": 0,
                "educacion": "No especificada",
                "resumen": "Error al analizar CV"
            }
    
    async def evaluar_compatibilidad(
        self,
        cv_text: str,
        respuestas: List[Dict[str, str]],
        titulo: str,
        habilidades_requeridas: List[str],
        experiencia_min: int
    ) -> Dict:
        """
        Evaluate candidate compatibility with job posting using LangChain.
        
        Analyzes CV and interview responses to calculate compatibility
        scores and identify strengths and weaknesses.
        
        Args:
            cv_text: CV text
            respuestas: Candidate's answers to interview questions
            titulo: Job title
            habilidades_requeridas: Required skills
            experiencia_min: Minimum experience required
            
        Returns:
            Evaluation with score, compatibility, strengths, and weaknesses
        """
        habilidades_str = ", ".join(habilidades_requeridas)
        
        # Format responses for better readability
        respuestas_formateadas = "\n".join([
            f"- {r.get('pregunta', 'N/A')}\n  Respuesta: {r.get('respuesta', 'N/A')}"
            for r in respuestas
        ])
        
        # Define structured prompt template
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", """Eres un experto en evaluación de candidatos para posiciones tecnológicas.
Tu análisis debe ser objetivo, justo y basado en evidencia concreta."""),
            ("user", """Evalúa la compatibilidad entre este candidato y la vacante.

**VACANTE:**
- Título: {titulo}
- Habilidades requeridas: {habilidades}
- Experiencia mínima: {experiencia_min} años

**CANDIDATO:**
CV: {cv_text}

**RESPUESTAS A PREGUNTAS:**
{respuestas}

Analiza y retorna ÚNICAMENTE un JSON:
{{
  "puntuacion": 85,
  "compatibilidad": 78,
  "fortalezas": ["Experiencia sólida en React", "Buena comunicación"],
  "debilidades": ["Poca experiencia con microservicios"]
}}

- puntuacion: 0-100 (evaluación general del candidato)
- compatibilidad: 0-100 (qué tan bien encaja con esta vacante específica)
- fortalezas: lista de 2-4 puntos fuertes
- debilidades: lista de 1-3 áreas de mejora

Sé honesto pero constructivo. No incluyas markdown ni explicaciones.
""")
        ])
        
        # Create LangChain chain
        chain = prompt_template | self.llm
        
        try:
            # Limit CV text to avoid token limits
            cv_text_limited = cv_text[:3000]
            
            # Execute chain asynchronously
            response = await chain.ainvoke({
                "titulo": titulo,
                "habilidades": habilidades_str,
                "experiencia_min": experiencia_min,
                "cv_text": cv_text_limited,
                "respuestas": respuestas_formateadas
            })
            
            response_text = response.content.strip()
            
            # Parse JSON response
            evaluacion = self._parse_json_response(response_text)
            
            # Validate scores are within range
            evaluacion["puntuacion"] = max(0, min(100, evaluacion.get("puntuacion", 50)))
            evaluacion["compatibilidad"] = max(0, min(100, evaluacion.get("compatibilidad", 50)))
            
            return evaluacion
            
        except Exception as e:
            print(f"Error evaluating compatibility with LangChain: {e}")
            return {
                "puntuacion": 50,
                "compatibilidad": 50,
                "fortalezas": ["Candidato con potencial"],
                "debilidades": ["Requiere evaluación manual"]
            }
    
    def _parse_json_response(self, response_text: str) -> Dict:
        """
        Parse JSON from LLM response, handling markdown code blocks.
        
        Args:
            response_text: Raw response from LLM
            
        Returns:
            Parsed JSON as dictionary
        """
        try:
            # Try direct JSON parsing first
            return json.loads(response_text)
        except json.JSONDecodeError:
            # Remove markdown code blocks if present
            text = response_text.strip()
            if text.startswith("```"):
                lines = text.split("\n")
                text = "\n".join(lines[1:-1])
                if text.startswith("json"):
                    text = text[4:]
            return json.loads(text.strip())
    
    def _get_fallback_questions(
        self,
        habilidades_requeridas: List[str],
        experiencia_min: int
    ) -> List[Dict[str, str]]:
        """
        Generate fallback questions when AI fails.
        
        Args:
            habilidades_requeridas: Required skills
            experiencia_min: Minimum experience
            
        Returns:
            List of basic fallback questions
        """
        return [
            {
                "pregunta": f"¿Cuál es tu experiencia con {habilidades_requeridas[0] if habilidades_requeridas else 'las tecnologías requeridas'}?",
                "tipo_pregunta": "abierta"
            },
            {
                "pregunta": "¿Puedes describir un proyecto relevante en el que hayas trabajado?",
                "tipo_pregunta": "abierta"
            },
            {
                "pregunta": f"¿Tienes al menos {experiencia_min} años de experiencia en este campo?",
                "tipo_pregunta": "si_no"
            }
        ]


# Singleton instance
ia_service = IAService()
