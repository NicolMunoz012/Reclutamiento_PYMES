import os
from dotenv import load_dotenv

load_dotenv()

print("=== VERIFICACIÓN DE VARIABLES DE ENTORNO ===")
print(f"SUPABASE_URL: {os.getenv('SUPABASE_URL')}")
print(f"SUPABASE_KEY (primeros 20 chars): {os.getenv('SUPABASE_KEY')[:20] if os.getenv('SUPABASE_KEY') else 'NO ENCONTRADA'}")
print(f"SUPABASE_KEY length: {len(os.getenv('SUPABASE_KEY', ''))}")
print(f"GROQ_API_KEY existe: {bool(os.getenv('GROQ_API_KEY'))}")
print("==========================================")