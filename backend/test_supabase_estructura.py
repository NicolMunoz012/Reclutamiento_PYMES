"""
Script para validar la estructura de la base de datos en Supabase
"""
from database import get_db
from datetime import datetime
import uuid

def test_estructura_bd():
    """Valida que las tablas y columnas existan"""
    print("=" * 60)
    print("VALIDACIÓN DE ESTRUCTURA DE BASE DE DATOS")
    print("=" * 60)
    
    db = get_db()
    
    # Test 1: Verificar tabla usuarios
    print("\n1. Verificando tabla 'usuarios'...")
    try:
        result = db.table("usuarios").select("*").limit(1).execute()
        print("   ✅ Tabla 'usuarios' existe")
        if result.data:
            print(f"   Columnas encontradas: {list(result.data[0].keys())}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 2: Verificar tabla empresas
    print("\n2. Verificando tabla 'empresas'...")
    try:
        result = db.table("empresas").select("*").limit(1).execute()
        print("   ✅ Tabla 'empresas' existe")
        if result.data:
            print(f"   Columnas encontradas: {list(result.data[0].keys())}")
            print(f"   Total empresas: {len(result.data)}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 3: Verificar tabla vacantes
    print("\n3. Verificando tabla 'vacantes'...")
    try:
        result = db.table("vacantes").select("*").limit(1).execute()
        print("   ✅ Tabla 'vacantes' existe")
        if result.data:
            print(f"   Columnas encontradas: {list(result.data[0].keys())}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 4: Verificar vacantes publicadas
    print("\n4. Verificando vacantes publicadas...")
    try:
        result = db.table("vacantes").select("id, titulo, estado").eq("estado", "publicada").execute()
        print(f"   ✅ Vacantes publicadas: {len(result.data)}")
        for v in result.data[:3]:
            print(f"      - {v['titulo']} (ID: {v['id'][:8]}...)")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 5: Verificar empresas existentes
    print("\n5. Verificando empresas existentes...")
    try:
        result = db.table("empresas").select("id, nombre_empresa").execute()
        print(f"   ✅ Empresas encontradas: {len(result.data)}")
        for e in result.data:
            print(f"      - {e['nombre_empresa']} (ID: {e['id'][:8]}...)")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 6: Verificar columnas específicas
    print("\n6. Verificando columnas críticas...")
    try:
        # Verificar que created_at existe (no fecha_registro)
        result = db.table("empresas").select("created_at").limit(1).execute()
        print("   ✅ Columna 'created_at' existe en empresas")
        
        # Verificar que NO existe email en empresas
        try:
            result = db.table("empresas").select("email").limit(1).execute()
            print("   ⚠️  Columna 'email' existe en empresas (inesperado)")
        except:
            print("   ✅ Columna 'email' NO existe en empresas (correcto)")
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("VALIDACIÓN COMPLETADA")
    print("=" * 60)


def test_insert_empresa():
    """Test de inserción de empresa con estructura correcta"""
    print("\n" + "=" * 60)
    print("TEST DE INSERCIÓN DE EMPRESA")
    print("=" * 60)
    
    db = get_db()
    
    try:
        # Crear usuario
        usuario_id = str(uuid.uuid4())
        usuario_data = {
            "id": usuario_id,
            "email": f"test_{usuario_id[:8]}@test.com",
            "tipo_usuario": "empresa",
            "nombre_completo": "Empresa Test"
        }
        
        print("\n1. Insertando usuario...")
        db.table("usuarios").insert(usuario_data).execute()
        print("   ✅ Usuario creado")
        
        # Crear empresa
        empresa_id = str(uuid.uuid4())
        empresa_data = {
            "id": empresa_id,
            "usuario_id": usuario_id,
            "nombre_empresa": "Test Corporation",
            "nit": "900999999",
            "industria": "Tecnología",
            "tamaño_empresa": "11-50",
            "descripcion": "Empresa de prueba",
            "ciudad": "Bogotá"
        }
        
        print("\n2. Insertando empresa...")
        db.table("empresas").insert(empresa_data).execute()
        print("   ✅ Empresa creada")
        
        # Verificar
        print("\n3. Verificando datos insertados...")
        result = db.table("empresas").select("*").eq("id", empresa_id).execute()
        if result.data:
            empresa = result.data[0]
            print(f"   ✅ Empresa encontrada: {empresa['nombre_empresa']}")
            print(f"   created_at: {empresa.get('created_at')}")
            print(f"   updated_at: {empresa.get('updated_at')}")
        
        # Limpiar
        print("\n4. Limpiando datos de prueba...")
        db.table("empresas").delete().eq("id", empresa_id).execute()
        db.table("usuarios").delete().eq("id", usuario_id).execute()
        print("   ✅ Datos de prueba eliminados")
        
        print("\n" + "=" * 60)
        print("✅ TEST DE INSERCIÓN EXITOSO")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error en test de inserción: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_estructura_bd()
    
    print("\n¿Deseas ejecutar test de inserción? (s/n): ", end="")
    respuesta = input().lower()
    if respuesta == 's':
        test_insert_empresa()
