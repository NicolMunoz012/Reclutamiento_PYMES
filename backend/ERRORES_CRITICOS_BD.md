# 🚨 ERRORES CRÍTICOS ENCONTRADOS - Estructura Real de BD

## ❌ DISCREPANCIAS GRAVES

### 1. Tabla `respuestas_candidato` NO EXISTE
**Error en mis correcciones:** Asumí que existía la tabla `respuestas_candidato`
**Realidad:** NO EXISTE - En su lugar existe la tabla `evaluaciones`

### 2. Tabla `documentos` - candidato_id es BIGINT, no TEXT
**Error en mis correcciones:** Dije que `candidato_id` era TEXT
**Realidad:** `candidato_id` es **BIGINT**, no TEXT

### 3. Tabla `candidatos` - ID puede ser diferente
**Error en mis correcciones:** Asumí que el ID era TEXT con formato CAND_XXX
**Realidad:** Necesito verificar si realmente es TEXT o si es BIGINT

## 📊 Estructura Real Confirmada

### Tabla: `usuarios` ✅ CORRECTO
```sql
id uuid PRIMARY KEY DEFAULT gen_random_uuid()
email text NOT NULL
tipo_usuario text NOT NULL
nombre_completo text NULL
telefono text NULL
created_at timestamptz DEFAULT now()
updated_at timestamptz DEFAULT now()
```

### Tabla: `vacante_preguntas` ✅ CORRECTO
```sql
id uuid PRIMARY KEY DEFAULT gen_random_uuid()
vacante_id uuid NULL  -- ⚠️ Puede ser NULL (inusual)
pregunta text NOT NULL
tipo_pregunta text NULL
opciones jsonb NULL
es_obligatoria boolean DEFAULT true
orden integer NULL
generada_por_ia boolean DEFAULT true
aprobada_por_empresa boolean DEFAULT false
created_at timestamptz DEFAULT now()
```

### Tabla: `evaluaciones` (NO respuestas_candidato) ❌ ERROR GRAVE
```sql
id integer PRIMARY KEY AUTOINCREMENT
entrevista_id integer NULL
puntaje_general integer NULL
fortalezas jsonb NULL
debilidades jsonb NULL
recomendacion text NULL
created_at timestamptz DEFAULT now()
evaluador_nombre text NULL
aspectos_positivos jsonb NULL
aspectos_negativos jsonb NULL
decision_final text NULL
```

**⚠️ IMPORTANTE:** Esta tabla tiene estructura COMPLETAMENTE DIFERENTE a lo que asumí

### Tabla: `documentos` ❌ ERROR EN candidato_id
```sql
id uuid PRIMARY KEY DEFAULT gen_random_uuid()
candidato_id bigint NULL  -- ❌ Es BIGINT, no TEXT
nombre_archivo text NOT NULL
tipo_documento text NULL
url_archivo text NOT NULL
tamaño_kb integer NULL
mime_type text NULL
texto_extraido text NULL
created_at timestamptz DEFAULT now()
```

## 🔍 Verificaciones Necesarias

### 1. Tabla `candidatos` - ¿Cuál es el tipo de ID?
Necesito confirmar:
- ¿Es `text` con formato CAND_XXX?
- ¿Es `bigint` autoincremental?
- ¿Es `uuid`?

### 2. Tabla `aplicaciones` - ¿Cuál es el tipo de candidato_id?
Debe coincidir con el tipo de `candidatos.id`

### 3. ¿Cómo se guardan las respuestas de los candidatos?
- ¿Se usa la tabla `evaluaciones`?
- ¿Hay otra tabla que no me mencionaste?
- ¿Las respuestas se guardan en otro lugar?

## 🚨 IMPACTO EN EL CÓDIGO

### Archivos que necesitan corrección URGENTE:

1. **`routes/candidatos.py`**
   - ❌ Intenta insertar en `respuestas_candidato` (NO EXISTE)
   - ❌ Usa `candidato_id` como TEXT en documentos (es BIGINT)
   - ❌ Genera ID como TEXT (puede ser incorrecto)

2. **`routes/empresas.py`**
   - ⚠️ Puede tener referencias incorrectas

3. **Todos los modelos Pydantic**
   - Necesitan actualización según estructura real

## 📝 INFORMACIÓN FALTANTE CRÍTICA

Para corregir el código correctamente, necesito saber:

1. **Estructura completa de tabla `candidatos`:**
   ```sql
   -- ¿Cuál es la estructura real?
   id ??? PRIMARY KEY
   nombre_anonimo text
   -- ... resto de columnas
   ```

2. **Estructura completa de tabla `aplicaciones`:**
   ```sql
   -- ¿Cuál es el tipo de candidato_id?
   candidato_id ??? REFERENCES candidatos(id)
   ```

3. **¿Cómo se guardan las respuestas a las preguntas?**
   - ¿En `evaluaciones`?
   - ¿En otra tabla?
   - ¿Directamente en `aplicaciones`?

## ⚠️ RECOMENDACIÓN URGENTE

**NO USES EL CÓDIGO QUE TE DI** hasta que confirmemos:
1. El tipo de dato de `candidatos.id`
2. Cómo se guardan las respuestas de los candidatos
3. La relación correcta entre todas las tablas

---

**Estado:** 🚨 REQUIERE CORRECCIÓN INMEDIATA
