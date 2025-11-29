# 🔗 Integración con Frontend (Next.js)

Guía para conectar el backend FastAPI con el frontend Next.js.

## 🌐 Configuración de CORS

El backend ya está configurado para aceptar requests del frontend:

```python
# En config.py
cors_origins: List[str] = ["http://localhost:3000", "http://localhost:5173"]
```

Si tu frontend corre en otro puerto, agrégalo al `.env`:

```env
CORS_ORIGINS=["http://localhost:3000","http://localhost:5173","http://localhost:4000"]
```

## 📡 Base URL del API

En tu frontend Next.js, configura la base URL:

```typescript
// lib/api.ts o config/api.ts
export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
```

En tu `.env.local` del frontend:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 🔌 Ejemplos de Integración

### 1. Registrar Empresa

```typescript
// services/empresaService.ts
import { API_BASE_URL } from '@/lib/api';

interface EmpresaRegistro {
  nombre_empresa: string;
  nit: string;
  industria: string;
  tamaño_empresa: string;
  descripcion?: string;
  ciudad: string;
  email: string;
}

export async function registrarEmpresa(data: EmpresaRegistro) {
  const response = await fetch(`${API_BASE_URL}/api/empresa/registrar`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    throw new Error('Error al registrar empresa');
  }

  return response.json();
}
```

### 2. Crear Vacante

```typescript
// services/vacanteService.ts
interface VacanteCrear {
  empresa_id: string;
  titulo: string;
  descripcion: string;
  cargo: string;
  tipo_contrato: string;
  modalidad: string;
  habilidades_requeridas: string[];
  experiencia_min: number;
  experiencia_max?: number;
  salario_min?: number;
  salario_max?: number;
  ciudad: string;
}

export async function crearVacante(data: VacanteCrear) {
  const response = await fetch(`${API_BASE_URL}/api/empresa/crear-vacante`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    throw new Error('Error al crear vacante');
  }

  return response.json();
}
```

### 3. Obtener Vacantes Publicadas

```typescript
// services/vacanteService.ts
interface FiltrosVacante {
  ciudad?: string;
  cargo?: string;
  modalidad?: string;
}

export async function obtenerVacantesPublicadas(filtros?: FiltrosVacante) {
  const params = new URLSearchParams();
  
  if (filtros?.ciudad) params.append('ciudad', filtros.ciudad);
  if (filtros?.cargo) params.append('cargo', filtros.cargo);
  if (filtros?.modalidad) params.append('modalidad', filtros.modalidad);

  const url = `${API_BASE_URL}/api/vacantes/publicadas${params.toString() ? '?' + params.toString() : ''}`;
  
  const response = await fetch(url);

  if (!response.ok) {
    throw new Error('Error al obtener vacantes');
  }

  return response.json();
}
```

### 4. Aplicar a Vacante (con CV)

```typescript
// services/candidatoService.ts
interface AplicarVacante {
  vacante_id: string;
  nombre_anonimo: string;
  email: string;
  telefono: string;
  ciudad: string;
  años_experiencia: number;
  cv_pdf: File;
}

export async function aplicarVacante(data: AplicarVacante) {
  const formData = new FormData();
  
  formData.append('vacante_id', data.vacante_id);
  formData.append('nombre_anonimo', data.nombre_anonimo);
  formData.append('email', data.email);
  formData.append('telefono', data.telefono);
  formData.append('ciudad', data.ciudad);
  formData.append('años_experiencia', data.años_experiencia.toString());
  formData.append('cv_pdf', data.cv_pdf);

  const response = await fetch(`${API_BASE_URL}/api/candidato/aplicar`, {
    method: 'POST',
    body: formData,
    // NO incluir Content-Type header, el browser lo configura automáticamente
  });

  if (!response.ok) {
    throw new Error('Error al aplicar a vacante');
  }

  return response.json();
}
```

### 5. Responder Preguntas

```typescript
// services/candidatoService.ts
interface Respuesta {
  pregunta_id: string;
  respuesta: string;
}

interface ResponderPreguntas {
  aplicacion_id: string;
  respuestas: Respuesta[];
}

export async function responderPreguntas(data: ResponderPreguntas) {
  const response = await fetch(`${API_BASE_URL}/api/candidato/responder`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    throw new Error('Error al enviar respuestas');
  }

  return response.json();
}
```

## 🎨 Componentes React Ejemplo

### Formulario de Registro de Empresa

```tsx
// components/RegistroEmpresaForm.tsx
'use client';

import { useState } from 'react';
import { registrarEmpresa } from '@/services/empresaService';

export default function RegistroEmpresaForm() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    const formData = new FormData(e.currentTarget);
    
    try {
      const result = await registrarEmpresa({
        nombre_empresa: formData.get('nombre_empresa') as string,
        nit: formData.get('nit') as string,
        industria: formData.get('industria') as string,
        tamaño_empresa: formData.get('tamaño_empresa') as string,
        descripcion: formData.get('descripcion') as string,
        ciudad: formData.get('ciudad') as string,
        email: formData.get('email') as string,
      });

      console.log('Empresa registrada:', result);
      // Redirigir o mostrar mensaje de éxito
      
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Error desconocido');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <input
        type="text"
        name="nombre_empresa"
        placeholder="Nombre de la empresa"
        required
        className="w-full p-2 border rounded"
      />
      
      <input
        type="text"
        name="nit"
        placeholder="NIT"
        required
        className="w-full p-2 border rounded"
      />
      
      {/* Más campos... */}
      
      {error && (
        <div className="text-red-500">{error}</div>
      )}
      
      <button
        type="submit"
        disabled={loading}
        className="w-full bg-blue-500 text-white p-2 rounded disabled:bg-gray-400"
      >
        {loading ? 'Registrando...' : 'Registrar Empresa'}
      </button>
    </form>
  );
}
```

### Lista de Vacantes

```tsx
// components/VacantesList.tsx
'use client';

import { useEffect, useState } from 'react';
import { obtenerVacantesPublicadas } from '@/services/vacanteService';

interface Vacante {
  id: string;
  titulo: string;
  empresa_nombre: string;
  ciudad: string;
  salario_min?: number;
  salario_max?: number;
  modalidad: string;
  habilidades_requeridas: string[];
}

export default function VacantesList() {
  const [vacantes, setVacantes] = useState<Vacante[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function cargarVacantes() {
      try {
        const data = await obtenerVacantesPublicadas();
        setVacantes(data.vacantes);
      } catch (error) {
        console.error('Error cargando vacantes:', error);
      } finally {
        setLoading(false);
      }
    }

    cargarVacantes();
  }, []);

  if (loading) return <div>Cargando vacantes...</div>;

  return (
    <div className="grid gap-4">
      {vacantes.map((vacante) => (
        <div key={vacante.id} className="border p-4 rounded">
          <h3 className="text-xl font-bold">{vacante.titulo}</h3>
          <p className="text-gray-600">{vacante.empresa_nombre}</p>
          <p>{vacante.ciudad} - {vacante.modalidad}</p>
          
          {vacante.salario_min && (
            <p>
              Salario: ${vacante.salario_min.toLocaleString()} - 
              ${vacante.salario_max?.toLocaleString()}
            </p>
          )}
          
          <div className="flex gap-2 mt-2">
            {vacante.habilidades_requeridas.map((skill) => (
              <span key={skill} className="bg-blue-100 px-2 py-1 rounded text-sm">
                {skill}
              </span>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}
```

### Formulario de Aplicación con CV

```tsx
// components/AplicarVacanteForm.tsx
'use client';

import { useState } from 'react';
import { aplicarVacante } from '@/services/candidatoService';

interface Props {
  vacanteId: string;
}

export default function AplicarVacanteForm({ vacanteId }: Props) {
  const [loading, setLoading] = useState(false);
  const [cvFile, setCvFile] = useState<File | null>(null);

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (!cvFile) return;

    setLoading(true);
    const formData = new FormData(e.currentTarget);

    try {
      const result = await aplicarVacante({
        vacante_id: vacanteId,
        nombre_anonimo: formData.get('nombre_anonimo') as string,
        email: formData.get('email') as string,
        telefono: formData.get('telefono') as string,
        ciudad: formData.get('ciudad') as string,
        años_experiencia: parseInt(formData.get('años_experiencia') as string),
        cv_pdf: cvFile,
      });

      console.log('Aplicación exitosa:', result);
      // Mostrar preguntas para responder
      
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <input
        type="text"
        name="nombre_anonimo"
        placeholder="Nombre"
        required
        className="w-full p-2 border rounded"
      />
      
      <input
        type="email"
        name="email"
        placeholder="Email"
        required
        className="w-full p-2 border rounded"
      />
      
      <input
        type="tel"
        name="telefono"
        placeholder="Teléfono"
        required
        className="w-full p-2 border rounded"
      />
      
      <input
        type="text"
        name="ciudad"
        placeholder="Ciudad"
        required
        className="w-full p-2 border rounded"
      />
      
      <input
        type="number"
        name="años_experiencia"
        placeholder="Años de experiencia"
        required
        min="0"
        className="w-full p-2 border rounded"
      />
      
      <div>
        <label className="block mb-2">CV (PDF)</label>
        <input
          type="file"
          accept=".pdf"
          onChange={(e) => setCvFile(e.target.files?.[0] || null)}
          required
          className="w-full"
        />
      </div>
      
      <button
        type="submit"
        disabled={loading || !cvFile}
        className="w-full bg-blue-500 text-white p-2 rounded disabled:bg-gray-400"
      >
        {loading ? 'Aplicando...' : 'Aplicar a Vacante'}
      </button>
    </form>
  );
}
```

## 🔄 Manejo de Estados con React Query

Para mejor manejo de estados y caché:

```bash
npm install @tanstack/react-query
```

```typescript
// hooks/useVacantes.ts
import { useQuery } from '@tanstack/react-query';
import { obtenerVacantesPublicadas } from '@/services/vacanteService';

export function useVacantes(filtros?: any) {
  return useQuery({
    queryKey: ['vacantes', filtros],
    queryFn: () => obtenerVacantesPublicadas(filtros),
  });
}
```

Uso en componente:

```tsx
import { useVacantes } from '@/hooks/useVacantes';

export default function VacantesPage() {
  const { data, isLoading, error } = useVacantes();

  if (isLoading) return <div>Cargando...</div>;
  if (error) return <div>Error: {error.message}</div>;

  return (
    <div>
      {data?.vacantes.map((vacante) => (
        <div key={vacante.id}>{vacante.titulo}</div>
      ))}
    </div>
  );
}
```

## 🎯 Tipos TypeScript

Crea un archivo de tipos compartidos:

```typescript
// types/api.ts

export interface Empresa {
  id: string;
  nombre_empresa: string;
  nit: string;
  industria: string;
  tamaño_empresa: string;
  descripcion?: string;
  ciudad: string;
  email: string;
}

export interface Vacante {
  id: string;
  titulo: string;
  descripcion: string;
  cargo: string;
  tipo_contrato: string;
  modalidad: string;
  habilidades_requeridas: string[];
  experiencia_min: number;
  experiencia_max?: number;
  salario_min?: number;
  salario_max?: number;
  ciudad: string;
  empresa_nombre: string;
  fecha_publicacion: string;
}

export interface Pregunta {
  pregunta_id: string;
  pregunta: string;
  tipo_pregunta: 'abierta' | 'si_no' | 'escala';
}

export interface Aplicacion {
  candidato_id: string;
  aplicacion_id: string;
  preguntas: Pregunta[];
}

export interface ResultadoAplicacion {
  mensaje: string;
  puntuacion_ia: number;
  compatibilidad_porcentaje: number;
  email_enviado: boolean;
}
```

## 🚨 Manejo de Errores

```typescript
// utils/apiError.ts
export class APIError extends Error {
  constructor(
    message: string,
    public statusCode: number,
    public details?: any
  ) {
    super(message);
    this.name = 'APIError';
  }
}

export async function handleAPIResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new APIError(
      error.detail || 'Error en la petición',
      response.status,
      error
    );
  }
  
  return response.json();
}
```

Uso:

```typescript
export async function registrarEmpresa(data: EmpresaRegistro) {
  const response = await fetch(`${API_BASE_URL}/api/empresa/registrar`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });

  return handleAPIResponse(response);
}
```

## 📱 Ejemplo de Flujo Completo

```typescript
// pages/aplicar/[vacanteId].tsx
'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { aplicarVacante, responderPreguntas } from '@/services/candidatoService';

export default function AplicarPage({ params }: { params: { vacanteId: string } }) {
  const router = useRouter();
  const [step, setStep] = useState<'datos' | 'preguntas' | 'completado'>('datos');
  const [aplicacionData, setAplicacionData] = useState<any>(null);

  // Paso 1: Enviar datos y CV
  const handleAplicar = async (formData: any) => {
    const result = await aplicarVacante({
      vacante_id: params.vacanteId,
      ...formData,
    });
    
    setAplicacionData(result);
    setStep('preguntas');
  };

  // Paso 2: Responder preguntas
  const handleResponder = async (respuestas: any[]) => {
    const result = await responderPreguntas({
      aplicacion_id: aplicacionData.aplicacion_id,
      respuestas,
    });
    
    setStep('completado');
    // Mostrar resultado
  };

  return (
    <div>
      {step === 'datos' && <FormularioDatos onSubmit={handleAplicar} />}
      {step === 'preguntas' && (
        <FormularioPreguntas
          preguntas={aplicacionData.preguntas}
          onSubmit={handleResponder}
        />
      )}
      {step === 'completado' && <MensajeExito />}
    </div>
  );
}
```

## 🔧 Variables de Entorno Frontend

```env
# .env.local
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## ✅ Checklist de Integración

- [ ] Configurar CORS en backend
- [ ] Configurar API_BASE_URL en frontend
- [ ] Crear servicios para cada endpoint
- [ ] Crear tipos TypeScript
- [ ] Implementar manejo de errores
- [ ] Crear componentes de formularios
- [ ] Probar flujo completo
- [ ] Agregar loading states
- [ ] Agregar validaciones
- [ ] Probar con datos reales

## 🎉 ¡Listo!

Con esta guía puedes integrar completamente el backend FastAPI con tu frontend Next.js. El backend está diseñado para ser fácil de consumir desde cualquier frontend moderno.
