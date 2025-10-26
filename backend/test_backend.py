# test_backend.py
import requests
import json

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("\n🔍 Testing Health Endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_query():
    """Test query endpoint"""
    print("\n🔍 Testing Query Endpoint...")
    data = {"question": "What is Python?"}
    response = requests.post(f"{BASE_URL}/query", json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_chat():
    """Test chat endpoint"""
    print("\n🔍 Testing Chat Endpoint...")
    
    # First message
    data1 = {"question": "What is machine learning?", "session_id": "test123"}
    response1 = requests.post(f"{BASE_URL}/chat", json=data1)
    print(f"Question 1: {data1['question']}")
    print(f"Answer: {response1.json()['text'][:100]}...")
    
    # Second message (should remember context)
    data2 = {"question": "Can you give me an example?", "session_id": "test123"}
    response2 = requests.post(f"{BASE_URL}/chat", json=data2)
    print(f"\nQuestion 2: {data2['question']}")
    print(f"Answer: {response2.json()['text'][:100]}...")

if __name__ == "__main__":
    print("🧪 AI Tutor Backend Tests")
    print("="*60)
    
    try:
        test_health()
        test_query()
        test_chat()
        print("\n✅ All tests completed!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
