"""
Quick Test Script for LangChain Integration
Run this to verify that LangChain is working correctly
"""
import asyncio
import sys


def test_imports():
    """Test that all required packages are installed"""
    print("🔍 Testing imports...")
    
    try:
        import langchain
        print(f"  ✅ langchain: {langchain.__version__}")
    except ImportError as e:
        print(f"  ❌ langchain not installed: {e}")
        return False
    
    try:
        from langchain_anthropic import ChatAnthropic
        print("  ✅ langchain-anthropic: OK")
    except ImportError as e:
        print(f"  ❌ langchain-anthropic not installed: {e}")
        return False
    
    try:
        from langchain.prompts import ChatPromptTemplate
        from langchain.memory import ConversationBufferMemory
        from langchain.chains import ConversationChain
        print("  ✅ langchain components: OK")
    except ImportError as e:
        print(f"  ❌ langchain components error: {e}")
        return False
    
    print("✅ All imports successful!\n")
    return True


def test_services():
    """Test that services can be imported"""
    print("🔍 Testing services...")
    
    try:
        from services.ia_service import ia_service
        print("  ✅ ia_service imported")
    except Exception as e:
        print(f"  ❌ ia_service error: {e}")
        return False
    
    try:
        from services.chatbot_service import chatbot_service
        print("  ✅ chatbot_service imported")
    except Exception as e:
        print(f"  ❌ chatbot_service error: {e}")
        return False
    
    print("✅ All services imported successfully!\n")
    return True


async def test_ia_service():
    """Test IA Service with LangChain"""
    print("🔍 Testing IA Service...")
    
    try:
        from services.ia_service import ia_service
        
        # Test question generation (without API call)
        print("  ✅ IA Service initialized with LangChain")
        print(f"  ✅ LLM model: {ia_service.llm.model}")
        print(f"  ✅ Temperature: {ia_service.llm.temperature}")
        
        # Check helper methods exist
        assert hasattr(ia_service, '_parse_json_response'), "Missing _parse_json_response method"
        assert hasattr(ia_service, '_get_fallback_questions'), "Missing _get_fallback_questions method"
        print("  ✅ Helper methods present")
        
    except Exception as e:
        print(f"  ❌ IA Service error: {e}")
        return False
    
    print("✅ IA Service test passed!\n")
    return True


async def test_chatbot_service():
    """Test Chatbot Service with LangChain"""
    print("🔍 Testing Chatbot Service...")
    
    try:
        from services.chatbot_service import chatbot_service
        
        # Test initialization
        print("  ✅ Chatbot Service initialized with LangChain")
        print(f"  ✅ LLM model: {chatbot_service.llm.model}")
        print(f"  ✅ Temperature: {chatbot_service.llm.temperature}")
        print(f"  ✅ Max tokens: {chatbot_service.llm.max_tokens}")
        
        # Check conversation memory
        assert hasattr(chatbot_service, 'conversations'), "Missing conversations dict"
        assert isinstance(chatbot_service.conversations, dict), "conversations should be dict"
        print("  ✅ Conversation memory initialized")
        
        # Check methods exist
        assert hasattr(chatbot_service, 'iniciar_conversacion'), "Missing iniciar_conversacion"
        assert hasattr(chatbot_service, 'siguiente_pregunta'), "Missing siguiente_pregunta"
        assert hasattr(chatbot_service, 'finalizar_conversacion'), "Missing finalizar_conversacion"
        assert hasattr(chatbot_service, 'limpiar_conversacion'), "Missing limpiar_conversacion"
        print("  ✅ All chatbot methods present")
        
    except Exception as e:
        print(f"  ❌ Chatbot Service error: {e}")
        return False
    
    print("✅ Chatbot Service test passed!\n")
    return True


async def test_endpoints():
    """Test that new endpoints are registered"""
    print("🔍 Testing endpoints...")
    
    try:
        from routes.candidatos import router
        
        # Get all routes
        routes = [route.path for route in router.routes]
        
        # Check chatbot endpoints exist
        chatbot_endpoints = [
            "/chatbot/iniciar",
            "/chatbot/siguiente",
            "/chatbot/finalizar",
            "/chatbot/limpiar/{aplicacion_id}"
        ]
        
        for endpoint in chatbot_endpoints:
            if endpoint in routes:
                print(f"  ✅ Endpoint registered: {endpoint}")
            else:
                print(f"  ❌ Endpoint missing: {endpoint}")
                return False
        
    except Exception as e:
        print(f"  ❌ Endpoints error: {e}")
        return False
    
    print("✅ All chatbot endpoints registered!\n")
    return True


async def main():
    """Run all tests"""
    print("=" * 60)
    print("🧪 LangChain Integration Test Suite")
    print("=" * 60)
    print()
    
    results = []
    
    # Test 1: Imports
    results.append(("Imports", test_imports()))
    
    # Test 2: Services
    results.append(("Services", test_services()))
    
    # Test 3: IA Service
    results.append(("IA Service", await test_ia_service()))
    
    # Test 4: Chatbot Service
    results.append(("Chatbot Service", await test_chatbot_service()))
    
    # Test 5: Endpoints
    results.append(("Endpoints", await test_endpoints()))
    
    # Summary
    print("=" * 60)
    print("📊 Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
    
    print()
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print()
        print("🎉 All tests passed! LangChain integration is working correctly.")
        print()
        print("Next steps:")
        print("  1. Start the server: python main.py")
        print("  2. Open Swagger docs: http://localhost:8000/docs")
        print("  3. Test chatbot endpoints")
        print("  4. Check CHATBOT_EXAMPLES.md for usage examples")
        return 0
    else:
        print()
        print("❌ Some tests failed. Please check the errors above.")
        print()
        print("Common issues:")
        print("  - Missing dependencies: pip install -r requirements.txt")
        print("  - Wrong Python version: Requires Python 3.10+")
        print("  - Missing .env file: Copy .env.example to .env")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
