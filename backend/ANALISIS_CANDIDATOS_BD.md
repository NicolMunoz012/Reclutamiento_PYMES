# 🔍 Análisis de Discrepancias - Endpoints de Candidatos

## ❌ Problemas Encontrados

### 1. Tabla `usuarios` (línea 73)
**Problema:** Usa `fecha_registro` (no existe)
**Solución:** Eliminar - `created_at` se genera automáticamente

### 2. Tabla `candidatos` (líneas 78-92)
**Problemas:**
- ❌ Usa `usuario_id` (no existe en tabla candidatos)
- ❌ Usa `email` (no existe en tabla candidatos)
- ❌ Usa `telefono` (no existe en tabla candidatos)
- ❌ Usa `años_experiencia` (debe ser `experiencia_años`)
- ❌ Usa `resumen_profesional` (no existe)
- ❌ Usa `fecha_registro` (no existe)

**Columnas correctas según BD:**
```sql
id text PRIMARY KEY
nombre_anonimo text
cargo_deseado text
experiencia_años int  ✅
habilidades jsonb
educacion text
disponibilidad text
pretension_salarial text
ciudad text
created_at timestamptz DEFAULT now()
```

### 3. Tabla `documentos` (líneas 106-115)
**Problemas:**
- ❌ Usa `fecha_subida` (no existe)
- ✅ Debe usar `created_at` (automático)
- ❌ Falta campo `tamaño_kb`
- ❌ Falta campo `mime_type`

### 4. Tabla `aplicaciones` (líneas 118-125)
**Problemas:**
- ❌ Usa `fecha_aplicacion` (no existe)
- ✅ Debe usar `created_at` o el campo correcto `fecha_aplicacion` (verificar)

**Nota:** La tabla tiene TRES campos de fecha:
- `fecha_aplicacion` (timestamptz DEFAULT now())
- `fecha_ultima_actualizacion` (timestamptz DEFAULT now())
- `updated_at` (timestamptz DEFAULT now())

### 5. Tabla `respuestas_candidato` (líneas 195-203)
**Problema:** Usa `fecha_respuesta` (no existe)
**Solución:** Eliminar - `created_at` se genera automáticamente

### 6. ID de Candidato
**Problema:** Genera UUID pero debe ser TEXT con formato específico
**Formato correcto:** `CAND_001`, `CAND_002`, etc. (no UUID)
**Solución:** Generar ID secuencial o usar formato específico

## ✅ Correcciones Necesarias

### Endpoint: POST /api/candidato/aplicar

1. **Línea 73:** Eliminar `fecha_registro` de usuarios
2. **Líneas 78-92:** Corregir estructura de candidatos:
   - Eliminar `usuario_id`, `email`, `telefono`
   - Cambiar `años_experiencia` → `experiencia_años`
   - Eliminar `resumen_profesional`
   - Eliminar `fecha_registro`
3. **Línea 77:** Generar ID correcto (TEXT, no UUID)
4. **Líneas 106-115:** Corregir documentos:
   - Eliminar `fecha_subida`
   - Agregar `tamaño_kb` y `mime_type`
5. **Líneas 118-125:** Verificar campo de fecha en aplicaciones

### Endpoint: POST /api/candidato/responder

1. **Línea 203:** Eliminar `fecha_respuesta`
2. Verificar que `created_at` se use automáticamente
