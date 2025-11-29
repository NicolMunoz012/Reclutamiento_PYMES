# ✅ Estructura REAL de la Base de Datos

## 📊 Tablas Confirmadas

### 1. `usuarios` ✅
```sql
id uuid PRIMARY KEY
email text NOT NULL
tipo_usuario text NOT NULL
nombre_completo text
telefono text
created_at timestamptz DEFAULT now()
updated_at timestamptz DEFAULT now()
```

### 2. `empresas` ✅
```sql
id uuid PRIMARY KEY
usuario_id uuid REFERENCES usuarios(id)
nombre_empresa text NOT NULL
nit text
industria text
tamaño_empresa text
descripcion text
sitio_web text
logo_url text
ciudad text
direccion text
created_at timestamptz DEFAULT now()
updated_at timestamptz DEFAULT now()
```
**Nota:** NO tiene campo `email` (está en usuarios)

### 3. `vacantes` ✅
```sql
id uuid PRIMARY KEY
empresa_id uuid REFERENCES empresas(id)
titulo text NOT NULL
descripcion text NOT NULL
cargo text NOT NULL
tipo_contrato text
modalidad text
habilidades_requeridas jsonb
experiencia_min int DEFAULT 0
experiencia_max int
salario_min numeric
salario_max numeric
ciudad text
estado text DEFAULT 'borrador'
fecha_publicacion timestamptz
fecha_cierre timestamptz
numero_vacantes int DEFAULT 1
beneficios jsonb
created_at timestamptz DEFAULT now()
updated_at timestamptz DEFAULT now()
```

### 4. `candidatos` ⚠️ ESTRUCTURA REAL
```sql
id bigint PRIMARY KEY  -- ⚠️ Es BIGINT, no TEXT
usuario_id uuid REFERENCES usuarios(id)
nombre_anonimo text
email text
telefono text
linkedin_url text
github_url text
años_experiencia int  -- ⚠️ Con tilde
resumen_profesional text
created_at timestamptz DEFAULT now()
```
**Nota:** NO tiene `cargo_deseado`, `experiencia_años`, `habilidades`

### 5. `aplicaciones` ⚠️ ESTRUCTURA REAL
```sql
id uuid PRIMARY KEY
vacante_id uuid REFERENCES vacantes(id)
candidato_id bigint REFERENCES candidatos(id)  -- ⚠️ Es BIGINT
estado text DEFAULT 'aplicado'
puntuacion_ia numeric
compatibilidad_porcentaje numeric
notas_reclutador text
fecha_aplicacion timestamptz DEFAULT now()
fecha_ultima_actualizacion timestamptz DEFAULT now()
updated_at timestamptz DEFAULT now()
```

### 6. `documentos` ⚠️ ESTRUCTURA REAL
```sql
id uuid PRIMARY KEY
candidato_id bigint REFERENCES candidatos(id)  -- ⚠️ Es BIGINT
nombre_archivo text NOT NULL
tipo_documento text
url_archivo text NOT NULL
tamaño_kb int
mime_type text
texto_extraido text
created_at timestamptz DEFAULT now()
```

### 7. `vacante_preguntas` ✅
```sql
id uuid PRIMARY KEY
vacante_id uuid
pregunta text NOT NULL
tipo_pregunta text
opciones jsonb
es_obligatoria boolean DEFAULT true
orden int
generada_por_ia boolean DEFAULT true
aprobada_por_empresa boolean DEFAULT false
created_at timestamptz DEFAULT now()
```

### 8. `evaluaciones` (NO respuestas_candidato)
```sql
id integer PRIMARY KEY AUTOINCREMENT
entrevista_id integer
puntaje_general integer
fortalezas jsonb
debilidades jsonb
recomendacion text
created_at timestamptz DEFAULT now()
evaluador_nombre text
aspectos_positivos jsonb
aspectos_negativos jsonb
decision_final text
```

## 🚨 CAMBIOS CRÍTICOS NECESARIOS

### 1. `candidatos.id` es BIGINT (no TEXT)
- ❌ NO usar formato `CAND_001`
- ✅ Usar autoincremental BIGINT

### 2. `candidatos` tiene campos diferentes
- ✅ Tiene: `email`, `telefono`, `usuario_id`
- ✅ Tiene: `años_experiencia` (con tilde)
- ✅ Tiene: `resumen_profesional`
- ❌ NO tiene: `cargo_deseado`, `experiencia_años`, `habilidades`

### 3. Foreign keys usan BIGINT
- `aplicaciones.candidato_id` → BIGINT
- `documentos.candidato_id` → BIGINT

### 4. NO existe tabla `respuestas_candidato`
- Usar tabla `evaluaciones` en su lugar
