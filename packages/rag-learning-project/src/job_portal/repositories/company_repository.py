"""Company-specific vector store operations."""
from typing import List, Dict, Any, Optional

from .base_vector_store import VectorStore


class CompanyStore(VectorStore):
    """Manages company job postings with vector embeddings and filterable metadata."""
    
    def __init__(self, collection, vector_index_name: str = "company_vector_index"):
        """
        Initialize company store.
        
        Args:
            collection: MongoDB collection for companies
            vector_index_name: Name of the vector search index
        """
        super().__init__(collection, vector_index_name)
    
    def store_job_posting(
        self,
        company_id: str,
        company_name: str,
        job_title: str,
        job_description: str,
        job_requirements_embedding: List[float],
        company_size: str,
        location: str,
        industry: str,
        salary_range: Optional[Dict[str, float]] = None,
        remote_policy: str = "onsite",
        required_skills: Optional[List[str]] = None,
        experience_level: Optional[str] = None,
        additional_metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Store a job posting with vector embedding and filterable metadata.
        
        Args:
            company_id: Unique company identifier
            company_name: Name of the company
            job_title: Job title
            job_description: Full job description text
            job_requirements_embedding: Vector embedding of job requirements
            company_size: Company size (e.g., "1-10", "11-50", "51-200", "201-500", "500+")
            location: Job location (city, state, country)
            industry: Industry sector
            salary_range: Optional salary range {"min": 50000, "max": 80000}
            remote_policy: Remote work policy ("onsite", "hybrid", "remote")
            required_skills: List of required skills
            experience_level: Experience level ("entry", "mid", "senior", "lead")
            additional_metadata: Any additional metadata
            
        Returns:
            Inserted document ID
        """
        document = {
            "company_id": company_id,
            "company_name": company_name,
            "job_title": job_title,
            "job_description": job_description,
            "requirements_embedding": job_requirements_embedding,
            "company_size": company_size,
            "location": location,
            "industry": industry,
            "remote_policy": remote_policy,
            "required_skills": required_skills or [],
            "experience_level": experience_level,
            "salary_range": salary_range,
            "status": "active",
            "created_at": None,  # Set by MongoDB timestamp
            **(additional_metadata or {})
        }
        
        return self.insert_document(document)
    
    def search_matching_candidates(
        self,
        candidate_profile_embedding: List[float],
        company_size: Optional[str] = None,
        location: Optional[str] = None,
        industry: Optional[str] = None,
        remote_policy: Optional[str] = None,
        experience_level: Optional[str] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Search for job postings matching a candidate's profile.
        
        Args:
            candidate_profile_embedding: Vector embedding of candidate's profile
            company_size: Filter by company size
            location: Filter by location
            industry: Filter by industry
            remote_policy: Filter by remote policy
            experience_level: Filter by experience level
            limit: Number of results to return
            
        Returns:
            List of matching job postings with similarity scores
        """
        filter_criteria = {"status": "active"}
        
        if company_size:
            filter_criteria["company_size"] = company_size
        if location:
            filter_criteria["location"] = {"$regex": location, "$options": "i"}
        if industry:
            filter_criteria["industry"] = industry
        if remote_policy:
            filter_criteria["remote_policy"] = remote_policy
        if experience_level:
            filter_criteria["experience_level"] = experience_level
        
        return self.vector_search(
            query_vector=candidate_profile_embedding,
            limit=limit,
            num_candidates=limit * 10,
            filter_criteria=filter_criteria if len(filter_criteria) > 1 else None,
            vector_field="requirements_embedding"
        )
    
    def get_jobs_by_company(self, company_id: str) -> List[Dict[str, Any]]:
        """
        Get all job postings for a specific company.
        
        Args:
            company_id: Company identifier
            
        Returns:
            List of job postings
        """
        return list(self.collection.find({"company_id": company_id}))
    
    def update_job_status(self, job_id: str, status: str) -> bool:
        """
        Update job posting status.
        
        Args:
            job_id: Job posting ID
            status: New status ("active", "closed", "filled")
            
        Returns:
            True if updated successfully
        """
        return self.update_document(job_id, {"status": status})
    
    def filter_by_metadata(
        self,
        company_size: Optional[str] = None,
        location: Optional[str] = None,
        industry: Optional[str] = None,
        remote_policy: Optional[str] = None,
        salary_min: Optional[float] = None,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Filter job postings by metadata only (no vector search).
        
        Args:
            company_size: Filter by company size
            location: Filter by location
            industry: Filter by industry
            remote_policy: Filter by remote policy
            salary_min: Minimum salary requirement
            limit: Maximum number of results
            
        Returns:
            List of matching job postings
        """
        filter_criteria = {"status": "active"}
        
        if company_size:
            filter_criteria["company_size"] = company_size
        if location:
            filter_criteria["location"] = {"$regex": location, "$options": "i"}
        if industry:
            filter_criteria["industry"] = industry
        if remote_policy:
            filter_criteria["remote_policy"] = remote_policy
        if salary_min:
            filter_criteria["salary_range.max"] = {"$gte": salary_min}
        
        return list(self.collection.find(filter_criteria).limit(limit))
