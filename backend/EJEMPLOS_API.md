# Ejemplos de Uso de la API

Ejemplos completos para probar todos los endpoints del sistema.

## 🔧 Configuración Inicial

Base URL: `http://localhost:8000`

## 📝 Ejemplos con cURL

### 1. Registrar Empresa

```bash
curl -X POST http://localhost:8000/api/empresa/registrar \
  -H "Content-Type: application/json" \
  -d '{
    "nombre_empresa": "TechCorp Solutions",
    "nit": "900123456-1",
    "industria": "Tecnología",
    "tamaño_empresa": "51-200",
    "descripcion": "Empresa líder en desarrollo de software",
    "ciudad": "Bogotá",
    "email": "rrhh@techcorp.co"
  }'
```

**Respuesta esperada:**
```json
{
  "empresa_id": "550e8400-e29b-41d4-a716-446655440000",
  "mensaje": "Empresa registrada exitosamente"
}
```

### 2. Crear Vacante

```bash
curl -X POST http://localhost:8000/api/empresa/crear-vacante \
  -H "Content-Type: application/json" \
  -d '{
    "empresa_id": "550e8400-e29b-41d4-a716-446655440000",
    "titulo": "Desarrollador Full Stack Senior",
    "descripcion": "Buscamos un desarrollador full stack con experiencia en React y Node.js para unirse a nuestro equipo de innovación.",
    "cargo": "Desarrollador Full Stack",
    "tipo_contrato": "Tiempo completo",
    "modalidad": "Híbrido",
    "habilidades_requeridas": ["React", "Node.js", "PostgreSQL", "Docker"],
    "experiencia_min": 3,
    "experiencia_max": 6,
    "salario_min": 5000000,
    "salario_max": 8000000,
    "ciudad": "Bogotá"
  }'
```

**Respuesta esperada:**
```json
{
  "vacante_id": "660e8400-e29b-41d4-a716-446655440001",
  "preguntas_sugeridas": [
    {
      "pregunta": "¿Puedes describir tu experiencia trabajando con React y Node.js?",
      "tipo_pregunta": "abierta"
    },
    {
      "pregunta": "¿Has trabajado con PostgreSQL en proyectos de producción?",
      "tipo_pregunta": "si_no"
    },
    {
      "pregunta": "¿Tienes experiencia con Docker y contenedores?",
      "tipo_pregunta": "si_no"
    }
  ]
}
```

### 3. Aprobar Preguntas y Publicar Vacante

```bash
curl -X POST http://localhost:8000/api/empresa/aprobar-preguntas \
  -H "Content-Type: application/json" \
  -d '{
    "vacante_id": "660e8400-e29b-41d4-a716-446655440001",
    "preguntas_aprobadas": [
      {
        "pregunta_id": "770e8400-e29b-41d4-a716-446655440002",
        "aprobada": true
      },
      {
        "pregunta_id": "770e8400-e29b-41d4-a716-446655440003",
        "aprobada": true
      },
      {
        "pregunta_id": "770e8400-e29b-41d4-a716-446655440004",
        "aprobada": false
      }
    ]
  }'
```

### 4. Obtener Vacantes Publicadas

```bash
# Todas las vacantes
curl http://localhost:8000/api/vacantes/publicadas

# Filtrar por ciudad
curl "http://localhost:8000/api/vacantes/publicadas?ciudad=Bogotá"

# Filtrar por modalidad
curl "http://localhost:8000/api/vacantes/publicadas?modalidad=Híbrido"

# Múltiples filtros
curl "http://localhost:8000/api/vacantes/publicadas?ciudad=Bogotá&modalidad=Remoto"
```

### 5. Obtener Detalles de Vacante

```bash
curl http://localhost:8000/api/vacantes/660e8400-e29b-41d4-a716-446655440001/detalles
```

### 6. Aplicar a Vacante (con CV)

```bash
curl -X POST http://localhost:8000/api/candidato/aplicar \
  -F "vacante_id=660e8400-e29b-41d4-a716-446655440001" \
  -F "nombre_anonimo=Candidato 51" \
  -F "email=candidato51@example.com" \
  -F "telefono=+57 300 123 4567" \
  -F "ciudad=Bogotá" \
  -F "años_experiencia=4" \
  -F "cv_pdf=@/ruta/a/tu/cv.pdf"
```

**Respuesta esperada:**
```json
{
  "candidato_id": "CAND_A1B2C3D4",
  "aplicacion_id": "880e8400-e29b-41d4-a716-446655440005",
  "preguntas": [
    {
      "pregunta_id": "770e8400-e29b-41d4-a716-446655440002",
      "pregunta": "¿Puedes describir tu experiencia trabajando con React y Node.js?",
      "tipo_pregunta": "abierta"
    }
  ]
}
```

### 7. Responder Preguntas

```bash
curl -X POST http://localhost:8000/api/candidato/responder \
  -H "Content-Type: application/json" \
  -d '{
    "aplicacion_id": "880e8400-e29b-41d4-a716-446655440005",
    "respuestas": [
      {
        "pregunta_id": "770e8400-e29b-41d4-a716-446655440002",
        "respuesta": "Tengo 4 años de experiencia trabajando con React en el frontend y Node.js en el backend. He desarrollado aplicaciones completas usando el stack MERN."
      },
      {
        "pregunta_id": "770e8400-e29b-41d4-a716-446655440003",
        "respuesta": "Sí, he trabajado con PostgreSQL en varios proyectos de producción, incluyendo diseño de esquemas, optimización de queries y migraciones."
      }
    ]
  }'
```

**Respuesta esperada:**
```json
{
  "mensaje": "Aplicación enviada exitosamente",
  "puntuacion_ia": 85,
  "compatibilidad_porcentaje": 78,
  "email_enviado": true
}
```

### 8. Obtener Aplicaciones de Empresa

```bash
curl http://localhost:8000/api/empresa/550e8400-e29b-41d4-a716-446655440000/aplicaciones
```

## 🐍 Ejemplos con Python

### Script Completo de Prueba

```python
import requests
import json

BASE_URL = "http://localhost:8000"

def test_flujo_completo():
    """Prueba el flujo completo del sistema"""
    
    # 1. Registrar empresa
    print("1. Registrando empresa...")
    empresa_data = {
        "nombre_empresa": "TechCorp Solutions",
        "nit": "900123456-1",
        "industria": "Tecnología",
        "tamaño_empresa": "51-200",
        "descripcion": "Empresa líder en desarrollo de software",
        "ciudad": "Bogotá",
        "email": "rrhh@techcorp.co"
    }
    
    response = requests.post(f"{BASE_URL}/api/empresa/registrar", json=empresa_data)
    empresa_result = response.json()
    empresa_id = empresa_result["empresa_id"]
    print(f"✓ Empresa registrada: {empresa_id}")
    
    # 2. Crear vacante
    print("\n2. Creando vacante...")
    vacante_data = {
        "empresa_id": empresa_id,
        "titulo": "Desarrollador Full Stack Senior",
        "descripcion": "Buscamos desarrollador con experiencia en React y Node.js",
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
    
    response = requests.post(f"{BASE_URL}/api/empresa/crear-vacante", json=vacante_data)
    vacante_result = response.json()
    vacante_id = vacante_result["vacante_id"]
    preguntas = vacante_result["preguntas_sugeridas"]
    print(f"✓ Vacante creada: {vacante_id}")
    print(f"✓ Preguntas generadas: {len(preguntas)}")
    
    # 3. Aprobar preguntas
    print("\n3. Aprobando preguntas...")
    # Nota: En este ejemplo necesitarías los IDs reales de las preguntas
    # que se guardaron en la base de datos
    
    # 4. Obtener vacantes publicadas
    print("\n4. Obteniendo vacantes publicadas...")
    response = requests.get(f"{BASE_URL}/api/vacantes/publicadas")
    vacantes = response.json()
    print(f"✓ Vacantes encontradas: {len(vacantes['vacantes'])}")
    
    # 5. Obtener detalles de vacante
    print(f"\n5. Obteniendo detalles de vacante {vacante_id}...")
    response = requests.get(f"{BASE_URL}/api/vacantes/{vacante_id}/detalles")
    detalle = response.json()
    print(f"✓ Título: {detalle['vacante']['titulo']}")
    
    print("\n✅ Flujo de prueba completado!")

if __name__ == "__main__":
    test_flujo_completo()
```

### Aplicar con CV (Python)

```python
import requests

def aplicar_con_cv(vacante_id, cv_path):
    """Aplicar a una vacante con CV"""
    
    url = "http://localhost:8000/api/candidato/aplicar"
    
    # Datos del formulario
    data = {
        "vacante_id": vacante_id,
        "nombre_anonimo": "Candidato 51",
        "email": "candidato51@example.com",
        "telefono": "+57 300 123 4567",
        "ciudad": "Bogotá",
        "años_experiencia": 4
    }
    
    # Archivo PDF
    files = {
        "cv_pdf": open(cv_path, "rb")
    }
    
    response = requests.post(url, data=data, files=files)
    result = response.json()
    
    print(f"Candidato ID: {result['candidato_id']}")
    print(f"Aplicación ID: {result['aplicacion_id']}")
    print(f"Preguntas a responder: {len(result['preguntas'])}")
    
    return result

# Uso
resultado = aplicar_con_cv(
    vacante_id="660e8400-e29b-41d4-a716-446655440001",
    cv_path="mi_cv.pdf"
)
```

## 🧪 Postman Collection

### Importar en Postman

Crea una nueva colección en Postman con estos endpoints:

**Variables de colección:**
- `base_url`: `http://localhost:8000`
- `empresa_id`: (se actualiza después de registrar)
- `vacante_id`: (se actualiza después de crear vacante)
- `aplicacion_id`: (se actualiza después de aplicar)

### Endpoints para Postman

1. **Registrar Empresa**
   - Method: POST
   - URL: `{{base_url}}/api/empresa/registrar`
   - Body: raw JSON (ver ejemplo arriba)

2. **Crear Vacante**
   - Method: POST
   - URL: `{{base_url}}/api/empresa/crear-vacante`
   - Body: raw JSON

3. **Aprobar Preguntas**
   - Method: POST
   - URL: `{{base_url}}/api/empresa/aprobar-preguntas`
   - Body: raw JSON

4. **Vacantes Publicadas**
   - Method: GET
   - URL: `{{base_url}}/api/vacantes/publicadas`

5. **Aplicar a Vacante**
   - Method: POST
   - URL: `{{base_url}}/api/candidato/aplicar`
   - Body: form-data (incluir archivo PDF)

6. **Responder Preguntas**
   - Method: POST
   - URL: `{{base_url}}/api/candidato/responder`
   - Body: raw JSON

## 🔍 Verificar Respuestas

### Health Check

```bash
curl http://localhost:8000/health
```

Respuesta esperada:
```json
{
  "status": "healthy",
  "environment": "development"
}
```

### Documentación Interactiva

Abre en tu navegador:
- Swagger: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

Desde ahí puedes probar todos los endpoints interactivamente.

## 💡 Tips

1. **Guarda los IDs**: Después de cada operación, guarda los IDs retornados para usarlos en las siguientes llamadas
2. **Verifica en Supabase**: Puedes verificar que los datos se guardaron correctamente en el dashboard de Supabase
3. **Revisa los logs**: El servidor imprime logs útiles en la consola
4. **Usa Swagger**: La interfaz de Swagger en `/docs` es la forma más fácil de probar

## ⚠️ Errores Comunes

### 404 Not Found
- Verifica que el ID existe en la base de datos
- Verifica que estás usando el ID correcto

### 500 Internal Server Error
- Revisa los logs del servidor
- Verifica que las credenciales están configuradas
- Verifica que Supabase está accesible

### Email no enviado
- No es un error crítico, el sistema funciona sin emails
- Configura SMTP si necesitas emails de confirmación
