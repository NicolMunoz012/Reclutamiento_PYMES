"""
Chatbot Service - Conversational AI for candidate interviews using LangChain
"""
import os
from typing import List, Dict
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from config import settings


class ChatbotService:
    """
    Service for managing conversational chatbot interactions with candidates.
    
    Uses LangChain with conversation memory to maintain context across
    multiple messages, creating a natural and engaging interview experience.
    
    Features:
    - Maintains conversation history per application
    - Natural language question flow
    - Empathetic and professional tone
    - Handles multiple concurrent conversations
    """
    
    def __init__(self):
        """Initialize LangChain Groq client for chatbot conversations"""
        if not settings.groq_api_key:
            raise ValueError(
                "Groq API key not configured. "
                "Please set GROQ_API_KEY in .env file"
            )
        
        # Configure Groq with LangChain for conversational AI
        # Modelo: llama-3.1-8b-instant (rápido y conversacional)
        self.llm = ChatGroq(
            model="llama-3.1-8b-instant",
            groq_api_key=settings.groq_api_key,
            max_tokens=500,  # Shorter responses for chatbot
            temperature=0.8  # More creativity for natural conversation
        )
        
        # Store conversation history for each application
        # Key: aplicacion_id, Value: List of messages
        self.conversations: Dict[str, List] = {}
    
    def _get_or_create_history(self, aplicacion_id: str) -> List:
        """
        Get or create conversation history for a specific application.
        
        Args:
            aplicacion_id: Unique application identifier
            
        Returns:
            List of messages for this conversation
        """
        if aplicacion_id not in self.conversations:
            self.conversations[aplicacion_id] = []
        return self.conversations[aplicacion_id]
    
    async def iniciar_conversacion(
        self,
        aplicacion_id: str,
        candidato_nombre: str,
        vacante_titulo: str,
        preguntas: List[str]
    ) -> str:
        """
        Start a conversation with personalized greeting and first question.
        
        Creates a warm, professional introduction and naturally transitions
        into the first interview question.
        
        Args:
            aplicacion_id: Application ID for tracking
            candidato_nombre: Candidate's name
            vacante_titulo: Job posting title
            preguntas: List of questions to ask during interview
            
        Returns:
            Greeting message with first question
        """
        history = self._get_or_create_history(aplicacion_id)
        
        # Format questions for the prompt
        preguntas_formateadas = "\n".join([f"- {p}" for p in preguntas])
        
        # Define conversational prompt template
        prompt = ChatPromptTemplate.from_messages([
            ("system", f"""Eres un asistente de reclutamiento amigable y profesional llamado Alex.

Estás conversando con {candidato_nombre} quien aplicó a la vacante: {vacante_titulo}.

Tu trabajo es:
1. Hacer que el candidato se sienta cómodo y bienvenido
2. Hacer preguntas de forma natural, una a la vez
3. Mostrar empatía y profesionalismo
4. Agradecer cada respuesta antes de la siguiente pregunta

Tienes estas preguntas para hacer:
{preguntas_formateadas}

IMPORTANTE: 
- Haz UNA sola pregunta a la vez y espera respuesta
- Sé conversacional, no robótico
- Usa un tono cálido pero profesional
"""),
            MessagesPlaceholder(variable_name="chat_history"),
            ("user", "{input}")
        ])
        
        # Create the chain
        chain = prompt | self.llm
        
        try:
            # Generate greeting and first question
            response = await chain.ainvoke({
                "chat_history": history,
                "input": "Inicia la conversación con un saludo cálido y haz la primera pregunta."
            })
            
            # Update history
            history.append(HumanMessage(content="Inicia la conversación con un saludo cálido y haz la primera pregunta."))
            history.append(AIMessage(content=response.content))
            
            return response.content
            
        except Exception as e:
            print(f"Error starting chatbot conversation: {e}")
            # Fallback greeting
            return f"¡Hola {candidato_nombre}! Gracias por tu interés en {vacante_titulo}. Comencemos con algunas preguntas. {preguntas[0] if preguntas else '¿Puedes contarme sobre tu experiencia?'}"
    
    async def siguiente_pregunta(
        self,
        aplicacion_id: str,
        respuesta_anterior: str,
        preguntas_restantes: List[str]
    ) -> str:
        """
        Process previous answer and ask the next question naturally.
        
        Acknowledges the candidate's response and smoothly transitions
        to the next question, maintaining conversational flow.
        
        Args:
            aplicacion_id: Application ID
            respuesta_anterior: Candidate's previous answer
            preguntas_restantes: Remaining questions to ask
            
        Returns:
            Next question from the chatbot
        """
        history = self._get_or_create_history(aplicacion_id)
        
        # Format remaining questions
        preguntas_formateadas = "\n".join([f"- {p}" for p in preguntas_restantes]) if preguntas_restantes else "No hay más preguntas"
        
        # Define conversational prompt template
        prompt = ChatPromptTemplate.from_messages([
            ("system", f"""Eres un asistente de reclutamiento conversacional.

El candidato acaba de responder. Debes:
1. Agradecer brevemente su respuesta (1 frase corta y natural)
2. Hacer la siguiente pregunta de forma natural

Preguntas restantes: 
{preguntas_formateadas}

Si no quedan preguntas, despídete agradeciendo su tiempo y menciona que recibirán noticias pronto.

Mantén un tono profesional pero cálido. No seas repetitivo en los agradecimientos.
"""),
            MessagesPlaceholder(variable_name="chat_history"),
            ("user", "{input}")
        ])
        
        # Create the chain
        chain = prompt | self.llm
        
        try:
            user_input = f"El candidato respondió: '{respuesta_anterior}'. "
            
            if preguntas_restantes:
                user_input += "Ahora haz la siguiente pregunta."
            else:
                user_input += "Ya no hay más preguntas. Despídete de forma profesional."
            
            # Generate acknowledgment and next question
            response = await chain.ainvoke({
                "chat_history": history,
                "input": user_input
            })
            
            # Update history
            history.append(HumanMessage(content=user_input))
            history.append(AIMessage(content=response.content))
            
            # Limit history to last 20 messages to avoid token limits
            if len(history) > 20:
                self.conversations[aplicacion_id] = history[-20:]
            
            return response.content
            
        except Exception as e:
            print(f"Error in chatbot next question: {e}")
            # Fallback response
            if preguntas_restantes:
                return f"Gracias por tu respuesta. {preguntas_restantes[0]}"
            else:
                return "Gracias por tu tiempo. Hemos completado la entrevista. Recibirás noticias pronto."
    
    async def finalizar_conversacion(self, aplicacion_id: str) -> str:
        """
        Generate closing message for the conversation.
        
        Creates a professional and motivating farewell message,
        thanking the candidate and setting expectations.
        
        Args:
            aplicacion_id: Application ID
            
        Returns:
            Farewell message
        """
        history = self._get_or_create_history(aplicacion_id)
        
        # Define closing prompt template
        prompt = ChatPromptTemplate.from_messages([
            ("system", """Genera un mensaje de despedida profesional y motivador.

Agradece al candidato por:
- Su tiempo
- Sus respuestas honestas
- Su interés en la posición

Menciona que:
- El equipo revisará su aplicación
- Recibirán noticias pronto
- Pueden contactarnos si tienen preguntas

Mantén un tono positivo y profesional. Sé breve (2-3 frases).
"""),
            MessagesPlaceholder(variable_name="chat_history"),
            ("user", "Genera el mensaje de cierre de la entrevista.")
        ])
        
        # Create the chain
        chain = prompt | self.llm
        
        try:
            # Generate closing message
            response = await chain.ainvoke({
                "chat_history": history,
                "input": "Genera el mensaje de cierre de la entrevista."
            })
            
            # Clean up memory after conversation ends
            if aplicacion_id in self.conversations:
                del self.conversations[aplicacion_id]
            
            return response.content
            
        except Exception as e:
            print(f"Error finalizing chatbot conversation: {e}")
            # Fallback closing
            return "¡Muchas gracias por tu tiempo! Hemos completado la entrevista. Nuestro equipo revisará tu aplicación y te contactaremos pronto. ¡Mucho éxito!"
    
    def limpiar_conversacion(self, aplicacion_id: str) -> None:
        """
        Clean up conversation memory for a specific application.
        
        Useful for freeing memory when conversation is abandoned
        or needs to be reset.
        
        Args:
            aplicacion_id: Application ID to clean up
        """
        if aplicacion_id in self.conversations:
            del self.conversations[aplicacion_id]
            print(f"Conversation memory cleaned for application: {aplicacion_id}")


# Singleton instance
chatbot_service = ChatbotService()