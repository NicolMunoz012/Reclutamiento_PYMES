# 🔧 Solución al Error de Pydantic

## Problema
Error: `TypeError: ForwardRef._evaluate() missing 1 required keyword-only argument: 'recursive_guard'`

Este error ocurre porque las versiones antiguas de LangChain (0.1.x) no son compatibles con Python 3.13.

## Solución

### Opción 1: Script Automático (Recomendado)
```bash
cd backend
ACTUALIZAR_DEPENDENCIAS.bat
```

### Opción 2: Manual
```bash
cd backend

# Activar entorno virtual
venv\Scripts\activate

# Desinstalar versiones antiguas
pip uninstall -y langchain langchain-anthropic langchain-community langchain-core pydantic pydantic-settings

# Instalar nuevas versiones
pip install -r requirements.txt

# Iniciar servidor
python main.py
```

## Cambios Realizados

Se actualizaron las versiones a compatibles con Python 3.13:

**Antes:**
- langchain==0.1.9
- langchain-anthropic==0.1.4
- pydantic==2.5.3

**Después:**
- langchain==0.3.7
- langchain-anthropic==0.3.3
- langchain-core==0.3.15
- pydantic==2.9.2

## Verificar Instalación

```bash
python main.py
```

Deberías ver:
```
INFO:     Started server process
INFO:     Uvicorn running on http://0.0.0.0:8000
```

## Si Persiste el Error

1. Eliminar el entorno virtual:
```bash
rmdir /s /q venv
```

2. Crear nuevo entorno:
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

3. Iniciar servidor:
```bash
python main.py
```
