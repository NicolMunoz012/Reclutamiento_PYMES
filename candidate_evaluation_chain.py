"""
Candidate Evaluation Chain - LangChain Implementation
Evaluates candidates against job requirements and provides structured feedback.
"""

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from typing import List


class CandidateEvaluation(BaseModel):
    """Structured output for candidate evaluation."""
    puntaje_general: int = Field(
        description="Puntuación general del candidato (0-100)",
        ge=0,
        le=100
    )
    fortalezas: List[str] = Field(
        description="Lista de fortalezas identificadas del candidato"
    )
    debilidades: List[str] = Field(
        description="Lista de debilidades o áreas de mejora del candidato"
    )
    recomendacion: str = Field(
        description="Recomendación final sobre la idoneidad del candidato"
    )


class CandidateEvaluationChain:
    """Chain for evaluating candidates against job requirements."""
    
    def __init__(self, llm: ChatOpenAI = None):
        """
        Initialize the evaluation chain.
        
        Args:
            llm: Language model instance. Defaults to GPT-4 if not provided.
        """
        self.llm = llm or ChatOpenAI(model="gpt-4", temperature=0.3)
        self.parser = PydanticOutputParser(pydantic_object=CandidateEvaluation)
        self.chain = self._build_chain()
    
    def _build_chain(self):
        """Build the LangChain evaluation chain."""
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", """Eres un experto reclutador de recursos humanos especializado en evaluar candidatos.
Tu tarea es analizar el perfil de un candidato contra los requisitos de un cargo específico.

Debes proporcionar:
1. Un puntaje general de 0 a 100 basado en el ajuste del candidato al cargo
2. Una lista de fortalezas específicas del candidato
3. Una lista de debilidades o áreas de mejora
4. Una recomendación clara sobre la idoneidad del candidato

Sé objetivo, específico y constructivo en tu evaluación.

{format_instructions}"""),
            ("human", """Evalúa al siguiente candidato:

**Perfil del Candidato:**
{perfil_candidato}

**Cargo:**
{cargo}

**Habilidades Requeridas:**
{habilidades_requeridas}

Proporciona tu evaluación estructurada.""")
        ])
        
        formatted_prompt = prompt.partial(
            format_instructions=self.parser.get_format_instructions()
        )
        
        return formatted_prompt | self.llm | self.parser
    
    def evaluate(
        self,
        perfil_candidato: str,
        cargo: str,
        habilidades_requeridas: str
    ) -> CandidateEvaluation:
        """
        Evaluate a candidate against job requirements.
        
        Args:
            perfil_candidato: Candidate profile description
            cargo: Job position title and description
            habilidades_requeridas: Required skills for the position
            
        Returns:
            CandidateEvaluation: Structured evaluation result
        """
        result = self.chain.invoke({
            "perfil_candidato": perfil_candidato,
            "cargo": cargo,
            "habilidades_requeridas": habilidades_requeridas
        })
        
        return result


# Example usage
if __name__ == "__main__":
    # Initialize the chain
    evaluation_chain = CandidateEvaluationChain()
    
    # Example evaluation
    result = evaluation_chain.evaluate(
        perfil_candidato="""
        Juan Pérez - Desarrollador Full Stack
        - 3 años de experiencia en desarrollo web
        - Dominio de React, Node.js, Python
        - Experiencia con bases de datos SQL y NoSQL
        - Inglés intermedio
        - Título en Ingeniería de Sistemas
        """,
        cargo="Desarrollador Full Stack Senior",
        habilidades_requeridas="""
        - 5+ años de experiencia en desarrollo web
        - Experto en React y Node.js
        - Conocimiento de arquitecturas cloud (AWS/Azure)
        - Inglés avanzado
        - Liderazgo de equipos técnicos
        """
    )
    
    print(f"Puntaje: {result.puntaje_general}/100")
    print(f"\nFortalezas:")
    for f in result.fortalezas:
        print(f"  - {f}")
    print(f"\nDebilidades:")
    for d in result.debilidades:
        print(f"  - {d}")
    print(f"\nRecomendación: {result.recomendacion}")
