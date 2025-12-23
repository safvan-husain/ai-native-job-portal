"""
Quick verification script for Phase 5 implementation.
Checks that all components are properly integrated.
"""

import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent.parent.parent / "src"
sys.path.insert(0, str(src_path))

def verify_imports():
    """Verify all required imports work."""
    print("🔍 Verifying imports...")
    
    try:
        from job_portal.agent.simple_agent import SimpleAgent, JobPortalState
        print("  ✅ SimpleAgent and JobPortalState")
    except ImportError as e:
        print(f"  ❌ SimpleAgent import failed: {e}")
        return False
    
    try:
        from job_portal.agent.prompts import get_system_prompt_with_tools
        print("  ✅ get_system_prompt_with_tools")
    except ImportError as e:
        print(f"  ❌ Prompts import failed: {e}")
        return False
    
    try:
        from job_portal.agent.tools import (
            search_jobs, get_company_details, compare_companies,
            search_candidates, get_candidate_details, compare_candidates
        )
        print("  ✅ All 6 tools")
    except ImportError as e:
        print(f"  ❌ Tools import failed: {e}")
        return False
    
    try:
        from job_portal.cli.session import SessionState
        print("  ✅ SessionState")
    except ImportError as e:
        print(f"  ❌ SessionState import failed: {e}")
        return False
    
    return True


def verify_agent_features():
    """Verify agent has required features."""
    print("\n🔍 Verifying agent features...")
    
    from job_portal.agent.simple_agent import SimpleAgent
    
    # Check agent can be created
    try:
        agent = SimpleAgent(user_type="job_seeker")
        print("  ✅ Agent creation")
    except Exception as e:
        print(f"  ❌ Agent creation failed: {e}")
        return False
    
    # Check tools are bound
    if hasattr(agent, 'tools') and len(agent.tools) > 0:
        print(f"  ✅ Tools bound ({len(agent.tools)} tools)")
    else:
        print("  ❌ No tools bound")
        return False
    
    # Check tool names
    tool_names = [tool.name for tool in agent.tools]
    expected = ["search_jobs", "get_company_details", "compare_companies"]
    if all(name in tool_names for name in expected):
        print(f"  ✅ Correct tools for job_seeker")
    else:
        print(f"  ❌ Wrong tools: {tool_names}")
        return False
    
    # Check user type switching
    try:
        agent.set_user_type("company")
        tool_names = [tool.name for tool in agent.tools]
        if "search_candidates" in tool_names:
            print("  ✅ User type switching works")
        else:
            print("  ❌ User type switching failed")
            return False
    except Exception as e:
        print(f"  ❌ User type switching error: {e}")
        return False
    
    return True


def verify_state_management():
    """Verify state management features."""
    print("\n🔍 Verifying state management...")
    
    from job_portal.cli.session import SessionState
    
    # Create session
    try:
        session = SessionState(session_id="test")
        print("  ✅ SessionState creation")
    except Exception as e:
        print(f"  ❌ SessionState creation failed: {e}")
        return False
    
    # Check new fields exist
    required_fields = [
        'user_type', 'conversation_history', 'selected_items',
        'search_results', 'comparison_mode', 'last_tool_call'
    ]
    
    for field in required_fields:
        if hasattr(session, field):
            print(f"  ✅ Field: {field}")
        else:
            print(f"  ❌ Missing field: {field}")
            return False
    
    # Check new methods exist
    required_methods = [
        'set_comparison_mode', 'record_tool_call', 'add_search_results'
    ]
    
    for method in required_methods:
        if hasattr(session, method):
            print(f"  ✅ Method: {method}")
        else:
            print(f"  ❌ Missing method: {method}")
            return False
    
    return True


def verify_prompts():
    """Verify prompts have tool instructions."""
    print("\n🔍 Verifying prompts...")
    
    from job_portal.agent.prompts import get_system_prompt_with_tools
    
    # Check job seeker prompt
    prompt = get_system_prompt_with_tools("job_seeker")
    if "search_jobs" in prompt and "Available Tools" in prompt:
        print("  ✅ Job seeker prompt has tool instructions")
    else:
        print("  ❌ Job seeker prompt missing tool instructions")
        return False
    
    # Check company prompt
    prompt = get_system_prompt_with_tools("company")
    if "search_candidates" in prompt and "Available Tools" in prompt:
        print("  ✅ Company prompt has tool instructions")
    else:
        print("  ❌ Company prompt missing tool instructions")
        return False
    
    return True


def main():
    """Run all verifications."""
    print("=" * 70)
    print("Phase 5 Verification")
    print("=" * 70)
    
    results = []
    
    results.append(("Imports", verify_imports()))
    results.append(("Agent Features", verify_agent_features()))
    results.append(("State Management", verify_state_management()))
    results.append(("Prompts", verify_prompts()))
    
    print("\n" + "=" * 70)
    print("Summary")
    print("=" * 70)
    
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {name}")
    
    all_passed = all(result[1] for result in results)
    
    print("\n" + "=" * 70)
    if all_passed:
        print("🎉 All verifications passed!")
        print("Phase 5 implementation is complete and working.")
    else:
        print("⚠️  Some verifications failed.")
        print("Please check the errors above.")
    print("=" * 70)
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
