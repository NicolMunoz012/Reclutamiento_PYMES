# 🤖 Chatbot Examples - LangChain Conversational AI

Ejemplos de uso del chatbot conversacional con memoria.

## 📋 Overview

El chatbot usa LangChain con `ConversationBufferMemory` para mantener contexto entre mensajes, creando una experiencia natural y fluida.

## 🎯 Flujo Completo

### 1. Iniciar Conversación

**Request:**
```bash
curl -X POST http://localhost:8000/api/candidato/chatbot/iniciar \
  -H "Content-Type: application/json" \
  -d '{
    "aplicacion_id": "app-123",
    "candidato_nombre": "María García",
    "vacante_titulo": "Desarrolladora Full Stack Senior",
    "preguntas": [
      "¿Cuál es tu experiencia con React y Node.js?",
      "¿Has liderado proyectos de desarrollo?",
      "¿Cómo manejas el trabajo bajo presión?"
    ]
  }'
```

**Response:**
```json
{
  "mensaje": "¡Hola María! Gracias por tu interés en la posición de Desarrolladora Full Stack Senior. Me encantaría conocer más sobre tu experiencia. Para empezar, ¿cuál es tu experiencia con React y Node.js?",
  "aplicacion_id": "app-123",
  "estado": "iniciado"
}
```

### 2. Primera Respuesta del Candidato

**Request:**
```bash
curl -X POST http://localhost:8000/api/candidato/chatbot/siguiente \
  -H "Content-Type: application/json" \
  -d '{
    "aplicacion_id": "app-123",
    "respuesta_anterior": "Tengo 4 años de experiencia con React en el frontend y 3 años con Node.js en el backend. He desarrollado aplicaciones completas usando el stack MERN y también he trabajado con Next.js para SSR.",
    "preguntas_restantes": [
      "¿Has liderado proyectos de desarrollo?",
      "¿Cómo manejas el trabajo bajo presión?"
    ]
  }'
```

**Response:**
```json
{
  "mensaje": "Excelente, esa es una experiencia muy sólida con el stack MERN. Ahora me gustaría saber, ¿has liderado proyectos de desarrollo?",
  "quedan_preguntas": true,
  "preguntas_restantes": 2
}
```

### 3. Segunda Respuesta del Candidato

**Request:**
```bash
curl -X POST http://localhost:8000/api/candidato/chatbot/siguiente \
  -H "Content-Type: application/json" \
  -d '{
    "aplicacion_id": "app-123",
    "respuesta_anterior": "Sí, he liderado dos proyectos importantes. El primero fue una plataforma de e-commerce con un equipo de 5 desarrolladores, y el segundo fue un sistema de gestión interna con 3 desarrolladores. En ambos casos coordiné sprints, revisiones de código y entregas.",
    "preguntas_restantes": [
      "¿Cómo manejas el trabajo bajo presión?"
    ]
  }'
```

**Response:**
```json
{
  "mensaje": "Impresionante experiencia de liderazgo. Una última pregunta: ¿cómo manejas el trabajo bajo presión?",
  "quedan_preguntas": true,
  "preguntas_restantes": 1
}
```

### 4. Última Respuesta del Candidato

**Request:**
```bash
curl -X POST http://localhost:8000/api/candidato/chatbot/siguiente \
  -H "Content-Type: application/json" \
  -d '{
    "aplicacion_id": "app-123",
    "respuesta_anterior": "Mantengo la calma priorizando tareas, comunicándome claramente con el equipo y dividiendo problemas grandes en partes manejables. También practico mindfulness y hago ejercicio regularmente para mantener el equilibrio.",
    "preguntas_restantes": []
  }'
```

**Response:**
```json
{
  "mensaje": "Gracias por compartir eso, María. Aprecio mucho tu tiempo y tus respuestas honestas. Hemos completado la entrevista. Nuestro equipo revisará tu aplicación cuidadosamente y te contactaremos pronto con los siguientes pasos. ¡Mucho éxito!",
  "quedan_preguntas": false,
  "preguntas_restantes": 0
}
```

### 5. Finalizar Conversación (Opcional)

**Request:**
```bash
curl -X POST http://localhost:8000/api/candidato/chatbot/finalizar \
  -H "Content-Type: application/json" \
  -d '{
    "aplicacion_id": "app-123"
  }'
```

**Response:**
```json
{
  "mensaje": "¡Muchas gracias por tu tiempo, María! Ha sido un placer conversar contigo. Nuestro equipo revisará tu aplicación y te contactaremos pronto. Si tienes alguna pregunta, no dudes en contactarnos. ¡Te deseamos mucho éxito!",
  "finalizado": true,
  "aplicacion_id": "app-123"
}
```

## 🎨 Ejemplo con Python

```python
import requests
import json

BASE_URL = "http://localhost:8000"

def chatbot_flow_example():
    """Ejemplo completo del flujo del chatbot"""
    
    # 1. Iniciar conversación
    print("1. Iniciando conversación...")
    response = requests.post(
        f"{BASE_URL}/api/candidato/chatbot/iniciar",
        json={
            "aplicacion_id": "test-456",
            "candidato_nombre": "Carlos Ruiz",
            "vacante_titulo": "Backend Developer",
            "preguntas": [
                "¿Experiencia con Python?",
                "¿Conoces FastAPI?",
                "¿Has trabajado con bases de datos?"
            ]
        }
    )
    
    data = response.json()
    print(f"Chatbot: {data['mensaje']}\n")
    
    # 2. Primera respuesta
    print("2. Candidato responde primera pregunta...")
    response = requests.post(
        f"{BASE_URL}/api/candidato/chatbot/siguiente",
        json={
            "aplicacion_id": "test-456",
            "respuesta_anterior": "Tengo 5 años con Python, principalmente Django y Flask",
            "preguntas_restantes": [
                "¿Conoces FastAPI?",
                "¿Has trabajado con bases de datos?"
            ]
        }
    )
    
    data = response.json()
    print(f"Chatbot: {data['mensaje']}\n")
    
    # 3. Segunda respuesta
    print("3. Candidato responde segunda pregunta...")
    response = requests.post(
        f"{BASE_URL}/api/candidato/chatbot/siguiente",
        json={
            "aplicacion_id": "test-456",
            "respuesta_anterior": "Sí, he usado FastAPI en 3 proyectos recientes",
            "preguntas_restantes": [
                "¿Has trabajado con bases de datos?"
            ]
        }
    )
    
    data = response.json()
    print(f"Chatbot: {data['mensaje']}\n")
    
    # 4. Última respuesta
    print("4. Candidato responde última pregunta...")
    response = requests.post(
        f"{BASE_URL}/api/candidato/chatbot/siguiente",
        json={
            "aplicacion_id": "test-456",
            "respuesta_anterior": "Sí, PostgreSQL, MongoDB y Redis",
            "preguntas_restantes": []
        }
    )
    
    data = response.json()
    print(f"Chatbot: {data['mensaje']}\n")
    
    # 5. Finalizar
    print("5. Finalizando conversación...")
    response = requests.post(
        f"{BASE_URL}/api/candidato/chatbot/finalizar",
        json={
            "aplicacion_id": "test-456"
        }
    )
    
    data = response.json()
    print(f"Chatbot: {data['mensaje']}\n")
    print("✅ Conversación completada!")

if __name__ == "__main__":
    chatbot_flow_example()
```

## 🎭 Ejemplo con JavaScript/TypeScript

```typescript
// chatbot-service.ts
const BASE_URL = 'http://localhost:8000';

interface ChatbotResponse {
  mensaje: string;
  quedan_preguntas?: boolean;
  preguntas_restantes?: number;
  finalizado?: boolean;
}

class ChatbotClient {
  async iniciarConversacion(
    aplicacionId: string,
    candidatoNombre: string,
    vacanteTitulo: string,
    preguntas: string[]
  ): Promise<ChatbotResponse> {
    const response = await fetch(`${BASE_URL}/api/candidato/chatbot/iniciar`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        aplicacion_id: aplicacionId,
        candidato_nombre: candidatoNombre,
        vacante_titulo: vacanteTitulo,
        preguntas
      })
    });
    
    return response.json();
  }
  
  async siguientePregunta(
    aplicacionId: string,
    respuestaAnterior: string,
    preguntasRestantes: string[]
  ): Promise<ChatbotResponse> {
    const response = await fetch(`${BASE_URL}/api/candidato/chatbot/siguiente`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        aplicacion_id: aplicacionId,
        respuesta_anterior: respuestaAnterior,
        preguntas_restantes: preguntasRestantes
      })
    });
    
    return response.json();
  }
  
  async finalizarConversacion(aplicacionId: string): Promise<ChatbotResponse> {
    const response = await fetch(`${BASE_URL}/api/candidato/chatbot/finalizar`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ aplicacion_id: aplicacionId })
    });
    
    return response.json();
  }
}

// Uso
async function ejemploUso() {
  const chatbot = new ChatbotClient();
  
  // Iniciar
  const inicio = await chatbot.iniciarConversacion(
    'app-789',
    'Ana López',
    'Frontend Developer',
    ['¿Experiencia con React?', '¿Conoces TypeScript?']
  );
  
  console.log('Chatbot:', inicio.mensaje);
  
  // Siguiente
  const siguiente = await chatbot.siguientePregunta(
    'app-789',
    'Tengo 3 años con React',
    ['¿Conoces TypeScript?']
  );
  
  console.log('Chatbot:', siguiente.mensaje);
  
  // Finalizar
  const fin = await chatbot.finalizarConversacion('app-789');
  console.log('Chatbot:', fin.mensaje);
}
```

## 🔄 Flujo en React Component

```tsx
// ChatbotInterview.tsx
import { useState, useEffect } from 'react';

interface Message {
  role: 'chatbot' | 'candidate';
  content: string;
}

export function ChatbotInterview({ aplicacionId, candidatoNombre, vacanteTitulo, preguntas }) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [currentAnswer, setCurrentAnswer] = useState('');
  const [preguntasRestantes, setPreguntasRestantes] = useState(preguntas);
  const [isFinished, setIsFinished] = useState(false);
  
  // Iniciar conversación
  useEffect(() => {
    async function iniciar() {
      const response = await fetch('/api/candidato/chatbot/iniciar', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          aplicacion_id: aplicacionId,
          candidato_nombre: candidatoNombre,
          vacante_titulo: vacanteTitulo,
          preguntas
        })
      });
      
      const data = await response.json();
      setMessages([{ role: 'chatbot', content: data.mensaje }]);
    }
    
    iniciar();
  }, []);
  
  // Enviar respuesta
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    // Agregar respuesta del candidato
    setMessages(prev => [...prev, { role: 'candidate', content: currentAnswer }]);
    
    // Obtener siguiente pregunta
    const response = await fetch('/api/candidato/chatbot/siguiente', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        aplicacion_id: aplicacionId,
        respuesta_anterior: currentAnswer,
        preguntas_restantes: preguntasRestantes.slice(1)
      })
    });
    
    const data = await response.json();
    
    // Agregar respuesta del chatbot
    setMessages(prev => [...prev, { role: 'chatbot', content: data.mensaje }]);
    
    // Actualizar estado
    setPreguntasRestantes(prev => prev.slice(1));
    setCurrentAnswer('');
    
    if (!data.quedan_preguntas) {
      setIsFinished(true);
    }
  };
  
  return (
    <div className="chatbot-container">
      <div className="messages">
        {messages.map((msg, idx) => (
          <div key={idx} className={`message ${msg.role}`}>
            <strong>{msg.role === 'chatbot' ? 'Alex' : candidatoNombre}:</strong>
            <p>{msg.content}</p>
          </div>
        ))}
      </div>
      
      {!isFinished && (
        <form onSubmit={handleSubmit}>
          <textarea
            value={currentAnswer}
            onChange={(e) => setCurrentAnswer(e.target.value)}
            placeholder="Escribe tu respuesta..."
            required
          />
          <button type="submit">Enviar</button>
        </form>
      )}
      
      {isFinished && (
        <div className="finished">
          <p>¡Entrevista completada! Gracias por tu tiempo.</p>
        </div>
      )}
    </div>
  );
}
```

## 💡 Tips de Uso

### 1. Manejo de Memoria
```python
# Limpiar memoria si el candidato abandona
requests.delete(f"{BASE_URL}/api/candidato/chatbot/limpiar/{aplicacion_id}")
```

### 2. Múltiples Conversaciones
El chatbot puede manejar múltiples conversaciones simultáneas usando `aplicacion_id` único para cada una.

### 3. Personalización
El chatbot se adapta al nombre del candidato y título de la vacante para una experiencia personalizada.

### 4. Tono Natural
El chatbot mantiene un tono profesional pero cálido, evitando respuestas robóticas.

## 🎯 Características del Chatbot

- ✅ **Memoria conversacional**: Recuerda el contexto
- ✅ **Respuestas naturales**: No robóticas
- ✅ **Agradecimientos**: Reconoce cada respuesta
- ✅ **Transiciones suaves**: Flujo natural entre preguntas
- ✅ **Cierre profesional**: Despedida motivadora
- ✅ **Múltiples sesiones**: Maneja varias conversaciones
- ✅ **Limpieza automática**: Libera memoria al finalizar

## 📊 Ventajas vs Chatbot Tradicional

| Aspecto | Tradicional | Con LangChain |
|---------|-------------|---------------|
| Memoria | ❌ Sin contexto | ✅ Contexto completo |
| Naturalidad | ❌ Robótico | ✅ Conversacional |
| Personalización | ❌ Genérico | ✅ Personalizado |
| Flexibilidad | ❌ Rígido | ✅ Adaptable |
| Experiencia | ⭐⭐ | ⭐⭐⭐⭐⭐ |

---

**¡El chatbot está listo para crear experiencias de entrevista excepcionales! 🚀**
