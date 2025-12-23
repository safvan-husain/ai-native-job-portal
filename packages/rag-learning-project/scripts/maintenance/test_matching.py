"""Test bidirectional matching between job seekers and companies."""
from pathlib import Path
import sys
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

# Load environment variables
load_dotenv(ROOT / ".env")

from job_portal import MongoDBConnection, CompanyStore, JobSeekerStore


def test_job_seeker_finds_companies():
    """Test: Job seekers finding matching companies."""
    print("=" * 80)
    print("TEST 1: Job Seekers Finding Matching Companies")
    print("=" * 80)
    print()
    
    with MongoDBConnection(database_name="job_portal") as conn:
        company_store = CompanyStore(conn.get_collection("companies"))
        jobseeker_store = JobSeekerStore(conn.get_collection("job_seekers"))
        
        # Get all job seekers
        seekers = list(conn.get_collection("job_seekers").find({}))
        
        for seeker in seekers:
            print(f"\n{'─' * 80}")
            print(f"👤 {seeker['name']} - {seeker['current_title']}")
            print(f"   Experience: {seeker['years_of_experience']} years")
            print(f"   Location: {seeker['desired_location']}")
            print(f"   Remote: {seeker['desired_remote_policy']}")
            print(f"   Min Salary: ${seeker.get('desired_salary_min', 0):,}")
            print(f"\n   Profile snippet: {seeker['profile_summary'][:150]}...")
            print(f"\n   🔍 Searching for matching jobs...")
            
            # Search for matching jobs using the seeker's profile embedding
            matches = company_store.search_matching_candidates(
                candidate_profile_embedding=seeker['profile_embedding'],
                limit=3
            )
            
            if matches:
                print(f"\n   ✓ Found {len(matches)} matching jobs:\n")
                for i, match in enumerate(matches, 1):
                    score = match.get('score', 0)
                    print(f"   {i}. {match['job_title']} at {match['company_name']}")
                    print(f"      📊 Match Score: {score:.4f}")
                    print(f"      💰 Salary: ${match['salary_range']['min']:,} - ${match['salary_range']['max']:,}")
                    print(f"      📍 {match['location']} | {match['remote_policy']}")
                    print(f"      🏢 Company Size: {match['company_size']}")
                    print(f"      💼 Level: {match['experience_level']}")
                    print(f"      🛠️  Skills: {', '.join(match['required_skills'][:5])}")
                    
                    # Show why it matched (snippet from job description)
                    desc_snippet = match['job_description'][:200].replace('\n', ' ')
                    print(f"      📝 \"{desc_snippet}...\"")
                    print()
            else:
                print(f"   ❌ No matching jobs found")


def test_company_finds_candidates():
    """Test: Companies finding matching candidates."""
    print("\n" + "=" * 80)
    print("TEST 2: Companies Finding Matching Candidates")
    print("=" * 80)
    print()
    
    with MongoDBConnection(database_name="job_portal") as conn:
        company_store = CompanyStore(conn.get_collection("companies"))
        jobseeker_store = JobSeekerStore(conn.get_collection("job_seekers"))
        
        # Get all companies
        companies = list(conn.get_collection("companies").find({}))
        
        for company in companies:
            print(f"\n{'─' * 80}")
            print(f"🏢 {company['company_name']} - {company['job_title']}")
            print(f"   Location: {company['location']}")
            print(f"   Remote: {company['remote_policy']}")
            print(f"   Level: {company['experience_level']}")
            print(f"   Salary: ${company['salary_range']['min']:,} - ${company['salary_range']['max']:,}")
            print(f"\n   Job snippet: {company['job_description'][:150]}...")
            print(f"\n   🔍 Searching for matching candidates...")
            
            # Search for matching candidates using the job's requirements embedding
            matches = jobseeker_store.search_matching_jobs(
                job_requirements_embedding=company['requirements_embedding'],
                limit=3
            )
            
            if matches:
                print(f"\n   ✓ Found {len(matches)} matching candidates:\n")
                for i, match in enumerate(matches, 1):
                    score = match.get('score', 0)
                    print(f"   {i}. {match['name']} - {match['current_title']}")
                    print(f"      📊 Match Score: {score:.4f}")
                    print(f"      💼 Experience: {match['years_of_experience']} years")
                    print(f"      📍 {match['desired_location']} | {match['desired_remote_policy']}")
                    print(f"      💰 Min Salary: ${match.get('desired_salary_min', 0):,}")
                    print(f"      🎓 Education: {match.get('education_level', 'N/A')}")
                    print(f"      🛠️  Skills: {', '.join(match['skills'][:5])}")
                    
                    # Show why they matched (snippet from profile)
                    profile_snippet = match['profile_summary'][:200].replace('\n', ' ')
                    print(f"      📝 \"{profile_snippet}...\"")
                    print()
            else:
                print(f"   ❌ No matching candidates found")


def test_specific_matches():
    """Test specific expected matches."""
    print("\n" + "=" * 80)
    print("TEST 3: Specific Expected Matches")
    print("=" * 80)
    print()
    
    with MongoDBConnection(database_name="job_portal") as conn:
        company_store = CompanyStore(conn.get_collection("companies"))
        jobseeker_store = JobSeekerStore(conn.get_collection("job_seekers"))
        
        test_cases = [
            {
                "seeker_name": "Alice Johnson",
                "expected_company": "TechCorp",
                "reason": "Senior Python dev looking for work-life balance + equity matches TechCorp's culture"
            },
            {
                "seeker_name": "Bob Smith",
                "expected_company": "DataCo",
                "reason": "ML engineer wanting remote + profitable company matches DataCo's profile"
            },
            {
                "seeker_name": "Carol Davis",
                "expected_company": "StartupXYZ",
                "reason": "Full stack dev wanting early-stage startup + equity matches StartupXYZ"
            },
            {
                "seeker_name": "David Chen",
                "expected_company": "FinanceAI",
                "reason": "Senior backend engineer wanting mature company + work-life balance matches FinanceAI"
            }
        ]
        
        for test_case in test_cases:
            print(f"\n{'─' * 80}")
            print(f"Testing: {test_case['seeker_name']} → {test_case['expected_company']}")
            print(f"Reason: {test_case['reason']}")
            
            # Get seeker
            seeker = conn.get_collection("job_seekers").find_one({"name": test_case['seeker_name']})
            if not seeker:
                print(f"   ❌ Seeker not found: {test_case['seeker_name']}")
                continue
            
            # Search for matches
            matches = company_store.search_matching_candidates(
                candidate_profile_embedding=seeker['profile_embedding'],
                limit=5
            )
            
            # Check if expected company is in top matches
            company_names = [m['company_name'] for m in matches]
            
            if test_case['expected_company'] in company_names:
                rank = company_names.index(test_case['expected_company']) + 1
                match = matches[rank - 1]
                score = match.get('score', 0)
                print(f"   ✓ PASS: Found {test_case['expected_company']} at rank #{rank}")
                print(f"      Match Score: {score:.4f}")
                print(f"      Job: {match['job_title']}")
            else:
                print(f"   ❌ FAIL: {test_case['expected_company']} not in top 5 matches")
                print(f"      Top matches: {', '.join(company_names)}")


def print_statistics():
    """Print overall statistics."""
    print("\n" + "=" * 80)
    print("STATISTICS")
    print("=" * 80)
    print()
    
    with MongoDBConnection(database_name="job_portal") as conn:
        companies_count = conn.get_collection("companies").count_documents({})
        seekers_count = conn.get_collection("job_seekers").count_documents({})
        
        print(f"📊 Total Companies: {companies_count}")
        print(f"📊 Total Job Seekers: {seekers_count}")
        print(f"📊 Total Possible Matches: {companies_count * seekers_count}")
        
        # Check embeddings
        companies_with_embeddings = conn.get_collection("companies").count_documents({
            "requirements_embedding": {"$exists": True, "$ne": None}
        })
        seekers_with_embeddings = conn.get_collection("job_seekers").count_documents({
            "profile_embedding": {"$exists": True, "$ne": None}
        })
        
        print(f"\n✓ Companies with embeddings: {companies_with_embeddings}/{companies_count}")
        print(f"✓ Job seekers with embeddings: {seekers_with_embeddings}/{seekers_count}")


if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("BIDIRECTIONAL MATCHING TESTS")
    print("Testing vector search between job seekers and companies")
    print("=" * 80)
    
    try:
        test_job_seeker_finds_companies()
        test_company_finds_candidates()
        test_specific_matches()
        print_statistics()
        
        print("\n" + "=" * 80)
        print("✓ ALL TESTS COMPLETED")
        print("=" * 80)
        print()
        
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
