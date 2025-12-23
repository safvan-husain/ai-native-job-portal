"""
Test script for Phase 5: Enhanced Agent with Tools

This script tests the agent's ability to:
1. Use tools intelligently based on user input
2. Handle different user types (job seeker vs company)
3. Manage state across conversation
4. Format tool results nicely
"""

import os
import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent.parent.parent / "src"
sys.path.insert(0, str(src_path))

from job_portal.agent.simple_agent import SimpleAgent


def test_job_seeker_flow():
    """Test job seeker conversation with tool usage."""
    print("=" * 70)
    print("TEST 1: Job Seeker Flow")
    print("=" * 70)
    
    try:
        # Create agent for job seeker
        agent = SimpleAgent(user_type="job_seeker")
        print("✅ Agent initialized for job seeker")
        
        # Test conversation
        test_messages = [
            "Hi, I'm looking for a job",
            "I'm a Python developer with 5 years of experience, interested in remote fintech positions",
        ]
        
        for msg in test_messages:
            print(f"\n👤 User: {msg}")
            print("🤖 Agent: ", end="")
            
            # Get response
            response = agent.chat(msg, thread_id="test_job_seeker")
            print(response)
        
        print("\n✅ Job seeker flow completed")
        
    except Exception as e:
        print(f"\n❌ Error in job seeker flow: {str(e)}")
        import traceback
        traceback.print_exc()


def test_company_flow():
    """Test company conversation with tool usage."""
    print("\n" + "=" * 70)
    print("TEST 2: Company Flow")
    print("=" * 70)
    
    try:
        # Create agent for company
        agent = SimpleAgent(user_type="company")
        print("✅ Agent initialized for company")
        
        # Test conversation
        test_messages = [
            "We're hiring",
            "We need a senior Python developer with ML experience for our fintech startup",
        ]
        
        for msg in test_messages:
            print(f"\n👤 User: {msg}")
            print("🤖 Agent: ", end="")
            
            # Get response
            response = agent.chat(msg, thread_id="test_company")
            print(response)
        
        print("\n✅ Company flow completed")
        
    except Exception as e:
        print(f"\n❌ Error in company flow: {str(e)}")
        import traceback
        traceback.print_exc()


def test_tool_selection():
    """Test that agent selects appropriate tools."""
    print("\n" + "=" * 70)
    print("TEST 3: Tool Selection")
    print("=" * 70)
    
    try:
        agent = SimpleAgent(user_type="job_seeker")
        
        # Check tools are bound
        print(f"✅ Agent has {len(agent.tools)} tools available")
        print(f"   Tools: {[tool.name for tool in agent.tools]}")
        
        # Verify tools match user type
        tool_names = [tool.name for tool in agent.tools]
        expected_tools = ["search_jobs", "get_company_details", "compare_companies"]
        
        for expected in expected_tools:
            if expected in tool_names:
                print(f"   ✅ {expected} available")
            else:
                print(f"   ❌ {expected} missing")
        
        print("\n✅ Tool selection test completed")
        
    except Exception as e:
        print(f"\n❌ Error in tool selection: {str(e)}")
        import traceback
        traceback.print_exc()


def test_user_type_switching():
    """Test switching user types."""
    print("\n" + "=" * 70)
    print("TEST 4: User Type Switching")
    print("=" * 70)
    
    try:
        agent = SimpleAgent(user_type="job_seeker")
        print(f"✅ Initial user type: job_seeker")
        print(f"   Tools: {[tool.name for tool in agent.tools]}")
        
        # Switch to company
        agent.set_user_type("company")
        print(f"\n✅ Switched to: company")
        print(f"   Tools: {[tool.name for tool in agent.tools]}")
        
        # Verify tools changed
        tool_names = [tool.name for tool in agent.tools]
        if "search_candidates" in tool_names:
            print("   ✅ Company tools loaded correctly")
        else:
            print("   ❌ Company tools not loaded")
        
        print("\n✅ User type switching test completed")
        
    except Exception as e:
        print(f"\n❌ Error in user type switching: {str(e)}")
        import traceback
        traceback.print_exc()


def main():
    """Run all tests."""
    print("\n🧪 Testing Phase 5: Enhanced Agent with Tools")
    print("=" * 70)
    
    # Check environment
    if not os.getenv("OLLAMA_API_KEY"):
        print("❌ OLLAMA_API_KEY not found in environment")
        print("   Please set it in .env file")
        return
    
    print("✅ Environment configured")
    
    # Run tests
    test_tool_selection()
    test_user_type_switching()
    
    print("\n" + "=" * 70)
    print("⚠️  Note: Full conversation tests require MongoDB and Voyage AI")
    print("   Run the CLI to test complete flows: python -m src.job_portal.cli.main start")
    print("=" * 70)
    
    # Optionally run conversation tests if user confirms
    print("\n💡 To test full conversations with tool calls:")
    print("   1. Ensure MongoDB is connected")
    print("   2. Ensure Voyage AI API key is set")
    print("   3. Run: python -m src.job_portal.cli.main start")


if __name__ == "__main__":
    main()
