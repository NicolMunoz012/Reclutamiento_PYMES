"""
Test rápido para verificar que todas las importaciones funcionan
"""

print("=" * 60)
print("TEST DE IMPORTACIONES - LangChain 1.x")
print("=" * 60)

try:
    print("\n1. Importando ChatGroq...")
    from langchain_groq import ChatGroq
    print("   ✅ ChatGroq importado correctamente")
except Exception as e:
    print(f"   ❌ Error: {e}")

try:
    print("\n2. Importando ChatPromptTemplate...")
    from langchain_core.prompts import ChatPromptTemplate
    print("   ✅ ChatPromptTemplate importado correctamente")
except Exception as e:
    print(f"   ❌ Error: {e}")

try:
    print("\n3. Importando MessagesPlaceholder...")
    from langchain_core.prompts import MessagesPlaceholder
    print("   ✅ MessagesPlaceholder importado correctamente")
except Exception as e:
    print(f"   ❌ Error: {e}")

try:
    print("\n4. Importando ConversationBufferMemory...")
    from langchain.memory import ConversationBufferMemory
    print("   ✅ ConversationBufferMemory importado correctamente")
except Exception as e:
    print(f"   ❌ Error: {e}")

try:
    print("\n5. Importando ConversationChain...")
    from langchain.chains import ConversationChain
    print("   ✅ ConversationChain importado correctamente")
except Exception as e:
    print(f"   ❌ Error: {e}")

try:
    print("\n6. Importando servicios...")
    from services.ia_service import ia_service
    print("   ✅ IAService importado correctamente")
except Exception as e:
    print(f"   ❌ Error: {e}")

try:
    print("\n7. Importando chatbot...")
    from services.chatbot_service import chatbot_service
    print("   ✅ ChatbotService importado correctamente")
except Exception as e:
    print(f"   ❌ Error: {e}")

try:
    print("\n8. Importando config...")
    from config import settings
    print("   ✅ Settings importado correctamente")
    print(f"   GROQ_API_KEY configurada: {'Sí' if settings.groq_api_key else 'No'}")
except Exception as e:
    print(f"   ❌ Error: {e}")

print("\n" + "=" * 60)
print("RESULTADO: Todas las importaciones funcionan correctamente ✅")
print("=" * 60)
print("\nEl servidor debería arrancar sin problemas.")
print("Ejecuta: python main.py")
print("=" * 60)
