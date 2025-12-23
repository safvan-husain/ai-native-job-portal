"""Example usage of the job portal vector database."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from job_portal import MongoDBConnection, CompanyStore, JobSeekerStore


def example_company_operations():
    """Example: Company storing job postings and searching for candidates."""
    
    # Connect to MongoDB
    with MongoDBConnection() as conn:
        # Get company collection and initialize store
        company_collection = conn.get_collection("companies")
        company_store = CompanyStore(company_collection)
        
        # Example: Store a job posting
        job_embedding = [0.1] * 1024  # Replace with actual embedding from your model
        
        job_id = company_store.store_job_posting(
            company_id="comp_123",
            company_name="TechCorp Inc",
            job_title="Senior Python Developer",
            job_description="We are looking for an experienced Python developer...",
            job_requirements_embedding=job_embedding,
            company_size="51-200",
            location="San Francisco, CA",
            industry="Technology",
            salary_range={"min": 120000, "max": 180000},
            remote_policy="hybrid",
            required_skills=["Python", "Django", "PostgreSQL", "Docker"],
            experience_level="senior"
        )
        print(f"Stored job posting: {job_id}")
        
        # Example: Search for matching candidates
        candidate_embedding = [0.15] * 1024  # Candidate's profile embedding
        
        matches = company_store.search_matching_candidates(
            candidate_profile_embedding=candidate_embedding,
            location="San Francisco",
            remote_policy="hybrid",
            experience_level="senior",
            limit=5
        )
        
        print(f"\nFound {len(matches)} matching candidates:")
        for match in matches:
            print(f"  - Score: {match['score']:.4f}, Job: {match['job_title']}")
        
        # Example: Filter jobs by metadata only
        filtered_jobs = company_store.filter_by_metadata(
            industry="Technology",
            remote_policy="hybrid",
            salary_min=100000,
            limit=10
        )
        print(f"\nFiltered {len(filtered_jobs)} jobs by metadata")


def example_jobseeker_operations():
    """Example: Job seeker storing profile and searching for jobs."""
    
    # Connect to MongoDB
    with MongoDBConnection() as conn:
        # Get job seeker collection and initialize store
        jobseeker_collection = conn.get_collection("jobseekers")
        jobseeker_store = JobSeekerStore(jobseeker_collection)
        
        # Example: Store a job seeker profile
        profile_embedding = [0.2] * 1024  # Replace with actual embedding
        
        profile_id = jobseeker_store.store_profile(
            user_id="user_456",
            name="Jane Doe",
            profile_summary="Experienced Python developer with 5 years in web development...",
            profile_embedding=profile_embedding,
            years_of_experience=5.0,
            skills=["Python", "Django", "React", "PostgreSQL", "AWS"],
            desired_location="San Francisco, CA",
            desired_remote_policy="hybrid",
            desired_salary_min=120000,
            education_level="bachelors",
            current_title="Senior Software Engineer",
            industries_of_interest=["Technology", "FinTech"],
            availability="2_weeks"
        )
        print(f"Stored job seeker profile: {profile_id}")
        
        # Example: Search for matching jobs
        job_requirements_embedding = [0.18] * 1024  # Job requirements embedding
        
        matches = jobseeker_store.search_matching_jobs(
            job_requirements_embedding=job_requirements_embedding,
            min_experience=3.0,
            max_experience=7.0,
            required_skills=["Python", "Django"],
            location="San Francisco",
            remote_policy="hybrid",
            limit=5
        )
        
        print(f"\nFound {len(matches)} matching jobs:")
        for match in matches:
            print(f"  - Score: {match['score']:.4f}, Candidate: {match['name']}")
        
        # Example: Get profile by user ID
        profile = jobseeker_store.get_profile_by_user("user_456")
        if profile:
            print(f"\nRetrieved profile: {profile['name']}")
        
        # Example: Update profile status
        success = jobseeker_store.update_profile_status(profile_id, "hired")
        print(f"Profile status updated: {success}")


def example_hybrid_search():
    """Example: Advanced hybrid search combining vectors and filters."""
    
    with MongoDBConnection() as conn:
        company_collection = conn.get_collection("companies")
        company_store = CompanyStore(company_collection)
        
        # Hybrid search: Vector similarity + strict metadata filters
        query_embedding = [0.12] * 1024
        
        results = company_store.hybrid_search(
            query_vector=query_embedding,
            filter_criteria={
                "status": "active",
                "company_size": {"$in": ["51-200", "201-500"]},
                "remote_policy": {"$ne": "onsite"},
                "salary_range.max": {"$gte": 150000}
            },
            limit=10,
            num_candidates=100
        )
        
        print(f"Hybrid search found {len(results)} results")


if __name__ == "__main__":
    print("=== Company Operations ===")
    example_company_operations()
    
    print("\n=== Job Seeker Operations ===")
    example_jobseeker_operations()
    
    print("\n=== Hybrid Search ===")
    example_hybrid_search()
