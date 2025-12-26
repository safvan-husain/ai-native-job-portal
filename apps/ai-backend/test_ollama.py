import asyncio
import os
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage

load_dotenv()

async def test_ollama():
    model_name = os.getenv("OLLAMA_MODEL", "llama3.1:8b")
    base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    api_key = os.getenv("OLLAMA_API_KEY")
    
    llm = ChatOllama(
        model=model_name,
        base_url=base_url,
        api_key=api_key
    )
    try:
        print(f"Invoking Ollama at {base_url} with model {model_name}...")
        response = await llm.ainvoke([HumanMessage(content="Hello")])
        print("Success!")
        print(response.content)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_ollama())
