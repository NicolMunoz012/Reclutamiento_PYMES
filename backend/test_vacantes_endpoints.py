"""
Script para probar los endpoints de vacantes
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_listar_vacantes():
    """Test: Listar todas las vacantes publicadas"""
    print("=" * 60)
    print("TEST 1: Listar Vacantes Publicadas")
    print("=" * 60)
    
    try:
        response = requests.get(f"{BASE_URL}/api/vacantes/publicadas")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Status: {response.status_code}")
            print(f"Total vacantes: {data.get('total', 0)}")
            print(f"Vacantes en respuesta: {len(data.get('vacantes', []))}")
            print(f"Limit: {data.get('limit')}")
            print(f"Offset: {data.get('offset')}")
            
            if data.get('vacantes'):
                print("\nPrimera vacante:")
                vacante = data['vacantes'][0]
                print(f"  ID: {vacante['id']}")
                print(f"  Título: {vacante['titulo']}")
                print(f"  Empresa: {vacante['empresa_nombre']}")
                print(f"  Ciudad: {vacante['ciudad']}")
                print(f"  Modalidad: {vacante['modalidad']}")
                print(f"  Salario: ${vacante.get('salario_min', 0):,} - ${vacante.get('salario_max', 0):,}")
                return vacante['id']  # Retornar ID para siguiente test
        else:
            print(f"❌ Error: Status {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    return None


def test_filtrar_por_ciudad():
    """Test: Filtrar vacantes por ciudad"""
    print("\n" + "=" * 60)
    print("TEST 2: Filtrar por Ciudad (Bogotá)")
    print("=" * 60)
    
    try:
        response = requests.get(f"{BASE_URL}/api/vacantes/publicadas?ciudad=Bogotá")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Status: {response.status_code}")
            print(f"Vacantes en Bogotá: {data.get('total', 0)}")
            
            for i, vacante in enumerate(data.get('vacantes', [])[:3], 1):
                print(f"\n{i}. {vacante['titulo']}")
                print(f"   Ciudad: {vacante['ciudad']}")
                print(f"   Empresa: {vacante['empresa_nombre']}")
        else:
            print(f"❌ Error: Status {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")


def test_filtrar_por_modalidad():
    """Test: Filtrar vacantes por modalidad"""
    print("\n" + "=" * 60)
    print("TEST 3: Filtrar por Modalidad (Remoto)")
    print("=" * 60)
    
    try:
        response = requests.get(f"{BASE_URL}/api/vacantes/publicadas?modalidad=Remoto")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Status: {response.status_code}")
            print(f"Vacantes remotas: {data.get('total', 0)}")
            
            for i, vacante in enumerate(data.get('vacantes', [])[:3], 1):
                print(f"\n{i}. {vacante['titulo']}")
                print(f"   Modalidad: {vacante['modalidad']}")
                print(f"   Ciudad: {vacante['ciudad']}")
        else:
            print(f"❌ Error: Status {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")


def test_paginacion():
    """Test: Paginación"""
    print("\n" + "=" * 60)
    print("TEST 4: Paginación (limit=5, offset=0)")
    print("=" * 60)
    
    try:
        response = requests.get(f"{BASE_URL}/api/vacantes/publicadas?limit=5&offset=0")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Status: {response.status_code}")
            print(f"Total: {data.get('total')}")
            print(f"Limit: {data.get('limit')}")
            print(f"Offset: {data.get('offset')}")
            print(f"Vacantes en respuesta: {len(data.get('vacantes', []))}")
            
            print("\nVacantes:")
            for i, vacante in enumerate(data.get('vacantes', []), 1):
                print(f"  {i}. {vacante['titulo']} - {vacante['empresa_nombre']}")
        else:
            print(f"❌ Error: Status {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")


def test_detalle_vacante(vacante_id):
    """Test: Obtener detalle de vacante"""
    print("\n" + "=" * 60)
    print("TEST 5: Detalle de Vacante")
    print("=" * 60)
    
    if not vacante_id:
        print("⚠️  No hay vacante_id para probar")
        return
    
    try:
        response = requests.get(f"{BASE_URL}/api/vacantes/{vacante_id}/detalles")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Status: {response.status_code}")
            
            vacante = data.get('vacante', {})
            empresa = data.get('empresa', {})
            preguntas = data.get('preguntas', [])
            
            print(f"\n📋 VACANTE:")
            print(f"  Título: {vacante.get('titulo')}")
            print(f"  Cargo: {vacante.get('cargo')}")
            print(f"  Descripción: {vacante.get('descripcion', '')[:100]}...")
            print(f"  Tipo contrato: {vacante.get('tipo_contrato')}")
            print(f"  Modalidad: {vacante.get('modalidad')}")
            print(f"  Ciudad: {vacante.get('ciudad')}")
            print(f"  Experiencia: {vacante.get('experiencia_min')}-{vacante.get('experiencia_max')} años")
            print(f"  Salario: ${vacante.get('salario_min', 0):,} - ${vacante.get('salario_max', 0):,}")
            print(f"  Habilidades: {', '.join(vacante.get('habilidades_requeridas', []))}")
            print(f"  Número de vacantes: {vacante.get('numero_vacantes', 1)}")
            
            if vacante.get('beneficios'):
                print(f"  Beneficios: {', '.join(vacante.get('beneficios', []))}")
            
            print(f"\n🏢 EMPRESA:")
            print(f"  Nombre: {empresa.get('nombre_empresa')}")
            print(f"  Industria: {empresa.get('industria')}")
            print(f"  Ciudad: {empresa.get('ciudad')}")
            print(f"  Tamaño: {empresa.get('tamaño_empresa')}")
            if empresa.get('descripcion'):
                print(f"  Descripción: {empresa.get('descripcion')[:100]}...")
            
            print(f"\n❓ PREGUNTAS ({len(preguntas)}):")
            for i, pregunta in enumerate(preguntas, 1):
                print(f"  {i}. {pregunta['pregunta']} ({pregunta['tipo_pregunta']})")
            
            print(f"\n📊 ESTADÍSTICAS:")
            print(f"  Aplicaciones recibidas: {data.get('numero_aplicaciones', 0)}")
            
        else:
            print(f"❌ Error: Status {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Error: {e}")


def test_combinar_filtros():
    """Test: Combinar múltiples filtros"""
    print("\n" + "=" * 60)
    print("TEST 6: Combinar Filtros (Bogotá + Remoto)")
    print("=" * 60)
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/vacantes/publicadas?ciudad=Bogotá&modalidad=Remoto"
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Status: {response.status_code}")
            print(f"Vacantes remotas en Bogotá: {data.get('total', 0)}")
            
            for i, vacante in enumerate(data.get('vacantes', []), 1):
                print(f"\n{i}. {vacante['titulo']}")
                print(f"   Ciudad: {vacante['ciudad']}")
                print(f"   Modalidad: {vacante['modalidad']}")
                print(f"   Empresa: {vacante['empresa_nombre']}")
        else:
            print(f"❌ Error: Status {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")


def main():
    """Ejecutar todos los tests"""
    print("\n🚀 INICIANDO TESTS DE ENDPOINTS DE VACANTES\n")
    
    # Test 1: Listar vacantes (retorna ID para siguiente test)
    vacante_id = test_listar_vacantes()
    
    # Test 2: Filtrar por ciudad
    test_filtrar_por_ciudad()
    
    # Test 3: Filtrar por modalidad
    test_filtrar_por_modalidad()
    
    # Test 4: Paginación
    test_paginacion()
    
    # Test 5: Detalle de vacante
    test_detalle_vacante(vacante_id)
    
    # Test 6: Combinar filtros
    test_combinar_filtros()
    
    print("\n" + "=" * 60)
    print("✅ TESTS COMPLETADOS")
    print("=" * 60)


if __name__ == "__main__":
    print("\n⚠️  IMPORTANTE: Asegúrate de que el servidor esté corriendo")
    print("   Ejecuta: cd backend && python main.py\n")
    
    input("Presiona Enter para continuar...")
    
    main()
