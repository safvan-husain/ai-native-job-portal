"""Example usage of job portal with real Voyage AI embeddings."""
from pathlib import Path
import sys

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from job_portal import (
    MongoDBConnection,
    CompanyStore,
    JobSeekerStore,
    JobPortalEmbeddings,
)

# Load environment variables
load_dotenv()


def main():
    """Demonstrate job portal with real embeddings."""
    
    # Initialize embedding service
    print("🚀 Initializing Voyage AI Embedding Service...")
    embeddings = JobPortalEmbeddings()
    
    # Connect to MongoDB
    print("📊 Connecting to MongoDB Atlas...")
    with MongoDBConnection() as db:
        # Initialize stores
        company_store = CompanyStore(db["companies"])
        jobseeker_store = JobSeekerStore(db["job_seekers"])
        
        print("\n" + "="*60)
        print("EXAMPLE 1: Store Job Posting with Real Embeddings")
        print("="*60)
        
        # Generate embedding for job posting
        job_embedding = embeddings.embed_job_posting(
            job_title="Senior Python Developer",
            job_description=(
                "We are seeking an experienced Python developer to join our backend team. "
                "You will work on building scalable APIs, optimizing database queries, "
                "and implementing new features for our SaaS platform. "
                "Strong experience with Django or FastAPI is required."
            ),
            required_skills=["Python", "Django", "FastAPI", "PostgreSQL", "REST APIs"],
            experience_level="senior"
        )
        
        print(f"✅ Generated job embedding (dimension: {len(job_embedding)})")
        print(f"   First 5 values: {job_embedding[:5]}")
        
        # Store job posting
        job_id = company_store.store_job_posting(
            company_id="techcorp_001",
            company_name="TechCorp Inc.",
            job_title="Senior Python Developer",
            job_description="Build scalable backend systems with Python",
            job_requirements_embedding=job_embedding,
            company_size="51-200",
            location="San Francisco, CA",
            industry="Technology",
            remote_policy="hybrid",
            required_skills=["Python", "Django", "FastAPI", "PostgreSQL"],
            experience_level="senior",
            salary_range={"min": 120000, "max": 160000}
        )
        
        print(f"✅ Stored job posting with ID: {job_id}")
        
        print("\n" + "="*60)
        print("EXAMPLE 2: Store Candidate Profile with Real Embeddings")
        print("="*60)
        
        # Generate embedding for candidate profile
        candidate_embedding = embeddings.embed_candidate_profile(
            name="Alice Johnson",
            current_title="Senior Software Engineer",
            profile_summary=(
                "Experienced Python developer with 6 years of building web applications. "
                "Specialized in Django and FastAPI frameworks. Strong background in "
                "database optimization and API design. Passionate about clean code and testing."
            ),
            skills=["Python", "Django", "FastAPI", "PostgreSQL", "Redis", "Docker"],
            years_of_experience=6.0,
            education="Bachelor's in Computer Science"
        )
        
        print(f"✅ Generated candidate embedding (dimension: {len(candidate_embedding)})")
        print(f"   First 5 values: {candidate_embedding[:5]}")
        
        # Store candidate profile
        profile_id = jobseeker_store.store_profile(
            user_id="alice_001",
            name="Alice Johnson",
            profile_summary="Senior Python developer with 6 years experience",
            profile_embedding=candidate_embedding,
            years_of_experience=6.0,
            skills=["Python", "Django", "FastAPI", "PostgreSQL", "Redis", "Docker"],
            desired_location="San Francisco, CA",
            desired_remote_policy="hybrid",
            education_level="bachelors",
            current_title="Senior Software Engineer",
            industries_of_interest=["Technology", "Fintech"],
            desired_salary_min=110000
        )
        
        print(f"✅ Stored candidate profile with ID: {profile_id}")
        
        print("\n" + "="*60)
        print("EXAMPLE 3: Search for Matching Jobs (Candidate Perspective)")
        print("="*60)
        
        # Generate search query embedding
        search_query = embeddings.embed_job_search_query(
            desired_role="Python Backend Developer",
            desired_skills=["Python", "Django", "APIs"],
            experience_level="senior",
            additional_preferences="Prefer hybrid or remote work in San Francisco"
        )
        
        print("🔍 Searching for jobs matching candidate profile...")
        
        # Search for matching jobs
        matching_jobs = company_store.search_matching_candidates(
            candidate_profile_embedding=search_query,
            location="San Francisco",
            remote_policy="hybrid",
            limit=5
        )
        
        print(f"\n✅ Found {len(matching_jobs)} matching jobs:")
        for i, job in enumerate(matching_jobs, 1):
            print(f"\n{i}. {job['job_title']} at {job['company_name']}")
            print(f"   Location: {job['location']}")
            print(f"   Remote: {job['remote_policy']}")
            print(f"   Similarity Score: {job.get('score', 'N/A'):.4f}")
        
        print("\n" + "="*60)
        print("EXAMPLE 4: Search for Matching Candidates (Company Perspective)")
        print("="*60)
        
        # Generate candidate search query
        candidate_search = embeddings.embed_candidate_search_query(
            job_title="Senior Python Developer",
            required_skills=["Python", "Django", "PostgreSQL"],
            experience_level="senior",
            additional_requirements="Looking for candidates with API development experience"
        )
        
        print("🔍 Searching for candidates matching job requirements...")
        
        # Search for matching candidates
        matching_candidates = jobseeker_store.search_matching_jobs(
            job_requirements_embedding=candidate_search,
            min_experience=4.0,
            required_skills=["Python", "Django"],
            location="San Francisco",
            limit=5
        )
        
        print(f"\n✅ Found {len(matching_candidates)} matching candidates:")
        for i, candidate in enumerate(matching_candidates, 1):
            print(f"\n{i}. {candidate['name']} - {candidate['current_title']}")
            print(f"   Experience: {candidate['years_of_experience']} years")
            print(f"   Skills: {', '.join(candidate['skills'][:5])}")
            print(f"   Similarity Score: {candidate.get('score', 'N/A'):.4f}")
        
        print("\n" + "="*60)
        print("EXAMPLE 5: Hybrid Search with Filters")
        print("="*60)
        
        print("🔍 Searching with vector similarity + metadata filters...")
        
        # Hybrid search: vector similarity + strict filters
        filtered_jobs = company_store.search_matching_candidates(
            candidate_profile_embedding=candidate_embedding,
            location="San Francisco",
            remote_policy="hybrid",
            experience_level="senior",
            industry="Technology",
            limit=10
        )
        
        print(f"\n✅ Found {len(filtered_jobs)} jobs matching all criteria:")
        for job in filtered_jobs:
            print(f"  • {job['job_title']} at {job['company_name']}")
            print(f"    Score: {job.get('score', 'N/A'):.4f} | "
                  f"Industry: {job['industry']} | "
                  f"Remote: {job['remote_policy']}")
        
        print("\n" + "="*60)
        print("✅ All examples completed successfully!")
        print("="*60)


if __name__ == "__main__":
    main()
