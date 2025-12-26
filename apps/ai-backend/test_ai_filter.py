import requests
import json
import time

def test_filter(query):
    print(f"\nQuery: '{query}'")
    try:
        response = requests.post(
            "http://127.0.0.1:8006/candidates/ai-filter",
            json={"query": query},
            timeout=30
        )
        if response.status_code == 200:
            print("Response:")
            print(response.json().get("response"))
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    # Give the server a moment to start if run concurrently
    time.sleep(2)
    
    test_queries = [
        "I need a Python developer who knows AI",
        "Looking for someone with React and TypeScript",
        "Are there any mobile experts specialization in Flutter?",
        "Show me game developers using Unreal Engine"
    ]
    
    for q in test_queries:
        test_filter(q)
