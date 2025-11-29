"""
Test script para verificar que Anthropic funciona correctamente
"""
import asyncio
import os
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain.prompts import ChatPromptTemplate

load_dotenv()

async def test_anthropic_basic():
    """Test básico de Anthropic con LangChain"""
    print("=" * 60)
    print("TEST 1: Conexión básica con Anthropic")
    print("=" * 60)
    
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("❌ ERROR: ANTHROPIC_API_KEY no configurada")
        return False
    
    print(f"✅ API Key encontrada: {api_key[:10]}...")
    
    try:
        # Modelo correcto de Anthropic
        llm = ChatAnthropic(
            model="claude-3-5-sonnet-20241022",
            anthropic_api_key=api_key,
            max_tokens=100,
            temperature=0.7
        )
        print("✅ Cliente ChatAnthropic creado correctamente")
        
        # Test simple
        prompt = ChatPromptTemplate.from_messages([
            ("system", "Eres un asistente útil."),
            ("user", "Di 'Hola mundo' en JSON: {{'mensaje': 'tu respuesta'}}")
        ])
        
        chain = prompt | llm
        print("✅ Chain creado con operador |")
        
        response = await chain.ainvoke({})
        print("✅ Respuesta recibida")
        print(f"Tipo de respuesta: {type(response)}")
        print(f"Contenido: {response.content}")
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_json_generation():
    """Test de generación de JSON"""
    print("\n" + "=" * 60)
    print("TEST 2: Generación de JSON")
    print("=" * 60)
    
    api_key = os.getenv("ANTHROPIC_API_KEY")
    
    try:
        llm = ChatAnthropic(
            model="claude-3-5-sonnet-20241022",
            anthropic_api_key=api_key,
            max_tokens=500,
            temperature=0.7
        )
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", "Eres un experto en reclutamiento."),
            ("user", """Genera 3 preguntas para un desarrollador Python.

Retorna ÚNICAMENTE un JSON:
[
  {{"pregunta": "texto aquí", "tipo_pregunta": "abierta"}},
  {{"pregunta": "texto aquí", "tipo_pregunta": "si_no"}}
]

No incluyas markdown, solo JSON.""")
        ])
        
        chain = prompt | llm
        response = await chain.ainvoke({})
        
        print("✅ JSON generado:")
        print(response.content)
        
        # Intentar parsear
        import json
        try:
            data = json.loads(response.content.strip())
            print("✅ JSON válido parseado correctamente")
            print(f"Número de preguntas: {len(data)}")
        except:
            # Intentar limpiar markdown
            text = response.content.strip()
            if text.startswith("```"):
                lines = text.split("\n")
                text = "\n".join(lines[1:-1])
                if text.startswith("json"):
                    text = text[4:]
            data = json.loads(text.strip())
            print("✅ JSON parseado después de limpiar markdown")
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_ia_service():
    """Test del servicio de IA completo"""
    print("\n" + "=" * 60)
    print("TEST 3: Servicio de IA completo")
    print("=" * 60)
    
    try:
        from services.ia_service import ia_service
        
        print("✅ IAService importado correctamente")
        
        # Test generar preguntas
        print("\nGenerando preguntas...")
        preguntas = await ia_service.generar_preguntas_vacante(
            titulo="Desarrollador Python",
            descripcion="Buscamos desarrollador con experiencia en FastAPI",
            habilidades_requeridas=["Python", "FastAPI", "PostgreSQL"],
            experiencia_min=2
        )
        
        print(f"✅ Preguntas generadas: {len(preguntas)}")
        for i, p in enumerate(preguntas, 1):
            print(f"  {i}. {p['pregunta'][:50]}... ({p['tipo_pregunta']})")
        
        # Test analizar CV
        print("\nAnalizando CV...")
        cv_test = """
        Juan Pérez
        Desarrollador Python con 3 años de experiencia
        Habilidades: Python, FastAPI, Django, PostgreSQL, Docker
        Educación: Ingeniería de Sistemas
        """
        
        analisis = await ia_service.analizar_cv(cv_test)
        print(f"✅ CV analizado:")
        print(f"  Habilidades: {analisis.get('habilidades', [])}")
        print(f"  Experiencia: {analisis.get('experiencia_años', 0)} años")
        print(f"  Educación: {analisis.get('educacion', 'N/A')}")
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """Ejecutar todos los tests"""
    print("\n🚀 INICIANDO TESTS DE ANTHROPIC + LANGCHAIN\n")
    
    results = []
    
    # Test 1: Básico
    results.append(await test_anthropic_basic())
    
    # Test 2: JSON
    results.append(await test_json_generation())
    
    # Test 3: Servicio completo
    results.append(await test_ia_service())
    
    # Resumen
    print("\n" + "=" * 60)
    print("RESUMEN DE TESTS")
    print("=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"✅ Tests exitosos: {passed}/{total}")
    
    if passed == total:
        print("\n🎉 ¡TODOS LOS TESTS PASARON!")
        print("El servicio de IA está funcionando correctamente.")
    else:
        print("\n⚠️  Algunos tests fallaron. Revisa los errores arriba.")


if __name__ == "__main__":
    asyncio.run(main())
