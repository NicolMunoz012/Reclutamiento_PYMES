"""
Quick API Test Script
Run this after starting the server to verify everything works
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("🔍 Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Health check passed!")
            print(f"   Response: {response.json()}")
            return True
        else:
            print(f"❌ Health check failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error connecting to server: {e}")
        print("   Make sure the server is running: python main.py")
        return False


def test_registrar_empresa():
    """Test company registration"""
    print("\n🏢 Testing company registration...")
    try:
        data = {
            "nombre_empresa": "Test Company",
            "nit": "900000000-1",
            "industria": "Tecnología",
            "tamaño_empresa": "11-50",
            "descripcion": "Empresa de prueba",
            "ciudad": "Bogotá",
            "email": f"test{hash('test')}@example.com"
        }
        
        response = requests.post(f"{BASE_URL}/api/empresa/registrar", json=data)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Company registered successfully!")
            print(f"   Company ID: {result['empresa_id']}")
            return result['empresa_id']
        else:
            print(f"❌ Registration failed: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def test_vacantes_publicadas():
    """Test getting published job postings"""
    print("\n📋 Testing get published job postings...")
    try:
        response = requests.get(f"{BASE_URL}/api/vacantes/publicadas")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Found {len(result['vacantes'])} published job postings")
            if result['vacantes']:
                print(f"   First job: {result['vacantes'][0]['titulo']}")
            return True
        else:
            print(f"❌ Failed to get job postings: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def main():
    """Run all tests"""
    print("=" * 60)
    print("🚀 API Test Suite - Sistema de Reclutamiento")
    print("=" * 60)
    
    # Test 1: Health check
    if not test_health():
        print("\n❌ Server is not running. Start it with: python main.py")
        return
    
    # Test 2: Register company
    empresa_id = test_registrar_empresa()
    
    # Test 3: Get published jobs
    test_vacantes_publicadas()
    
    print("\n" + "=" * 60)
    print("✅ Basic tests completed!")
    print("=" * 60)
    print("\n📚 Next steps:")
    print("   1. Open http://localhost:8000/docs for interactive API docs")
    print("   2. Check EJEMPLOS_API.md for more detailed examples")
    print("   3. Configure your .env file with real credentials")
    print("   4. Test creating a job posting and applying as a candidate")
    

if __name__ == "__main__":
    main()
