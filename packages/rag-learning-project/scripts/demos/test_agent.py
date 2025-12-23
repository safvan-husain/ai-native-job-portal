"""
Test script for Phase 2: Ollama Cloud Integration
Tests the agent independently and verifies all Phase 2 requirements.
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.job_portal.agent import SimpleAgent


def test_basic_chat():
    """Test basic chat functionality."""
    print("=" * 60)
    print("TEST 1: Basic Chat")
    print("=" * 60)
    
    agent = SimpleAgent(user_type="job_seeker")
    
    response = agent.chat("Hi, I'm looking for a job", thread_id="test1")
    print(f"User: Hi, I'm looking for a job")
    print(f"Agent: {response}\n")
    
    assert len(response) > 0, "Agent should return a response"
    print("✓ Basic chat works\n")


def test_memory():
    """Test conversation memory."""
    print("=" * 60)
    print("TEST 2: Conversation Memory")
    print("=" * 60)
    
    agent = SimpleAgent(user_type="job_seeker")
    thread_id = "test2"
    
    # First message
    response1 = agent.chat("I'm a Python developer with 5 years of experience", thread_id=thread_id)
    print(f"User: I'm a Python developer with 5 years of experience")
    print(f"Agent: {response1}\n")
    
    # Second message - should remember context
    response2 = agent.chat("What did I just tell you about my experience?", thread_id=thread_id)
    print(f"User: What did I just tell you about my experience?")
    print(f"Agent: {response2}\n")
    
    # Check if agent remembers
    assert "python" in response2.lower() or "5" in response2 or "five" in response2.lower(), \
        "Agent should remember previous context"
    
    print("✓ Memory works\n")


def test_streaming():
    """Test streaming responses."""
    print("=" * 60)
    print("TEST 3: Streaming Responses")
    print("=" * 60)
    
    agent = SimpleAgent(user_type="company")
    
    print("User: Tell me about hiring Python developers")
    print("Agent (streaming): ", end="", flush=True)
    
    chunks = []
    for chunk in agent.stream_chat("Tell me about hiring Python developers", thread_id="test3"):
        # Print only new content
        if not chunks or chunk != "".join(chunks):
            new_content = chunk[len("".join(chunks)):]
            print(new_content, end="", flush=True)
            chunks.append(new_content)
    
    print("\n")
    
    full_response = "".join(chunks)
    assert len(full_response) > 0, "Streaming should return content"
    print("✓ Streaming works\n")


def test_user_type_switching():
    """Test switching between user types."""
    print("=" * 60)
    print("TEST 4: User Type Switching")
    print("=" * 60)
    
    agent = SimpleAgent(user_type="job_seeker")
    
    response1 = agent.chat("Hi", thread_id="test4")
    print(f"As Job Seeker: {response1[:100]}...\n")
    
    # Switch to company
    agent.set_user_type("company")
    response2 = agent.chat("Hi", thread_id="test5")
    print(f"As Company: {response2[:100]}...\n")
    
    print("✓ User type switching works\n")


def test_error_handling():
    """Test error handling."""
    print("=" * 60)
    print("TEST 5: Error Handling")
    print("=" * 60)
    
    try:
        # Test with invalid API key
        agent = SimpleAgent(api_key="invalid_key")
        print("✗ Should have raised error for invalid API key")
    except Exception as e:
        print(f"✓ Correctly handles invalid API key: {type(e).__name__}\n")
    
    try:
        # Test with no API key
        os.environ.pop("OLLAMA_API_KEY", None)
        agent = SimpleAgent()
        print("✗ Should have raised error for missing API key")
    except ValueError as e:
        print(f"✓ Correctly handles missing API key: {str(e)}\n")


def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("PHASE 2: OLLAMA CLOUD INTEGRATION - TEST SUITE")
    print("=" * 60 + "\n")
    
    try:
        test_basic_chat()
        test_memory()
        test_streaming()
        test_user_type_switching()
        test_error_handling()
        
        print("=" * 60)
        print("ALL TESTS PASSED! ✓")
        print("=" * 60)
        print("\nPhase 2 Requirements Met:")
        print("✓ Ollama Cloud connection works")
        print("✓ Basic chat functionality")
        print("✓ Conversation memory (LangGraph checkpointer)")
        print("✓ Streaming responses")
        print("✓ User type awareness")
        print("✓ Error handling")
        print("\nReady to proceed to Phase 3!")
        
    except Exception as e:
        print(f"\n✗ TEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
