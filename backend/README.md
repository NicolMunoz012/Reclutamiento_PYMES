# Sistema de Reclutamiento Inteligente - Backend

Backend API construido con FastAPI para sistema de reclutamiento con IA para SMEs.

## 🚀 Stack Tecnológico

- **Framework**: FastAPI (Python 3.10+)
- **Base de datos**: Supabase (PostgreSQL)
- **IA**: Anthropic Claude API (Claude Sonnet 4)
- **Storage**: Supabase Storage
- **Email**: Gmail SMTP
- **PDF Processing**: PyPDF2

## 📋 Requisitos Previos

- Python 3.10 o superior
- Cuenta de Supabase con base de datos configurada
- API Key de Anthropic Claude
- Cuenta de Gmail con App Password (para emails)

## 🔧 Instalación

### 1. Clonar el repositorio y navegar al backend

```bash
cd backend
```

### 2. Crear entorno virtual

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r ../requirements.txt
```

### 4. Configurar variables de entorno

Copia el archivo `.env.example` a `.env`:

```bash
copy .env.example .env  # Windows
cp .env.example .env    # Linux/Mac
```

Edita el archivo `.env` con tus credenciales:

```env
# Supabase
SUPABASE_URL=https://tu-proyecto.supabase.co
SUPABASE_SERVICE_KEY=tu-service-role-key

# Claude API
ANTHROPIC_API_KEY=tu-api-key

# Email
SMTP_USER=tu-email@gmail.com
SMTP_PASSWORD=tu-app-password
EMAIL_FROM=tu-email@gmail.com
```

#### Dónde obtener las credenciales:

**Supabase:**
1. Ve a https://supabase.com/dashboard
2. Selecciona tu proyecto
3. Settings → API
4. Copia `URL` y `service_role key`

**Anthropic Claude:**
1. Ve a https://console.anthropic.com
2. Settings → API Keys
3. Crea una nueva API key

**Gmail App Password:**
1. Ve a https://myaccount.google.com/apppasswords
2. Genera una contraseña de aplicación
3. Usa esa contraseña en `SMTP_PASSWORD`

## ▶️ Ejecutar el servidor

### Modo desarrollo (con auto-reload)

```bash
python main.py
```

O usando uvicorn directamente:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

El servidor estará disponible en: http://localhost:8000

## 📚 Documentación API

Una vez el servidor esté corriendo:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🤖 Integración con LangChain

Este proyecto usa **LangChain** como framework principal para todas las interacciones con IA.

### Arquitectura LangChain

```
Frontend → FastAPI → LangChain → Claude API
                         ↓
              Conversation Memory
```

### Funcionalidades Implementadas

#### 1. **Generación de Preguntas Inteligentes**
- Usa `ChatPromptTemplate` con prompts estructurados
- Genera 5-7 preguntas contextualizadas por vacante
- Tipos: abierta, si_no, escala

#### 2. **Análisis de CVs**
- Extrae información estructurada de PDFs
- Identifica habilidades, experiencia, educación
- Genera resumen profesional automático

#### 3. **Evaluación de Compatibilidad**
- Analiza respuestas vs requisitos
- Calcula puntuación (0-100) y compatibilidad (%)
- Identifica fortalezas y áreas de mejora

#### 4. **Chatbot Conversacional** 🆕
- Mantiene memoria con `ConversationBufferMemory`
- Interacción natural y fluida
- Múltiples conversaciones simultáneas
- Tono profesional y empático

### Ventajas de LangChain

- ✅ Mejor gestión de prompts
- ✅ Memoria conversacional
- ✅ Composición de cadenas
- ✅ Framework industry-standard
- ✅ Fácil extensibilidad

Ver [MIGRATION.md](MIGRATION.md) para detalles de la implementación.

## 🔌 Endpoints Disponibles

### Empresas

#### POST `/api/empresa/registrar`
Registrar una nueva empresa

```json
{
  "nombre_empresa": "TechCorp",
  "nit": "900123456-1",
  "industria": "Tecnología",
  "tamaño_empresa": "51-200",
  "descripcion": "Empresa de desarrollo de software",
  "ciudad": "Bogotá",
  "email": "contacto@techcorp.co"
}
```

#### POST `/api/empresa/crear-vacante`
Crear vacante y generar preguntas con IA

```json
{
  "empresa_id": "uuid",
  "titulo": "Desarrollador Full Stack Senior",
  "descripcion": "Buscamos desarrollador con experiencia...",
  "cargo": "Desarrollador Full Stack",
  "tipo_contrato": "Tiempo completo",
  "modalidad": "Híbrido",
  "habilidades_requeridas": ["React", "Node.js", "PostgreSQL"],
  "experiencia_min": 3,
  "experiencia_max": 6,
  "salario_min": 5000000,
  "salario_max": 8000000,
  "ciudad": "Bogotá"
}
```

#### POST `/api/empresa/aprobar-preguntas`
Aprobar preguntas y publicar vacante

```json
{
  "vacante_id": "uuid",
  "preguntas_aprobadas": [
    {
      "pregunta_id": "uuid",
      "aprobada": true
    }
  ]
}
```

#### GET `/api/empresa/{empresa_id}/aplicaciones`
Obtener todas las aplicaciones de la empresa

### Candidatos

#### POST `/api/candidato/aplicar`
Aplicar a una vacante (multipart/form-data)

```
vacante_id: uuid
nombre_anonimo: Candidato 51
email: candidato@example.com
telefono: +57 300 123 4567
ciudad: Bogotá
años_experiencia: 4
cv_pdf: [archivo PDF]
```

#### POST `/api/candidato/responder`
Responder preguntas de la vacante

```json
{
  "aplicacion_id": "uuid",
  "respuestas": [
    {
      "pregunta_id": "uuid",
      "respuesta": "Tengo 4 años de experiencia con React..."
    }
  ]
}
```

#### POST `/api/candidato/chatbot/iniciar` 🆕
Iniciar conversación con chatbot

```json
{
  "aplicacion_id": "uuid",
  "candidato_nombre": "Juan Pérez",
  "vacante_titulo": "Desarrollador Full Stack",
  "preguntas": ["¿Experiencia con React?", "¿Trabajo en equipo?"]
}
```

#### POST `/api/candidato/chatbot/siguiente` 🆕
Obtener siguiente pregunta del chatbot

```json
{
  "aplicacion_id": "uuid",
  "respuesta_anterior": "Tengo 3 años con React...",
  "preguntas_restantes": ["¿Trabajo en equipo?"]
}
```

#### POST `/api/candidato/chatbot/finalizar` 🆕
Finalizar conversación del chatbot

```json
{
  "aplicacion_id": "uuid"
}
```

### Vacantes

#### GET `/api/vacantes/publicadas`
Obtener vacantes publicadas (con filtros opcionales)

Query params:
- `ciudad`: Filtrar por ciudad
- `cargo`: Filtrar por cargo
- `modalidad`: Filtrar por modalidad

#### GET `/api/vacantes/{vacante_id}/detalles`
Obtener detalles de una vacante específica

## 🧪 Probar los Endpoints

### Usando cURL

```bash
# Registrar empresa
curl -X POST http://localhost:8000/api/empresa/registrar \
  -H "Content-Type: application/json" \
  -d '{
    "nombre_empresa": "TechCorp",
    "nit": "900123456-1",
    "industria": "Tecnología",
    "tamaño_empresa": "51-200",
    "ciudad": "Bogotá",
    "email": "contacto@techcorp.co"
  }'

# Obtener vacantes publicadas
curl http://localhost:8000/api/vacantes/publicadas

# Obtener vacantes por ciudad
curl "http://localhost:8000/api/vacantes/publicadas?ciudad=Bogotá"
```

### Usando Python requests

```python
import requests

# Registrar empresa
response = requests.post(
    "http://localhost:8000/api/empresa/registrar",
    json={
        "nombre_empresa": "TechCorp",
        "nit": "900123456-1",
        "industria": "Tecnología",
        "tamaño_empresa": "51-200",
        "ciudad": "Bogotá",
        "email": "contacto@techcorp.co"
    }
)
print(response.json())
```

## 📁 Estructura del Proyecto

```
backend/
├── main.py                 # FastAPI app principal
├── config.py               # Configuración y variables de entorno
├── database.py             # Cliente Supabase
├── models/
│   ├── empresa.py          # Modelos Pydantic para empresas
│   ├── vacante.py          # Modelos Pydantic para vacantes
│   └── candidato.py        # Modelos Pydantic para candidatos
├── services/
│   ├── ia_service.py       # Integración con Claude API
│   ├── pdf_service.py      # Extracción de texto de PDFs
│   ├── email_service.py    # Envío de emails
│   └── storage_service.py  # Subida de archivos a Supabase
├── routes/
│   ├── empresas.py         # Endpoints de empresas
│   ├── candidatos.py       # Endpoints de candidatos
│   └── vacantes.py         # Endpoints de vacantes
├── requirements.txt        # Dependencias Python
├── .env.example            # Ejemplo de variables de entorno
└── README.md               # Este archivo
```

## 🔍 Flujo Completo del Sistema

### Flujo Empresa:
1. Empresa se registra → `POST /api/empresa/registrar`
2. Empresa crea vacante → `POST /api/empresa/crear-vacante`
3. IA genera preguntas automáticamente
4. Empresa aprueba preguntas → `POST /api/empresa/aprobar-preguntas`
5. Vacante se publica
6. Empresa revisa aplicaciones → `GET /api/empresa/{id}/aplicaciones`

### Flujo Candidato:
1. Candidato ve vacantes → `GET /api/vacantes/publicadas`
2. Candidato ve detalles → `GET /api/vacantes/{id}/detalles`
3. Candidato aplica con CV → `POST /api/candidato/aplicar`
4. Sistema extrae texto del CV y analiza con IA
5. Candidato responde preguntas → `POST /api/candidato/responder`
6. IA evalúa compatibilidad
7. Sistema envía email de confirmación

## 🤖 Funciones de IA

### 1. Generación de Preguntas
- Input: Descripción de vacante, habilidades, experiencia
- Output: 5-7 preguntas inteligentes
- Modelo: Claude Sonnet 4

### 2. Análisis de CV
- Input: Texto extraído del PDF
- Output: Habilidades, experiencia, educación, resumen
- Modelo: Claude Sonnet 4

### 3. Evaluación de Compatibilidad
- Input: CV + Respuestas + Requisitos de vacante
- Output: Puntuación (0-100), compatibilidad (%), fortalezas, debilidades
- Modelo: Claude Sonnet 4

## ⚠️ Notas Importantes

- Este backend está configurado para un hackathon (sin autenticación JWT completa)
- Se usa `service_role_key` de Supabase directamente
- En producción, implementar autenticación JWT y RLS apropiado
- Los emails requieren configuración de Gmail App Password
- El bucket de Supabase Storage debe llamarse `cvs` y estar público

## 🐛 Troubleshooting

### Error: "Supabase credentials not configured"
- Verifica que `.env` existe y tiene `SUPABASE_URL` y `SUPABASE_SERVICE_KEY`

### Error: "Anthropic API key not configured"
- Verifica que `.env` tiene `ANTHROPIC_API_KEY`

### Error al subir archivos
- Verifica que el bucket `cvs` existe en Supabase Storage
- Verifica que el bucket tiene permisos públicos

### Emails no se envían
- Verifica credenciales SMTP en `.env`
- Usa App Password de Gmail, no tu contraseña normal
- Verifica que 2FA está habilitado en tu cuenta de Gmail

## 📞 Soporte

Para problemas o preguntas sobre el backend, revisa:
1. Logs del servidor en la consola
2. Documentación de Swagger en `/docs`
3. Verifica que todas las credenciales están configuradas

## ✅ Checklist de Configuración

- [ ] Python 3.10+ instalado
- [ ] Dependencias instaladas (`pip install -r ../requirements.txt`)
- [ ] Archivo `.env` creado con todas las credenciales
- [ ] Supabase URL y Service Key configurados
- [ ] Anthropic API Key configurada
- [ ] Gmail SMTP configurado (opcional para emails)
- [ ] Bucket `cvs` creado en Supabase Storage
- [ ] Servidor corriendo en http://localhost:8000
- [ ] Swagger docs accesibles en http://localhost:8000/docs

¡Listo para el hackathon! 🚀
