# 🔍 Análisis de Discrepancias con Base de Datos

## ❌ Problemas Encontrados

### 1. Tabla `usuarios`
**Columna incorrecta en código:**
- ❌ `fecha_registro` (no existe en BD)
- ✅ Debe ser: `created_at` (existe en BD)

### 2. Tabla `empresas`
**Columnas incorrectas en código:**
- ❌ `email` (no existe en BD)
- ❌ `fecha_registro` (no existe en BD)
- ✅ Debe usar: `created_at` (existe en BD)

**Columnas faltantes en código:**
- `sitio_web`
- `logo_url`
- `direccion`
- `updated_at`

### 3. Tabla `vacantes`
**Columnas incorrectas en código:**
- ❌ `fecha_creacion` (no existe en BD)
- ✅ Debe ser: `created_at` (existe en BD)

**Columnas faltantes en código:**
- `numero_vacantes`
- `beneficios`
- `updated_at`

### 4. Tabla `aplicaciones`
**Columna incorrecta en código:**
- ❌ `fecha_aplicacion` (probablemente debe ser `created_at`)

## ✅ Correcciones Necesarias

### routes/empresas.py
1. Línea ~28: Cambiar `fecha_registro` → `created_at`
2. Línea ~48: Eliminar campo `email` (no existe en tabla empresas)
3. Línea ~49: Cambiar `fecha_registro` → `created_at`
4. Línea ~103: Cambiar `fecha_creacion` → `created_at`
5. Línea ~127: Cambiar `fecha_creacion` → `created_at`

### models/empresa.py
1. Eliminar campo `email` de `EmpresaDetalle`
2. Cambiar `fecha_registro` → `created_at`

### models/vacante.py
- No requiere cambios (los modelos Pydantic están bien)

### models/candidato.py
- Cambiar `fecha_aplicacion` → `created_at` en `AplicacionDetalle`
