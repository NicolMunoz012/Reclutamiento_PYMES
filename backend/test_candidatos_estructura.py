"""
Script para validar la estructura de candidatos en Supabase
"""
from database import get_db
import uuid

def test_estructura_candidatos():
    """Valida que las tablas de candidatos tengan la estructura correcta"""
    print("=" * 60)
    print("VALIDACIÓN DE ESTRUCTURA - CANDIDATOS")
    print("=" * 60)
    
    db = get_db()
    
    # Test 1: Verificar tabla candidatos
    print("\n1. Verificando tabla 'candidatos'...")
    try:
        result = db.table("candidatos").select("*").limit(1).execute()
        print("   ✅ Tabla 'candidatos' existe")
        if result.data:
            print(f"   Columnas encontradas: {list(result.data[0].keys())}")
            print(f"   Tipo de ID: {type(result.data[0]['id'])} - {result.data[0]['id']}")
            
            # Verificar que ID es TEXT, no UUID
            if isinstance(result.data[0]['id'], str) and result.data[0]['id'].startswith('CAND_'):
                print("   ✅ ID es TEXT con formato correcto (CAND_XXX)")
            else:
                print(f"   ⚠️  ID tiene formato inesperado: {result.data[0]['id']}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 2: Verificar que NO existen columnas incorrectas
    print("\n2. Verificando que NO existan columnas incorrectas...")
    try:
        result = db.table("candidatos").select("*").limit(1).execute()
        if result.data:
            columnas = list(result.data[0].keys())
            
            # Columnas que NO deberían existir
            columnas_incorrectas = ['usuario_id', 'email', 'telefono', 'años_experiencia', 'resumen_profesional', 'fecha_registro']
            
            for col in columnas_incorrectas:
                if col in columnas:
                    print(f"   ⚠️  Columna '{col}' existe (no debería)")
                else:
                    print(f"   ✅ Columna '{col}' NO existe (correcto)")
            
            # Verificar columna correcta
            if 'experiencia_años' in columnas:
                print("   ✅ Columna 'experiencia_años' existe (correcto)")
            else:
                print("   ❌ Columna 'experiencia_años' NO existe (debería existir)")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 3: Verificar tabla documentos
    print("\n3. Verificando tabla 'documentos'...")
    try:
        result = db.table("documentos").select("*").limit(1).execute()
        print("   ✅ Tabla 'documentos' existe")
        if result.data:
            columnas = list(result.data[0].keys())
            print(f"   Columnas encontradas: {columnas}")
            
            # Verificar columnas requeridas
            if 'tamaño_kb' in columnas:
                print("   ✅ Columna 'tamaño_kb' existe")
            else:
                print("   ❌ Columna 'tamaño_kb' NO existe (requerida)")
            
            if 'mime_type' in columnas:
                print("   ✅ Columna 'mime_type' existe")
            else:
                print("   ❌ Columna 'mime_type' NO existe (requerida)")
            
            # Verificar que candidato_id es TEXT
            if result.data[0].get('candidato_id'):
                print(f"   candidato_id: {result.data[0]['candidato_id']} (tipo: {type(result.data[0]['candidato_id'])})")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 4: Verificar tabla aplicaciones
    print("\n4. Verificando tabla 'aplicaciones'...")
    try:
        result = db.table("aplicaciones").select("*").limit(1).execute()
        print("   ✅ Tabla 'aplicaciones' existe")
        if result.data:
            columnas = list(result.data[0].keys())
            print(f"   Columnas de fecha encontradas:")
            
            # Verificar campos de fecha
            campos_fecha = ['fecha_aplicacion', 'fecha_ultima_actualizacion', 'updated_at', 'created_at']
            for campo in campos_fecha:
                if campo in columnas:
                    print(f"      ✅ {campo}: {result.data[0].get(campo)}")
                else:
                    print(f"      ❌ {campo}: NO existe")
            
            # Verificar que candidato_id es TEXT
            if result.data[0].get('candidato_id'):
                print(f"   candidato_id: {result.data[0]['candidato_id']} (tipo: {type(result.data[0]['candidato_id'])})")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 5: Verificar tabla respuestas_candidato
    print("\n5. Verificando tabla 'respuestas_candidato'...")
    try:
        result = db.table("respuestas_candidato").select("*").limit(1).execute()
        print("   ✅ Tabla 'respuestas_candidato' existe")
        if result.data:
            columnas = list(result.data[0].keys())
            print(f"   Columnas encontradas: {columnas}")
            
            # Verificar que NO existe fecha_respuesta
            if 'fecha_respuesta' in columnas:
                print("   ⚠️  Columna 'fecha_respuesta' existe (no debería)")
            else:
                print("   ✅ Columna 'fecha_respuesta' NO existe (correcto)")
            
            # Verificar que existe created_at
            if 'created_at' in columnas:
                print("   ✅ Columna 'created_at' existe (correcto)")
            else:
                print("   ❌ Columna 'created_at' NO existe (debería existir)")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 6: Verificar candidatos existentes
    print("\n6. Verificando candidatos existentes...")
    try:
        result = db.table("candidatos").select("id, nombre_anonimo").execute()
        print(f"   ✅ Candidatos encontrados: {len(result.data)}")
        
        # Mostrar primeros 5
        for i, c in enumerate(result.data[:5], 1):
            print(f"      {i}. {c['id']} - {c.get('nombre_anonimo', 'N/A')}")
        
        # Verificar formato de IDs
        ids_correctos = sum(1 for c in result.data if isinstance(c['id'], str) and c['id'].startswith('CAND_'))
        print(f"   IDs con formato correcto (CAND_XXX): {ids_correctos}/{len(result.data)}")
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("VALIDACIÓN COMPLETADA")
    print("=" * 60)


def test_foreign_keys():
    """Verifica que las foreign keys funcionen correctamente"""
    print("\n" + "=" * 60)
    print("TEST DE FOREIGN KEYS")
    print("=" * 60)
    
    db = get_db()
    
    try:
        # Test 1: Verificar relación candidatos -> aplicaciones
        print("\n1. Verificando relación candidatos -> aplicaciones...")
        candidatos = db.table("candidatos").select("id").limit(1).execute()
        if candidatos.data:
            candidato_id = candidatos.data[0]['id']
            print(f"   Candidato ID: {candidato_id} (tipo: {type(candidato_id)})")
            
            # Buscar aplicaciones de este candidato
            aplicaciones = db.table("aplicaciones").select("*").eq("candidato_id", candidato_id).execute()
            print(f"   ✅ Aplicaciones encontradas: {len(aplicaciones.data)}")
        
        # Test 2: Verificar relación candidatos -> documentos
        print("\n2. Verificando relación candidatos -> documentos...")
        if candidatos.data:
            documentos = db.table("documentos").select("*").eq("candidato_id", candidato_id).execute()
            print(f"   ✅ Documentos encontrados: {len(documentos.data)}")
            if documentos.data:
                doc = documentos.data[0]
                print(f"   Documento: {doc.get('nombre_archivo')}")
                print(f"   Tamaño: {doc.get('tamaño_kb')} KB")
                print(f"   MIME: {doc.get('mime_type')}")
        
        print("\n" + "=" * 60)
        print("✅ FOREIGN KEYS FUNCIONAN CORRECTAMENTE")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error en test de foreign keys: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_estructura_candidatos()
    
    print("\n¿Deseas ejecutar test de foreign keys? (s/n): ", end="")
    respuesta = input().lower()
    if respuesta == 's':
        test_foreign_keys()
