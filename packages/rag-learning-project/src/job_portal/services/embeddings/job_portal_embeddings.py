"""High-level embedding functions for job portal use cases."""
from typing import Dict, List, Any

try:
    from ...infrastructure.voyage.embedding_service import VoyageEmbeddingService
except ImportError:
    from job_portal.infrastructure.voyage.embedding_service import VoyageEmbeddingService


class JobPortalEmbeddings:
    """
    High-level interface for generating embeddings for job portal entities.
    Handles job postings, candidate profiles, and search queries.
    """
    
    def __init__(self, api_key: str = None):
        """
        Initialize job portal embeddings.
        
        Args:
            api_key: Voyage AI API key (optional, uses env var if not provided)
        """
        self.embedding_service = VoyageEmbeddingService(api_key=api_key)
    
    def embed_job_posting(
        self,
        job_title: str,
        job_description: str,
        required_skills: List[str],
        experience_level: str = None,
        additional_context: str = None
    ) -> List[float]:
        """
        Generate embedding for a job posting.
        
        Args:
            job_title: Job title
            job_description: Full job description
            required_skills: List of required skills
            experience_level: Experience level (entry, mid, senior, lead)
            additional_context: Any additional context
            
        Returns:
            Embedding vector for the job requirements
        """
        # Construct comprehensive job requirements text
        requirements_text = f"Job Title: {job_title}\n\n"
        
        if experience_level:
            requirements_text += f"Experience Level: {experience_level}\n\n"
        
        requirements_text += f"Description:\n{job_description}\n\n"
        
        if required_skills:
            requirements_text += f"Required Skills: {', '.join(required_skills)}\n\n"
        
        if additional_context:
            requirements_text += f"Additional Requirements:\n{additional_context}"
        
        # Generate embedding (auto-chunk if needed)
        embedding_result = self.embedding_service.embed_document(
            requirements_text,
            auto_chunk=True
        )
        
        # If chunked, return the first chunk's embedding (most important context)
        # or average all chunks
        if isinstance(embedding_result, dict):
            # For job postings, use first chunk (usually contains title + key info)
            return embedding_result["embeddings"][0]
        else:
            return embedding_result
    
    def embed_candidate_profile(
        self,
        name: str,
        current_title: str,
        profile_summary: str,
        skills: List[str],
        years_of_experience: float,
        education: str = None,
        work_history: str = None
    ) -> List[float]:
        """
        Generate embedding for a candidate profile.
        
        Args:
            name: Candidate name
            current_title: Current or most recent job title
            profile_summary: Professional summary
            skills: List of skills
            years_of_experience: Years of experience
            education: Education background
            work_history: Work history details
            
        Returns:
            Embedding vector for the candidate profile
        """
        # Construct comprehensive profile text
        profile_text = f"Candidate: {name}\n"
        profile_text += f"Current Title: {current_title}\n"
        profile_text += f"Experience: {years_of_experience} years\n\n"
        
        if education:
            profile_text += f"Education: {education}\n\n"
        
        profile_text += f"Professional Summary:\n{profile_summary}\n\n"
        profile_text += f"Skills: {', '.join(skills)}\n\n"
        
        if work_history:
            profile_text += f"Work History:\n{work_history}"
        
        # Generate embedding (auto-chunk if needed)
        embedding_result = self.embedding_service.embed_document(
            profile_text,
            auto_chunk=True
        )
        
        # If chunked, return the first chunk's embedding
        if isinstance(embedding_result, dict):
            return embedding_result["embeddings"][0]
        else:
            return embedding_result
    
    def embed_search_query(self, query: str) -> List[float]:
        """
        Generate embedding for a search query.
        
        Args:
            query: Search query text
            
        Returns:
            Query embedding vector
        """
        return self.embedding_service.embed_query(query)
    
    def embed_job_search_query(
        self,
        desired_role: str = None,
        desired_skills: List[str] = None,
        experience_level: str = None,
        additional_preferences: str = None
    ) -> List[float]:
        """
        Generate embedding for a job search query from candidate preferences.
        
        Args:
            desired_role: Desired job title/role
            desired_skills: Skills the candidate wants to use
            experience_level: Candidate's experience level
            additional_preferences: Additional preferences
            
        Returns:
            Query embedding vector
        """
        query_text = ""
        
        if desired_role:
            query_text += f"Looking for: {desired_role}\n"
        
        if experience_level:
            query_text += f"Experience level: {experience_level}\n"
        
        if desired_skills:
            query_text += f"Skills: {', '.join(desired_skills)}\n"
        
        if additional_preferences:
            query_text += f"\n{additional_preferences}"
        
        return self.embed_search_query(query_text.strip())
    
    def embed_candidate_search_query(
        self,
        job_title: str,
        required_skills: List[str] = None,
        experience_level: str = None,
        additional_requirements: str = None
    ) -> List[float]:
        """
        Generate embedding for a candidate search query from job requirements.
        
        Args:
            job_title: Job title to search for
            required_skills: Required skills
            experience_level: Required experience level
            additional_requirements: Additional requirements
            
        Returns:
            Query embedding vector
        """
        query_text = f"Searching for candidates for: {job_title}\n"
        
        if experience_level:
            query_text += f"Experience level: {experience_level}\n"
        
        if required_skills:
            query_text += f"Required skills: {', '.join(required_skills)}\n"
        
        if additional_requirements:
            query_text += f"\n{additional_requirements}"
        
        return self.embed_search_query(query_text.strip())
