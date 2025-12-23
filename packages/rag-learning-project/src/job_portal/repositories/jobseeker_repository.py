"""Job seeker-specific vector store operations."""
from typing import List, Dict, Any, Optional

from .base_vector_store import VectorStore


class JobSeekerStore(VectorStore):
    """Manages job seeker profiles with vector embeddings and filterable metadata."""
    
    def __init__(self, collection, vector_index_name: str = "jobseeker_vector_index"):
        """
        Initialize job seeker store.
        
        Args:
            collection: MongoDB collection for job seekers
            vector_index_name: Name of the vector search index
        """
        super().__init__(collection, vector_index_name)
    
    def store_profile(
        self,
        user_id: str,
        name: str,
        profile_summary: str,
        profile_embedding: List[float],
        years_of_experience: float,
        skills: List[str],
        desired_location: str,
        desired_remote_policy: str = "any",
        desired_salary_min: Optional[float] = None,
        education_level: Optional[str] = None,
        current_title: Optional[str] = None,
        industries_of_interest: Optional[List[str]] = None,
        availability: str = "immediately",
        additional_metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Store a job seeker profile with vector embedding and filterable metadata.
        
        Args:
            user_id: Unique user identifier
            name: Job seeker's name
            profile_summary: Summary of experience and qualifications
            profile_embedding: Vector embedding of profile
            years_of_experience: Total years of professional experience
            skills: List of skills
            desired_location: Desired work location
            desired_remote_policy: Remote work preference ("onsite", "hybrid", "remote", "any")
            desired_salary_min: Minimum desired salary
            education_level: Education level ("high_school", "bachelors", "masters", "phd")
            current_title: Current or most recent job title
            industries_of_interest: List of industries of interest
            availability: Availability status ("immediately", "2_weeks", "1_month", "3_months")
            additional_metadata: Any additional metadata
            
        Returns:
            Inserted document ID
        """
        document = {
            "user_id": user_id,
            "name": name,
            "profile_summary": profile_summary,
            "profile_embedding": profile_embedding,
            "years_of_experience": years_of_experience,
            "skills": skills,
            "desired_location": desired_location,
            "desired_remote_policy": desired_remote_policy,
            "desired_salary_min": desired_salary_min,
            "education_level": education_level,
            "current_title": current_title,
            "industries_of_interest": industries_of_interest or [],
            "availability": availability,
            "status": "active",
            "created_at": None,  # Set by MongoDB timestamp
            **(additional_metadata or {})
        }
        
        return self.insert_document(document)
    
    def search_matching_jobs(
        self,
        job_requirements_embedding: List[float],
        min_experience: Optional[float] = None,
        max_experience: Optional[float] = None,
        required_skills: Optional[List[str]] = None,
        location: Optional[str] = None,
        remote_policy: Optional[str] = None,
        industry: Optional[str] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Search for candidates matching job requirements.
        
        Args:
            job_requirements_embedding: Vector embedding of job requirements
            min_experience: Minimum years of experience
            max_experience: Maximum years of experience
            required_skills: List of required skills
            location: Filter by desired location
            remote_policy: Filter by remote policy preference
            industry: Filter by industry of interest
            limit: Number of results to return
            
        Returns:
            List of matching candidate profiles with similarity scores
        """
        filter_criteria = {"status": "active"}
        
        if min_experience is not None:
            filter_criteria["years_of_experience"] = {"$gte": min_experience}
        if max_experience is not None:
            if "years_of_experience" in filter_criteria:
                filter_criteria["years_of_experience"]["$lte"] = max_experience
            else:
                filter_criteria["years_of_experience"] = {"$lte": max_experience}
        
        if required_skills:
            filter_criteria["skills"] = {"$in": required_skills}
        
        if location:
            filter_criteria["desired_location"] = {"$regex": location, "$options": "i"}
        
        if remote_policy and remote_policy != "any":
            filter_criteria["$or"] = [
                {"desired_remote_policy": remote_policy},
                {"desired_remote_policy": "any"}
            ]
        
        if industry:
            filter_criteria["industries_of_interest"] = industry
        
        return self.vector_search(
            query_vector=job_requirements_embedding,
            limit=limit,
            num_candidates=limit * 10,
            filter_criteria=filter_criteria if len(filter_criteria) > 1 else None,
            vector_field="profile_embedding"
        )
    
    def get_profile_by_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Get job seeker profile by user ID.
        
        Args:
            user_id: User identifier
            
        Returns:
            Profile document if found
        """
        return self.collection.find_one({"user_id": user_id})
    
    def update_profile_status(self, profile_id: str, status: str) -> bool:
        """
        Update profile status.
        
        Args:
            profile_id: Profile ID
            status: New status ("active", "inactive", "hired")
            
        Returns:
            True if updated successfully
        """
        return self.update_document(profile_id, {"status": status})
    
    def filter_by_metadata(
        self,
        min_experience: Optional[float] = None,
        max_experience: Optional[float] = None,
        skills: Optional[List[str]] = None,
        location: Optional[str] = None,
        education_level: Optional[str] = None,
        availability: Optional[str] = None,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Filter candidates by metadata only (no vector search).
        
        Args:
            min_experience: Minimum years of experience
            max_experience: Maximum years of experience
            skills: Required skills (any match)
            location: Filter by desired location
            education_level: Filter by education level
            availability: Filter by availability
            limit: Maximum number of results
            
        Returns:
            List of matching profiles
        """
        filter_criteria = {"status": "active"}
        
        if min_experience is not None:
            filter_criteria["years_of_experience"] = {"$gte": min_experience}
        if max_experience is not None:
            if "years_of_experience" in filter_criteria:
                filter_criteria["years_of_experience"]["$lte"] = max_experience
            else:
                filter_criteria["years_of_experience"] = {"$lte": max_experience}
        
        if skills:
            filter_criteria["skills"] = {"$in": skills}
        
        if location:
            filter_criteria["desired_location"] = {"$regex": location, "$options": "i"}
        
        if education_level:
            filter_criteria["education_level"] = education_level
        
        if availability:
            filter_criteria["availability"] = availability
        
        return list(self.collection.find(filter_criteria).limit(limit))
