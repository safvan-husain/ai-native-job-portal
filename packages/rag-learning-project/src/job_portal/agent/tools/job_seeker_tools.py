"""LangChain tools for job seekers."""
import time
from langchain_core.tools import tool

try:
    from ...infrastructure.mongodb.connection import MongoDBConnection
    from ...repositories.company_repository import CompanyStore
    from ...services.embeddings.job_portal_embeddings import JobPortalEmbeddings
except ImportError:
    from job_portal.infrastructure.mongodb.connection import MongoDBConnection
    from job_portal.repositories.company_repository import CompanyStore
    from job_portal.services.embeddings.job_portal_embeddings import JobPortalEmbeddings


# Initialize services (lazy loading)
_db_connection = None
_company_store = None
_embeddings = None
_last_api_call = 0  # Track last API call for rate limiting


def _get_company_store() -> CompanyStore:
    """Get or create company store instance."""
    global _db_connection, _company_store
    if _company_store is None:
        _db_connection = MongoDBConnection()
        collection = _db_connection.get_collection("companies")
        _company_store = CompanyStore(collection)
    return _company_store


def _get_embeddings() -> JobPortalEmbeddings:
    """Get or create embeddings service instance."""
    global _embeddings
    if _embeddings is None:
        _embeddings = JobPortalEmbeddings()
    return _embeddings


def _handle_rate_limit():
    """Handle Voyage AI rate limiting (3 RPM)."""
    global _last_api_call
    current_time = time.time()
    time_since_last_call = current_time - _last_api_call
    
    # If less than 20 seconds since last call, wait
    if time_since_last_call < 20 and _last_api_call > 0:
        wait_time = 20 - time_since_last_call
        time.sleep(wait_time)
    
    _last_api_call = time.time()


def _format_salary(salary_range):
    """Format salary range for display."""
    if not salary_range:
        return "Not specified"
    min_sal = salary_range.get('min', 0)
    max_sal = salary_range.get('max', 0)
    return f"${min_sal:,.0f} - ${max_sal:,.0f}"


def _truncate_description(text, max_length=200):
    """Truncate description to max length."""
    if len(text) <= max_length:
        return text
    return text[:max_length].rsplit(' ', 1)[0] + "..."


@tool
def search_jobs(requirements: str, limit: int = 5) -> str:
    """
    Search for job postings that match the given requirements.
    
    Use this tool when a job seeker wants to find matching companies and job opportunities.
    The tool performs vector similarity search to find the best matches.
    
    Args:
        requirements: Job requirements as natural language text (e.g., "Python developer with 5 years experience")
        limit: Maximum number of results to return (default: 5, max: 10)
        
    Returns:
        Formatted string with matching job postings including company name, job title, 
        location, salary, and similarity score.
    """
    try:
        # Validate limit
        limit = min(max(1, limit), 10)
        
        # Handle rate limiting for Voyage AI
        _handle_rate_limit()
        
        # Generate embedding for requirements
        embeddings = _get_embeddings()
        requirements_embedding = embeddings.embed_search_query(requirements)
        
        # Search for matching companies
        company_store = _get_company_store()
        results = company_store.vector_search(
            query_vector=requirements_embedding,
            limit=limit,
            num_candidates=limit * 10,
            vector_field="requirements_embedding"
        )
        
        if not results:
            return "No matching job postings found. Try different requirements or broader search terms."
        
        # Format results with enhanced information
        output = f"🔍 Found {len(results)} matching job posting(s):\n\n"
        for i, job in enumerate(results, 1):
            score = job.get('score', 0)
            match_pct = score * 100
            
            output += f"{i}. 🏢 {job.get('company_name', 'Unknown Company')}\n"
            output += f"   💼 Job: {job.get('job_title', 'N/A')}\n"
            output += f"   📍 Location: {job.get('location', 'N/A')} | {job.get('remote_policy', 'N/A')}\n"
            output += f"   💰 Salary: {_format_salary(job.get('salary_range'))}\n"
            output += f"   📊 Experience: {job.get('experience_level', 'N/A')}\n"
            output += f"   🎯 Match: {match_pct:.1f}%\n"
            
            skills = job.get('required_skills', [])
            if skills:
                output += f"   🛠️  Skills: {', '.join(skills[:5])}\n"
            
            output += f"   🆔 ID: {job.get('_id')}\n\n"
        
        output += "💡 Use get_company_details with an ID to see full job description.\n"
        output += "💡 Use compare_companies with multiple IDs to compare opportunities.\n"
        
        return output
        
    except Exception as e:
        return f"❌ Error searching for jobs: {str(e)}\n\nPlease check your connection and try again."


@tool
def get_company_details(company_id: str) -> str:
    """
    Get detailed information about a specific company and job posting.
    
    Use this tool when you need to retrieve full details about a company
    after finding it through search. Provides complete job description and requirements.
    
    Args:
        company_id: The MongoDB ObjectId of the company document (from search results)
        
    Returns:
        Formatted string with complete company and job posting details including
        full job description, requirements, salary, and company information.
    """
    try:
        company_store = _get_company_store()
        company = company_store.get_by_id(company_id)
        
        if not company:
            return f"❌ Company with ID '{company_id}' not found.\n\nPlease verify the ID from search results."
        
        # Format detailed output with emojis for better readability
        output = "=" * 70 + "\n"
        output += f"🏢 {company.get('company_name', 'Unknown Company')}\n"
        output += "=" * 70 + "\n\n"
        
        output += f"💼 Position: {company.get('job_title', 'N/A')}\n"
        output += f"🏭 Company Size: {company.get('company_size', 'N/A')} employees\n"
        output += f"🏢 Industry: {company.get('industry', 'N/A')}\n"
        output += f"📍 Location: {company.get('location', 'N/A')}\n"
        output += f"🏠 Remote Policy: {company.get('remote_policy', 'N/A')}\n"
        output += f"📊 Experience Level: {company.get('experience_level', 'N/A')}\n"
        
        salary = company.get('salary_range')
        if salary:
            output += f"💰 Salary Range: {_format_salary(salary)}\n"
        
        skills = company.get('required_skills', [])
        if skills:
            output += f"🛠️  Required Skills: {', '.join(skills)}\n"
        
        output += "\n" + "-" * 70 + "\n"
        output += "📝 Job Description:\n"
        output += "-" * 70 + "\n"
        output += f"{company.get('job_description', 'No description available.')}\n"
        
        return output
        
    except Exception as e:
        return f"❌ Error retrieving company details: {str(e)}\n\nPlease check the company ID and try again."


@tool
def compare_companies(company_ids: str) -> str:
    """
    Compare multiple companies side-by-side.
    
    Use this tool when a job seeker wants to compare different job opportunities.
    Provide company IDs as a comma-separated string from search results.
    
    Args:
        company_ids: Comma-separated list of company MongoDB ObjectIds (e.g., "id1,id2,id3")
        
    Returns:
        Formatted comparison table showing key differences between opportunities.
    """
    try:
        # Parse company IDs
        ids = [id.strip() for id in company_ids.split(',')]
        
        if len(ids) < 2:
            return "⚠️  Please provide at least 2 company IDs to compare.\n\nExample: compare_companies('id1,id2')"
        
        if len(ids) > 5:
            return "⚠️  Maximum 5 companies can be compared at once.\n\nPlease select your top 5 choices."
        
        # Fetch all companies
        company_store = _get_company_store()
        companies = []
        not_found = []
        
        for company_id in ids:
            company = company_store.get_by_id(company_id)
            if company:
                companies.append(company)
            else:
                not_found.append(company_id)
        
        if not companies:
            return f"❌ No valid companies found with the provided IDs.\n\nIDs tried: {', '.join(ids)}"
        
        # Format comparison with enhanced layout
        output = "=" * 70 + "\n"
        output += f"📊 Comparing {len(companies)} Job Opportunities\n"
        output += "=" * 70 + "\n\n"
        
        if not_found:
            output += f"⚠️  Note: {len(not_found)} ID(s) not found: {', '.join(not_found)}\n\n"
        
        for i, company in enumerate(companies, 1):
            output += f"{'─'*70}\n"
            output += f"Option {i}: 🏢 {company.get('company_name', 'Unknown')}\n"
            output += f"{'─'*70}\n"
            output += f"💼 Job Title: {company.get('job_title', 'N/A')}\n"
            output += f"📍 Location: {company.get('location', 'N/A')} | {company.get('remote_policy', 'N/A')}\n"
            output += f"💰 Salary: {_format_salary(company.get('salary_range'))}\n"
            output += f"📊 Experience: {company.get('experience_level', 'N/A')}\n"
            output += f"🏭 Company Size: {company.get('company_size', 'N/A')} employees\n"
            output += f"🏢 Industry: {company.get('industry', 'N/A')}\n"
            
            skills = company.get('required_skills', [])
            if skills:
                output += f"🛠️  Skills: {', '.join(skills[:5])}"
                if len(skills) > 5:
                    output += f" (+{len(skills)-5} more)"
                output += "\n"
            
            # Add brief description snippet
            desc = company.get('job_description', '')
            if desc:
                output += f"📝 Preview: {_truncate_description(desc, 150)}\n"
            
            output += "\n"
        
        output += "💡 Use get_company_details with an ID to see full descriptions.\n"
        
        return output
        
    except Exception as e:
        return f"❌ Error comparing companies: {str(e)}\n\nPlease verify the IDs and try again."
