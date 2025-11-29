from database import get_db

try:
    db = get_db()
    result = db.table("empresas").select("*").limit(1).execute()
    print("✅ Conexión exitosa a Supabase")
    print(f"Datos: {result.data}")
except Exception as e:
    print(f"❌ Error de conexión: {e}")
    import traceback
    traceback.print_exc()