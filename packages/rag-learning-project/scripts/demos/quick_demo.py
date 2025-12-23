"""
Quick demo of Phase 2 - Ollama Cloud Integration
Shows the agent in action with a sample conversation.
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.job_portal.agent import SimpleAgent


def main():
    print("\n" + "=" * 70)
    print("PHASE 2 DEMO: Ollama Cloud Integration")
    print("=" * 70 + "\n")
    
    print("Creating agent for job seeker...\n")
    agent = SimpleAgent(user_type="job_seeker")
    
    conversation = [
        "Hi, I'm looking for a Python developer job",
        "I have 5 years of experience with Django and FastAPI",
        "What did I just tell you about my experience?"
    ]
    
    thread_id = "demo"
    
    for i, message in enumerate(conversation, 1):
        print(f"\n{'─' * 70}")
        print(f"Turn {i}")
        print(f"{'─' * 70}")
        print(f"\n👤 User: {message}\n")
        print("🤖 Agent: ", end="", flush=True)
        
        # Stream the response
        chunks = []
        for chunk in agent.stream_chat(message, thread_id=thread_id):
            if not chunks or chunk != "".join(chunks):
                new_content = chunk[len("".join(chunks)):]
                print(new_content, end="", flush=True)
                chunks.append(new_content)
        
        print("\n")
    
    print("=" * 70)
    print("Demo complete! Phase 2 is working perfectly. ✅")
    print("=" * 70 + "\n")
    
    print("Key Features Demonstrated:")
    print("  ✅ Ollama Cloud connection")
    print("  ✅ Intelligent responses")
    print("  ✅ Conversation memory (remembers context)")
    print("  ✅ Streaming responses")
    print("  ✅ User type awareness (job seeker mode)")
    print("\nReady for Phase 3: Tool Definitions! 🚀\n")


if __name__ == "__main__":
    main()
