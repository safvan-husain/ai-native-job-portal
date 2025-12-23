"""Demo script to test tools directly (without agent)."""
import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.job_portal.agent.tools import (
    search_jobs,
    get_company_details,
    compare_companies,
    search_candidates,
    get_candidate_details,
    compare_candidates
)


def test_job_seeker_tools():
    """Test job seeker tools."""
    print("=" * 70)
    print("TESTING JOB SEEKER TOOLS")
    print("=" * 70)
    
    # Test 1: Search for jobs
    print("\n1. Searching for Python developer jobs...")
    print("-" * 70)
    result = search_jobs.invoke({
        "requirements": "Python developer with Django experience, 3-5 years",
        "limit": 3
    })
    print(result)
    
    # Extract first company ID from results (if any)
    if "ID:" in result:
        lines = result.split('\n')
        company_id = None
        for line in lines:
            if "ID:" in line:
                company_id = line.split("ID:")[1].strip()
                break
        
        if company_id:
            # Test 2: Get company details
            print("\n2. Getting details for first company...")
            print("-" * 70)
            details = get_company_details.invoke({"company_id": company_id})
            print(details)
            
            # Test 3: Compare companies (if we have multiple)
            print("\n3. Comparing companies...")
            print("-" * 70)
            # For demo, we'll just show the message about needing 2+ IDs
            compare_result = compare_companies.invoke({"company_ids": company_id})
            print(compare_result)


def test_company_tools():
    """Test company tools."""
    print("\n\n" + "=" * 70)
    print("TESTING COMPANY TOOLS")
    print("=" * 70)
    
    # Test 1: Search for candidates
    print("\n1. Searching for Python developer candidates...")
    print("-" * 70)
    result = search_candidates.invoke({
        "job_requirements": "Senior Python developer with ML experience",
        "limit": 3
    })
    print(result)
    
    # Extract first candidate ID from results (if any)
    if "ID:" in result:
        lines = result.split('\n')
        candidate_id = None
        for line in lines:
            if "ID:" in line:
                candidate_id = line.split("ID:")[1].strip()
                break
        
        if candidate_id:
            # Test 2: Get candidate details
            print("\n2. Getting details for first candidate...")
            print("-" * 70)
            details = get_candidate_details.invoke({"candidate_id": candidate_id})
            print(details)
            
            # Test 3: Compare candidates (if we have multiple)
            print("\n3. Comparing candidates...")
            print("-" * 70)
            # For demo, we'll just show the message about needing 2+ IDs
            compare_result = compare_candidates.invoke({"candidate_ids": candidate_id})
            print(compare_result)


def test_tool_schemas():
    """Test that tools have proper LangChain schemas."""
    print("\n\n" + "=" * 70)
    print("TESTING TOOL SCHEMAS")
    print("=" * 70)
    
    tools = [
        search_jobs,
        get_company_details,
        compare_companies,
        search_candidates,
        get_candidate_details,
        compare_candidates
    ]
    
    for tool in tools:
        print(f"\n{tool.name}:")
        print(f"  Description: {tool.description[:100]}...")
        print(f"  Has schema: {hasattr(tool, 'args_schema')}")


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("TOOL TESTING DEMO")
    print("=" * 70)
    print("\nThis script tests all 6 tools independently (without agent).")
    print("Make sure you have:")
    print("  - MONGODB_URI in .env")
    print("  - VOYAGE_API_KEY in .env")
    print("  - Sample data in MongoDB")
    print("=" * 70)
    
    try:
        # Test job seeker tools
        test_job_seeker_tools()
        
        # Test company tools
        test_company_tools()
        
        # Test schemas
        test_tool_schemas()
        
        print("\n\n" + "=" * 70)
        print("ALL TESTS COMPLETED!")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n\nERROR: {e}")
        print("\nMake sure:")
        print("  1. MongoDB is connected")
        print("  2. Sample data exists in database")
        print("  3. Environment variables are set")
        import traceback
        traceback.print_exc()
