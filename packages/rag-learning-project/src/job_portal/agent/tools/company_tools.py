"""LangChain tools for companies."""
import time
from langchain_core.tools import tool

try:
    from ...infrastructure.mongodb.connection import MongoDBConnection
    from ...repositories.jobseeker_repository import JobSeekerStore
    from ...services.embeddings.job_portal_embeddings import JobPortalEmbeddings
except ImportError:
    from job_portal.infrastructure.mongodb.connection import MongoDBConnection
    from job_portal.repositories.jobseeker_repository import JobSeekerStore
    from job_portal.services.embeddings.job_portal_embeddings import JobPortalEmbeddings


# Initialize services (lazy loading)
_db_connection = None
_jobseeker_store = None
_embeddings = None
_last_api_call = 0  # Track last API call for rate limiting


def _get_jobseeker_store() -> JobSeekerStore:
    """Get or create job seeker store instance."""
    global _db_connection, _jobseeker_store
    if _jobseeker_store is None:
        _db_connection = MongoDBConnection()
        collection = _db_connection.get_collection("job_seekers")
        _jobseeker_store = JobSeekerStore(collection)
    return _jobseeker_store


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


def _format_salary(salary_min):
    """Format minimum salary for display."""
    if not salary_min:
        return "Not specified"
    return f"${salary_min:,.0f}+"


def _truncate_summary(text, max_length=200):
    """Truncate profile summary to max length."""
    if len(text) <= max_length:
        return text
    return text[:max_length].rsplit(' ', 1)[0] + "..."


@tool
def search_candidates(job_requirements: str, limit: int = 5) -> str:
    """
    Search for candidates that match the given job requirements.
    
    Use this tool when a company wants to find matching candidates for a job opening.
    The tool performs vector similarity search to find the best matches.
    
    Args:
        job_requirements: Job requirements as natural language text (e.g., "Senior Python developer with ML experience")
        limit: Maximum number of results to return (default: 5, max: 10)
        
    Returns:
        Formatted string with matching candidates including name, title, experience,
        salary expectations, and similarity score.
    """
    try:
        # Validate limit
        limit = min(max(1, limit), 10)
        
        # Handle rate limiting for Voyage AI
        _handle_rate_limit()
        
        # Generate embedding for requirements
        embeddings = _get_embeddings()
        requirements_embedding = embeddings.embed_search_query(job_requirements)
        
        # Search for matching candidates
        jobseeker_store = _get_jobseeker_store()
        results = jobseeker_store.vector_search(
            query_vector=requirements_embedding,
            limit=limit,
            num_candidates=limit * 10,
            vector_field="profile_embedding"
        )
        
        if not results:
            return "No matching candidates found. Try different requirements or broader search terms."
        
        # Format results with enhanced information
        output = f"🔍 Found {len(results)} matching candidate(s):\n\n"
        for i, candidate in enumerate(results, 1):
            score = candidate.get('score', 0)
            match_pct = score * 100
            
            output += f"{i}. 👤 {candidate.get('name', 'Unknown')}\n"
            output += f"   💼 Title: {candidate.get('current_title', 'N/A')}\n"
            output += f"   📊 Experience: {candidate.get('years_of_experience', 0)} years\n"
            output += f"   📍 Location: {candidate.get('desired_location', 'N/A')} | {candidate.get('desired_remote_policy', 'N/A')}\n"
            output += f"   💰 Desired Salary: {_format_salary(candidate.get('desired_salary_min'))}\n"
            output += f"   🎓 Education: {candidate.get('education_level', 'N/A')}\n"
            output += f"   🎯 Match: {match_pct:.1f}%\n"
            
            skills = candidate.get('skills', [])
            if skills:
                output += f"   🛠️  Skills: {', '.join(skills[:5])}\n"
            
            output += f"   🆔 ID: {candidate.get('_id')}\n\n"
        
        output += "💡 Use get_candidate_details with an ID to see full profile.\n"
        output += "💡 Use compare_candidates with multiple IDs to compare candidates.\n"
        
        return output
        
    except Exception as e:
        return f"❌ Error searching for candidates: {str(e)}\n\nPlease check your connection and try again."


@tool
def get_candidate_details(candidate_id: str) -> str:
    """
    Get detailed information about a specific candidate.
    
    Use this tool when you need to retrieve full details about a candidate
    after finding them through search. Provides complete profile and experience.
    
    Args:
        candidate_id: The MongoDB ObjectId of the candidate document (from search results)
        
    Returns:
        Formatted string with complete candidate profile details including
        full summary, skills, experience, and preferences.
    """
    try:
        jobseeker_store = _get_jobseeker_store()
        candidate = jobseeker_store.get_by_id(candidate_id)
        
        if not candidate:
            return f"❌ Candidate with ID '{candidate_id}' not found.\n\nPlease verify the ID from search results."
        
        # Format detailed output with emojis for better readability
        output = "=" * 70 + "\n"
        output += f"👤 {candidate.get('name', 'Unknown')}\n"
        output += "=" * 70 + "\n\n"
        
        output += f"💼 Current Title: {candidate.get('current_title', 'N/A')}\n"
        output += f"📊 Experience: {candidate.get('years_of_experience', 0)} years\n"
        output += f"🎓 Education: {candidate.get('education_level', 'N/A')}\n"
        output += f"📍 Desired Location: {candidate.get('desired_location', 'N/A')}\n"
        output += f"🏠 Remote Preference: {candidate.get('desired_remote_policy', 'N/A')}\n"
        output += f"⏰ Availability: {candidate.get('availability', 'N/A')}\n"
        
        salary = candidate.get('desired_salary_min')
        if salary:
            output += f"💰 Desired Salary: {_format_salary(salary)}\n"
        
        skills = candidate.get('skills', [])
        if skills:
            output += f"🛠️  Skills: {', '.join(skills)}\n"
        
        industries = candidate.get('industries_of_interest', [])
        if industries:
            output += f"🏢 Industries of Interest: {', '.join(industries)}\n"
        
        output += "\n" + "-" * 70 + "\n"
        output += "📝 Profile Summary:\n"
        output += "-" * 70 + "\n"
        output += f"{candidate.get('profile_summary', 'No summary available.')}\n"
        
        return output
        
    except Exception as e:
        return f"❌ Error retrieving candidate details: {str(e)}\n\nPlease check the candidate ID and try again."


@tool
def compare_candidates(candidate_ids: str) -> str:
    """
    Compare multiple candidates side-by-side.
    
    Use this tool when a company wants to compare different candidates for a position.
    Provide candidate IDs as a comma-separated string from search results.
    
    Args:
        candidate_ids: Comma-separated list of candidate MongoDB ObjectIds (e.g., "id1,id2,id3")
        
    Returns:
        Formatted comparison table showing key differences between candidates.
    """
    try:
        # Parse candidate IDs
        ids = [id.strip() for id in candidate_ids.split(',')]
        
        if len(ids) < 2:
            return "⚠️  Please provide at least 2 candidate IDs to compare.\n\nExample: compare_candidates('id1,id2')"
        
        if len(ids) > 5:
            return "⚠️  Maximum 5 candidates can be compared at once.\n\nPlease select your top 5 choices."
        
        # Fetch all candidates
        jobseeker_store = _get_jobseeker_store()
        candidates = []
        not_found = []
        
        for candidate_id in ids:
            candidate = jobseeker_store.get_by_id(candidate_id)
            if candidate:
                candidates.append(candidate)
            else:
                not_found.append(candidate_id)
        
        if not candidates:
            return f"❌ No valid candidates found with the provided IDs.\n\nIDs tried: {', '.join(ids)}"
        
        # Format comparison with enhanced layout
        output = "=" * 70 + "\n"
        output += f"📊 Comparing {len(candidates)} Candidates\n"
        output += "=" * 70 + "\n\n"
        
        if not_found:
            output += f"⚠️  Note: {len(not_found)} ID(s) not found: {', '.join(not_found)}\n\n"
        
        for i, candidate in enumerate(candidates, 1):
            output += f"{'─'*70}\n"
            output += f"Candidate {i}: 👤 {candidate.get('name', 'Unknown')}\n"
            output += f"{'─'*70}\n"
            output += f"💼 Title: {candidate.get('current_title', 'N/A')}\n"
            output += f"📊 Experience: {candidate.get('years_of_experience', 0)} years\n"
            output += f"🎓 Education: {candidate.get('education_level', 'N/A')}\n"
            output += f"📍 Location: {candidate.get('desired_location', 'N/A')} | {candidate.get('desired_remote_policy', 'N/A')}\n"
            output += f"💰 Desired Salary: {_format_salary(candidate.get('desired_salary_min'))}\n"
            output += f"⏰ Availability: {candidate.get('availability', 'N/A')}\n"
            
            skills = candidate.get('skills', [])
            if skills:
                output += f"🛠️  Skills: {', '.join(skills[:5])}"
                if len(skills) > 5:
                    output += f" (+{len(skills)-5} more)"
                output += "\n"
            
            # Add brief profile snippet
            summary = candidate.get('profile_summary', '')
            if summary:
                output += f"📝 Preview: {_truncate_summary(summary, 150)}\n"
            
            output += "\n"
        
        output += "💡 Use get_candidate_details with an ID to see full profiles.\n"
        
        return output
        
    except Exception as e:
        return f"❌ Error comparing candidates: {str(e)}\n\nPlease verify the IDs and try again."
