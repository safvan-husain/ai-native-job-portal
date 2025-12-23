"""Unit tests for JobSeekerStore repository."""
import pytest
from unittest.mock import Mock, patch

from src.job_portal.repositories.jobseeker_repository import JobSeekerStore


class TestJobSeekerStore:
    """Test suite for JobSeekerStore class."""
    
    def test_init(self):
        """Test initialization."""
        mock_collection = Mock()
        store = JobSeekerStore(mock_collection, vector_index_name="custom_index")
        
        assert store.collection == mock_collection
        assert store.vector_index_name == "custom_index"
    
    def test_init_default_index_name(self):
        """Test initialization with default index name."""
        mock_collection = Mock()
        store = JobSeekerStore(mock_collection)
        
        assert store.vector_index_name == "jobseeker_vector_index"
    
    def test_store_profile_minimal(self):
        """Test storing a profile with minimal fields."""
        mock_collection = Mock()
        mock_collection.insert_one.return_value = Mock(inserted_id="profile123")
        
        store = JobSeekerStore(mock_collection)
        profile_id = store.store_profile(
            user_id="user1",
            name="John Doe",
            profile_summary="Experienced developer",
            profile_embedding=[0.1, 0.2, 0.3],
            years_of_experience=5.0,
            skills=["Python", "JavaScript"],
            desired_location="San Francisco"
        )
        
        assert profile_id == "profile123"
        call_args = mock_collection.insert_one.call_args[0][0]
        assert call_args["user_id"] == "user1"
        assert call_args["name"] == "John Doe"
        assert call_args["years_of_experience"] == 5.0
        assert call_args["status"] == "active"
        assert call_args["desired_remote_policy"] == "any"
        assert call_args["availability"] == "immediately"
    
    def test_store_profile_full(self):
        """Test storing a profile with all fields."""
        mock_collection = Mock()
        mock_collection.insert_one.return_value = Mock(inserted_id="profile123")
        
        store = JobSeekerStore(mock_collection)
        profile_id = store.store_profile(
            user_id="user1",
            name="Jane Smith",
            profile_summary="Senior engineer",
            profile_embedding=[0.1, 0.2],
            years_of_experience=8.0,
            skills=["Python", "Go"],
            desired_location="Remote",
            desired_remote_policy="remote",
            desired_salary_min=150000,
            education_level="masters",
            current_title="Senior Engineer",
            industries_of_interest=["FinTech", "AI"],
            availability="2_weeks",
            additional_metadata={"portfolio": "github.com/jane"}
        )
        
        call_args = mock_collection.insert_one.call_args[0][0]
        assert call_args["desired_remote_policy"] == "remote"
        assert call_args["desired_salary_min"] == 150000
        assert call_args["education_level"] == "masters"
        assert call_args["current_title"] == "Senior Engineer"
        assert call_args["industries_of_interest"] == ["FinTech", "AI"]
        assert call_args["availability"] == "2_weeks"
        assert call_args["portfolio"] == "github.com/jane"
    
    @patch.object(JobSeekerStore, 'vector_search')
    def test_search_matching_jobs_no_filters(self, mock_vector_search):
        """Test searching for matching jobs without filters."""
        mock_collection = Mock()
        mock_vector_search.return_value = [{"name": "John", "score": 0.9}]
        
        store = JobSeekerStore(mock_collection)
        results = store.search_matching_jobs(
            job_requirements_embedding=[0.1, 0.2, 0.3],
            limit=5
        )
        
        assert len(results) == 1
        mock_vector_search.assert_called_once()
        call_kwargs = mock_vector_search.call_args[1]
        assert call_kwargs["limit"] == 5
        assert call_kwargs["vector_field"] == "profile_embedding"
        assert call_kwargs["filter_criteria"] is None
    
    @patch.object(JobSeekerStore, 'vector_search')
    def test_search_matching_jobs_with_experience_range(self, mock_vector_search):
        """Test searching with experience range filters."""
        mock_collection = Mock()
        mock_vector_search.return_value = []
        
        store = JobSeekerStore(mock_collection)
        store.search_matching_jobs(
            job_requirements_embedding=[0.1, 0.2],
            min_experience=3.0,
            max_experience=7.0,
            limit=10
        )
        
        call_kwargs = mock_vector_search.call_args[1]
        filter_criteria = call_kwargs["filter_criteria"]
        assert filter_criteria["years_of_experience"]["$gte"] == 3.0
        assert filter_criteria["years_of_experience"]["$lte"] == 7.0
    
    @patch.object(JobSeekerStore, 'vector_search')
    def test_search_matching_jobs_with_all_filters(self, mock_vector_search):
        """Test searching with all filters."""
        mock_collection = Mock()
        mock_vector_search.return_value = []
        
        store = JobSeekerStore(mock_collection)
        store.search_matching_jobs(
            job_requirements_embedding=[0.1, 0.2],
            min_experience=5.0,
            required_skills=["Python", "AWS"],
            location="San Francisco",
            remote_policy="hybrid",
            industry="Technology",
            limit=10
        )
        
        call_kwargs = mock_vector_search.call_args[1]
        filter_criteria = call_kwargs["filter_criteria"]
        assert filter_criteria["years_of_experience"]["$gte"] == 5.0
        assert filter_criteria["skills"]["$in"] == ["Python", "AWS"]
        assert "$regex" in filter_criteria["desired_location"]
        assert filter_criteria["industries_of_interest"] == "Technology"
        assert "$or" in filter_criteria  # Remote policy check
    
    @patch.object(JobSeekerStore, 'vector_search')
    def test_search_matching_jobs_remote_policy_any(self, mock_vector_search):
        """Test searching with 'any' remote policy doesn't add filter."""
        mock_collection = Mock()
        mock_vector_search.return_value = []
        
        store = JobSeekerStore(mock_collection)
        store.search_matching_jobs(
            job_requirements_embedding=[0.1, 0.2],
            remote_policy="any",
            limit=10
        )
        
        call_kwargs = mock_vector_search.call_args[1]
        filter_criteria = call_kwargs["filter_criteria"]
        # When only status filter exists, filter_criteria should be None
        assert filter_criteria is None or "$or" not in filter_criteria
    
    def test_get_profile_by_user_found(self):
        """Test getting profile by user ID when found."""
        mock_collection = Mock()
        mock_collection.find_one.return_value = {"user_id": "user1", "name": "John"}
        
        store = JobSeekerStore(mock_collection)
        profile = store.get_profile_by_user("user1")
        
        assert profile["name"] == "John"
        mock_collection.find_one.assert_called_once_with({"user_id": "user1"})
    
    def test_get_profile_by_user_not_found(self):
        """Test getting profile by user ID when not found."""
        mock_collection = Mock()
        mock_collection.find_one.return_value = None
        
        store = JobSeekerStore(mock_collection)
        profile = store.get_profile_by_user("user999")
        
        assert profile is None
    
    @patch.object(JobSeekerStore, 'update_document')
    def test_update_profile_status(self, mock_update):
        """Test updating profile status."""
        mock_collection = Mock()
        mock_update.return_value = True
        
        store = JobSeekerStore(mock_collection)
        success = store.update_profile_status("profile123", "hired")
        
        assert success is True
        mock_update.assert_called_once_with("profile123", {"status": "hired"})
    
    def test_filter_by_metadata_no_filters(self):
        """Test filtering by metadata with no filters."""
        mock_collection = Mock()
        mock_cursor = Mock()
        mock_cursor.limit.return_value = [{"name": "John"}]
        mock_collection.find.return_value = mock_cursor
        
        store = JobSeekerStore(mock_collection)
        results = store.filter_by_metadata(limit=10)
        
        mock_collection.find.assert_called_once_with({"status": "active"})
        mock_cursor.limit.assert_called_once_with(10)
    
    def test_filter_by_metadata_with_all_filters(self):
        """Test filtering by metadata with all filters."""
        mock_collection = Mock()
        mock_cursor = Mock()
        mock_cursor.limit.return_value = []
        mock_collection.find.return_value = mock_cursor
        
        store = JobSeekerStore(mock_collection)
        store.filter_by_metadata(
            min_experience=3.0,
            max_experience=8.0,
            skills=["Python", "Go"],
            location="SF",
            education_level="bachelors",
            availability="immediately",
            limit=20
        )
        
        call_args = mock_collection.find.call_args[0][0]
        assert call_args["years_of_experience"]["$gte"] == 3.0
        assert call_args["years_of_experience"]["$lte"] == 8.0
        assert call_args["skills"]["$in"] == ["Python", "Go"]
        assert "$regex" in call_args["desired_location"]
        assert call_args["education_level"] == "bachelors"
        assert call_args["availability"] == "immediately"
