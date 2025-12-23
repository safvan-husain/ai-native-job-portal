"""Seed sample data with real embeddings and rich descriptions."""
from pathlib import Path
import sys
import time
import os
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

# Load environment variables
load_dotenv(ROOT / ".env")

from job_portal import MongoDBConnection, CompanyStore, JobSeekerStore
from job_portal.services.embeddings.job_portal_embeddings import JobPortalEmbeddings


def seed_companies(embeddings_service: JobPortalEmbeddings):
    """Insert sample company job postings with real embeddings."""
    print("Seeding company data...")
    
    with MongoDBConnection(database_name="job_portal") as conn:
        company_store = CompanyStore(conn.get_collection("companies"))
        
        # Rich company descriptions with culture, values, and detailed requirements
        companies_data = [
            {
                "company_id": "comp_001",
                "company_name": "TechCorp",
                "job_title": "Senior Python Developer",
                "job_description": """We're a Series B startup that recently raised $150M, building the future of cloud infrastructure. 
                Our founders come from Google and AWS, bringing deep technical expertise and a vision for developer-first tools.
                
                We believe in work-life balance and sustainable pace - no hero culture here. Our team collaborates openly, 
                shares knowledge freely, and celebrates learning from failures. We offer competitive equity (0.15-0.3%), 
                unlimited PTO, and a $5K annual learning budget.
                
                You'll work on distributed systems that handle millions of requests per second, mentoring junior developers 
                and shaping our technical direction. We value clean code, thorough testing, and pragmatic solutions over 
                perfect architecture. Our tech stack includes Python, Django, PostgreSQL, Redis, and Kubernetes.
                
                We're looking for someone who thrives in ambiguity, asks great questions, and can balance speed with quality. 
                6+ years of Python experience required, with strong fundamentals in databases, APIs, and system design.""",
                "company_size": "51-200",
                "location": "San Francisco, CA",
                "industry": "Technology",
                "remote_policy": "hybrid",
                "required_skills": ["Python", "Django", "PostgreSQL", "Redis", "Kubernetes"],
                "experience_level": "senior",
                "salary_range": {"min": 140000, "max": 190000}
            },
            {
                "company_id": "comp_002",
                "company_name": "DataCo",
                "job_title": "Machine Learning Engineer",
                "job_description": """Join a profitable, bootstrapped company that's been growing 100% YoY for 3 years. 
                Our founder is a Stanford PhD who previously led ML teams at Meta. We're building AI-powered analytics 
                that help enterprises make data-driven decisions.
                
                We value deep work and focus time - meetings are rare and always optional. Everyone has ownership of their 
                projects from conception to production. We're fully remote with team members across 15 countries, and we 
                gather twice a year for company retreats in amazing locations.
                
                You'll build production ML systems that process billions of data points daily. We need someone comfortable 
                with the full ML lifecycle: data pipelines, model training, deployment, monitoring, and iteration. 
                Experience with transformers, recommendation systems, or time series forecasting is a plus.
                
                We're looking for curious problem-solvers who can communicate complex ideas simply and aren't afraid to 
                challenge assumptions. 4+ years of ML experience, strong Python skills, and production deployment experience required.""",
                "company_size": "201-500",
                "location": "New York, NY",
                "industry": "Technology",
                "remote_policy": "remote",
                "required_skills": ["Python", "TensorFlow", "PyTorch", "MLOps", "Data Pipelines"],
                "experience_level": "mid",
                "salary_range": {"min": 150000, "max": 210000}
            },
            {
                "company_id": "comp_003",
                "company_name": "StartupXYZ",
                "job_title": "Full Stack Developer",
                "job_description": """We're a pre-seed startup (just raised $2M from Y Combinator) building tools for 
                content creators. Our founding team includes a former YouTube product manager and a successful creator 
                with 2M followers who deeply understands the pain points.
                
                We move fast and ship daily. You'll have massive impact - your code will reach thousands of users within 
                weeks. We're scrappy, resourceful, and believe in building MVPs to validate ideas quickly. Equity package 
                is generous (0.5-1.5%) because we want everyone to feel like an owner.
                
                The environment is high-energy and collaborative. We do pair programming, code reviews, and weekly demos. 
                We're building with modern tools: React, Next.js, Node.js, TypeScript, and MongoDB. You'll work across 
                the entire stack, from UI/UX to APIs to database design.
                
                Looking for someone who's excited by ambiguity, can wear multiple hats, and wants to help shape company 
                culture from day one. 3+ years of full stack experience, strong JavaScript fundamentals, and a portfolio 
                of shipped projects required.""",
                "company_size": "11-50",
                "location": "Austin, TX",
                "industry": "Technology",
                "remote_policy": "hybrid",
                "required_skills": ["JavaScript", "React", "Node.js", "TypeScript", "MongoDB"],
                "experience_level": "mid",
                "salary_range": {"min": 100000, "max": 150000}
            },
            {
                "company_id": "comp_004",
                "company_name": "FinanceAI",
                "job_title": "Senior Backend Engineer",
                "job_description": """We're a well-established fintech company (Series D, $1B valuation) revolutionizing 
                personal finance. Our co-founders are former Goldman Sachs engineers who saw how technology could democratize 
                financial services. We serve 5M+ users and process $10B+ in transactions annually.
                
                We have a strong engineering culture with high standards. Code quality matters - we do thorough reviews, 
                maintain 90%+ test coverage, and invest in tooling and infrastructure. We believe in sustainable pace: 
                40-hour weeks, no on-call for most teams, and generous parental leave (6 months).
                
                You'll work on critical financial systems requiring high reliability, security, and performance. We use 
                Go, Python, PostgreSQL, and AWS. Experience with financial systems, payment processing, or regulatory 
                compliance is valuable but not required - we'll teach you.
                
                We want thoughtful engineers who sweat the details, communicate proactively, and take pride in their craft. 
                Someone who can design robust systems, mentor others, and contribute to technical strategy. 7+ years of 
                backend experience with strong fundamentals in distributed systems.""",
                "company_size": "201-500",
                "location": "Remote",
                "industry": "Fintech",
                "remote_policy": "remote",
                "required_skills": ["Go", "Python", "PostgreSQL", "AWS", "Distributed Systems"],
                "experience_level": "senior",
                "salary_range": {"min": 160000, "max": 220000}
            }
        ]
        
        print("  Generating embeddings for job postings (this may take a few minutes due to rate limits)...")
        
        for i, company_data in enumerate(companies_data):
            # Generate embedding for job description
            print(f"  Processing {i+1}/{len(companies_data)}: {company_data['job_title']} at {company_data['company_name']}...")
            
            embedding = embeddings_service.embed_job_posting(
                job_title=company_data["job_title"],
                job_description=company_data["job_description"],
                required_skills=company_data["required_skills"],
                experience_level=company_data["experience_level"]
            )
            company_data["job_requirements_embedding"] = embedding
            
            job_id = company_store.store_job_posting(**company_data)
            print(f"    ✓ Created with real embedding")
            
            # Rate limit: wait 25 seconds between requests (3 RPM = 20s, add buffer)
            if i < len(companies_data) - 1:
                print(f"    ⏳ Waiting 25s for rate limit...")
                time.sleep(25)
        
        print(f"✓ Seeded {len(companies_data)} job postings with real embeddings")


def seed_job_seekers(embeddings_service: JobPortalEmbeddings):
    """Insert sample job seeker profiles with real embeddings."""
    print("\nSeeding job seeker data...")
    
    with MongoDBConnection(database_name="job_portal") as conn:
        jobseeker_store = JobSeekerStore(conn.get_collection("job_seekers"))
        
        # Rich job seeker profiles with personality, values, and detailed backgrounds
        seekers_data = [
            {
                "user_id": "user_001",
                "name": "Alice Johnson",
                "profile_summary": """I'm a senior software engineer with 6 years building scalable web applications. 
                Started my career at a large enterprise where I learned the importance of testing and documentation, 
                then moved to a startup where I discovered my love for moving fast and owning features end-to-end.
                
                I thrive in environments where people trust each other and aren't afraid to admit when they don't know 
                something. I value mentorship - both giving and receiving - and believe the best teams are those where 
                everyone is constantly learning. I'm looking for a place where work-life balance isn't just a buzzword, 
                where I can do deep work without constant interruptions, and where technical excellence is celebrated.
                
                My sweet spot is backend systems with Python and Django, but I'm comfortable across the stack. I've built 
                REST APIs serving millions of requests, optimized database queries that were killing production, and 
                mentored junior developers through their first major projects. I care deeply about code quality but know 
                when to ship something imperfect to learn faster.
                
                I'm drawn to companies with strong technical leadership, clear product vision, and meaningful equity. 
                I want to work on problems that matter, with people who challenge me to grow. Bonus points if there's 
                a learning budget and opportunities to attend conferences.""",
                "years_of_experience": 6.0,
                "skills": ["Python", "Django", "PostgreSQL", "Redis", "React", "AWS"],
                "desired_location": "San Francisco, CA",
                "desired_remote_policy": "hybrid",
                "desired_salary_min": 140000,
                "education_level": "bachelors",
                "current_title": "Senior Software Engineer",
                "industries_of_interest": ["Technology", "SaaS"]
            },
            {
                "user_id": "user_002",
                "name": "Bob Smith",
                "profile_summary": """Machine learning engineer with 4 years taking models from research to production. 
                I have a Master's in Computer Science with a focus on deep learning, but I'm more excited about solving 
                real problems than publishing papers. I've built recommendation systems, fraud detection models, and 
                NLP pipelines that actually ship to users.
                
                I'm looking for a fully remote role where I can focus on deep work. I do my best thinking in long, 
                uninterrupted blocks, and I've found that remote work gives me that space. I value async communication, 
                clear documentation, and teams that respect different working styles and time zones.
                
                What matters to me: working on ML problems that have real impact, not just incremental improvements to 
                vanity metrics. I want to be somewhere that values the full ML lifecycle - not just model training, but 
                data quality, monitoring, and iteration. I'm comfortable with ambiguity and can figure things out 
                independently, but I also know when to ask for help.
                
                I'm drawn to companies that are profitable or have strong fundamentals - I've seen too many friends 
                laid off from overfunded startups. I want stability, interesting technical challenges, and the freedom 
                to work from anywhere. I'm open to mentoring others and contributing to technical strategy.""",
                "years_of_experience": 4.0,
                "skills": ["Python", "TensorFlow", "PyTorch", "MLOps", "Data Engineering", "AWS"],
                "desired_location": "Remote",
                "desired_remote_policy": "remote",
                "desired_salary_min": 150000,
                "education_level": "masters",
                "current_title": "ML Engineer",
                "industries_of_interest": ["Technology", "AI/ML"]
            },
            {
                "user_id": "user_003",
                "name": "Carol Davis",
                "profile_summary": """Full stack developer with 3.5 years, all at early-stage startups. I love the 
                energy and impact of small teams where everyone wears multiple hats. I've been employee #5 at two 
                companies, which taught me how to move fast, make decisions with incomplete information, and ship 
                features that users actually want.
                
                I'm looking for another early-stage opportunity where I can have massive impact and help shape the 
                product and culture. I want to work with founders who are technical, who understand the market deeply, 
                and who communicate transparently. I'm excited by generous equity packages because I want to feel like 
                a true owner, not just an employee.
                
                My strength is shipping quickly without sacrificing too much quality. I can build a feature from Figma 
                mockup to production in days, not weeks. I'm comfortable with React, Node.js, TypeScript, and modern 
                tooling. I've done everything from implementing pixel-perfect UIs to designing database schemas to 
                setting up CI/CD pipelines.
                
                I thrive in high-energy, collaborative environments. I love pair programming, brainstorming sessions, 
                and the feeling of shipping something and immediately getting user feedback. I'm looking for a hybrid 
                setup in Austin where I can be in the office a few days a week for that in-person energy, but also 
                have flexibility to focus at home when needed.""",
                "years_of_experience": 3.5,
                "skills": ["JavaScript", "TypeScript", "React", "Node.js", "MongoDB", "Next.js"],
                "desired_location": "Austin, TX",
                "desired_remote_policy": "hybrid",
                "desired_salary_min": 110000,
                "education_level": "bachelors",
                "current_title": "Full Stack Developer",
                "industries_of_interest": ["Technology", "Startup"]
            },
            {
                "user_id": "user_004",
                "name": "David Chen",
                "profile_summary": """Backend engineer with 8 years building reliable, high-scale systems. I started 
                in finance where I learned that correctness and reliability aren't optional - they're the baseline. 
                I've worked on payment systems, trading platforms, and infrastructure that can't go down.
                
                I'm looking for a senior role at a mature company with strong engineering practices. I want to work 
                somewhere that values doing things right: comprehensive testing, thorough code reviews, proper monitoring, 
                and incident postmortems that lead to actual improvements. I'm tired of startups that cut corners and 
                accumulate technical debt they never pay back.
                
                I care about sustainable pace and work-life balance. I have a family and I want to be present for them. 
                I'm looking for a 40-hour week, no on-call if possible, and generous parental leave policies. I'm happy 
                to work hard during those hours, but I need clear boundaries.
                
                My expertise is in Go and Python for backend services, PostgreSQL for databases, and AWS for infrastructure. 
                I've designed systems that handle millions of transactions, optimized performance bottlenecks, and mentored 
                teams on best practices. I want to work somewhere that values my experience and gives me autonomy to make 
                technical decisions. Fully remote is ideal - I'm based in Seattle but open to working with teams anywhere.""",
                "years_of_experience": 8.0,
                "skills": ["Go", "Python", "PostgreSQL", "AWS", "Distributed Systems", "Kubernetes"],
                "desired_location": "Remote",
                "desired_remote_policy": "remote",
                "desired_salary_min": 170000,
                "education_level": "bachelors",
                "current_title": "Senior Backend Engineer",
                "industries_of_interest": ["Fintech", "Technology"]
            }
        ]
        
        print("  Generating embeddings for candidate profiles (this may take a few minutes due to rate limits)...")
        
        for i, seeker_data in enumerate(seekers_data):
            print(f"  Processing {i+1}/{len(seekers_data)}: {seeker_data['name']}...")
            
            # Generate embedding for profile
            embedding = embeddings_service.embed_candidate_profile(
                name=seeker_data["name"],
                current_title=seeker_data["current_title"],
                profile_summary=seeker_data["profile_summary"],
                skills=seeker_data["skills"],
                years_of_experience=seeker_data["years_of_experience"],
                education=seeker_data["education_level"]
            )
            seeker_data["profile_embedding"] = embedding
            
            profile_id = jobseeker_store.store_profile(**seeker_data)
            print(f"    ✓ Created with real embedding")
            
            # Rate limit: wait 25 seconds between requests (3 RPM = 20s, add buffer)
            if i < len(seekers_data) - 1:
                print(f"    ⏳ Waiting 25s for rate limit...")
                time.sleep(25)
        
        print(f"✓ Seeded {len(seekers_data)} job seeker profiles with real embeddings")


def verify_data():
    """Verify seeded data."""
    print("\nVerifying data...")
    
    with MongoDBConnection(database_name="job_portal") as conn:
        companies_count = conn.get_collection("companies").count_documents({})
        seekers_count = conn.get_collection("job_seekers").count_documents({})
        
        print(f"  Companies: {companies_count} documents")
        print(f"  Job Seekers: {seekers_count} documents")
        
        # Show sample
        print("\nSample company:")
        sample_company = conn.get_collection("companies").find_one()
        if sample_company:
            print(f"  {sample_company['job_title']} at {sample_company['company_name']}")
        
        print("\nSample job seeker:")
        sample_seeker = conn.get_collection("job_seekers").find_one()
        if sample_seeker:
            print(f"  {sample_seeker['name']} - {sample_seeker['current_title']}")


if __name__ == "__main__":
    print("=" * 60)
    print("Seeding Sample Data with Real Embeddings")
    print("=" * 60)
    print()
    print("⚠️  This will take several minutes due to rate limits (3 RPM)")
    print("    Total API calls needed: 8 (4 companies + 4 job seekers)")
    print("    Estimated time: ~3 minutes")
    print()
    
    # Initialize embeddings service
    print("Initializing embeddings service...")
    embeddings_service = JobPortalEmbeddings()
    print("✓ Embeddings service ready")
    print()
    
    seed_companies(embeddings_service)
    
    # Wait before processing job seekers to avoid rate limit
    print("\n⏳ Waiting 30 seconds before processing job seekers...")
    time.sleep(30)
    
    seed_job_seekers(embeddings_service)
    verify_data()
    
    print("\n" + "=" * 60)
    print("✓ Sample data seeded successfully with real embeddings!")
    print("\nNext steps:")
    print("  1. Run matching tests: python scripts/maintenance/test_matching.py")
    print("  2. Try the demo: python scripts/demos/example_with_embeddings.py")
    print("=" * 60)
