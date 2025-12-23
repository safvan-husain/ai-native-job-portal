"""Unit tests for CompanyStore repository."""
import pytest
from unittest.mock import Mock, patch

from src.job_portal.repositories.company_repository import CompanyStore


class TestCompanyStore:
    """Test suite for CompanyStore class."""
    
    def test_init(self):
        """Test initialization."""
        mock_collection = Mock()
        store = CompanyStore(mock_collection, vector_index_name="custom_index")
        
        assert store.collection == mock_collection
        assert store.vector_index_name == "custom_index"
    
    def test_init_default_index_name(self):
        """Test initialization with default index name."""
        mock_collection = Mock()
        store = CompanyStore(mock_collection)
        
        assert store.vector_index_name == "company_vector_index"
    
    def test_store_job_posting_minimal(self):
        """Test storing a job posting with minimal fields."""
        mock_collection = Mock()
        mock_collection.insert_one.return_value = Mock(inserted_id="job123")
        
        store = CompanyStore(mock_collection)
        job_id = store.store_job_posting(
            company_id="comp1",
            company_name="TechCorp",
            job_title="Software Engineer",
            job_description="Build software",
            job_requirements_embedding=[0.1, 0.2, 0.3],
            company_size="51-200",
            location="San Francisco",
            industry="Technology"
        )
        
        assert job_id == "job123"
        call_args = mock_collection.insert_one.call_args[0][0]
        assert call_args["company_id"] == "comp1"
        assert call_args["job_title"] == "Software Engineer"
        assert call_args["status"] == "active"
        assert call_args["remote_policy"] == "onsite"
    
    def test_store_job_posting_full(self):
        """Test storing a job posting with all fields."""
        mock_collection = Mock()
        mock_collection.insert_one.return_value = Mock(inserted_id="job123")
        
        store = CompanyStore(mock_collection)
        job_id = store.store_job_posting(
            company_id="comp1",
            company_name="TechCorp",
            job_title="Senior Engineer",
            job_description="Lead development",
            job_requirements_embedding=[0.1, 0.2],
            company_size="201-500",
            location="New York",
            industry="FinTech",
            salary_range={"min": 120000, "max": 180000},
            remote_policy="hybrid",
            required_skills=["Python", "AWS"],
            experience_level="senior",
            additional_metadata={"benefits": "Great"}
        )
        
        call_args = mock_collection.insert_one.call_args[0][0]
        assert call_args["salary_range"]["min"] == 120000
        assert call_args["remote_policy"] == "hybrid"
        assert call_args["required_skills"] == ["Python", "AWS"]
        assert call_args["experience_level"] == "senior"
        assert call_args["benefits"] == "Great"
    
    @patch.object(CompanyStore, 'vector_search')
    def test_search_matching_candidates_no_filters(self, mock_vector_search):
        """Test searching for matching candidates without filters."""
        mock_collection = Mock()
        mock_vector_search.return_value = [{"job_title": "Engineer", "score": 0.9}]
        
        store = CompanyStore(mock_collection)
        results = store.search_matching_candidates(
            candidate_profile_embedding=[0.1, 0.2, 0.3],
            limit=5
        )
        
        assert len(results) == 1
        mock_vector_search.assert_called_once()
        call_kwargs = mock_vector_search.call_args[1]
        assert call_kwargs["limit"] == 5
        assert call_kwargs["vector_field"] == "requirements_embedding"
        assert call_kwargs["filter_criteria"] is None
    
    @patch.object(CompanyStore, 'vector_search')
    def test_search_matching_candidates_with_filters(self, mock_vector_search):
        """Test searching for matching candidates with filters."""
        mock_collection = Mock()
        mock_vector_search.return_value = []
        
        store = CompanyStore(mock_collection)
        store.search_matching_candidates(
            candidate_profile_embedding=[0.1, 0.2],
            company_size="51-200",
            location="San Francisco",
            industry="Technology",
            remote_policy="remote",
            experience_level="senior",
            limit=10
        )
        
        call_kwargs = mock_vector_search.call_args[1]
        filter_criteria = call_kwargs["filter_criteria"]
        assert filter_criteria["company_size"] == "51-200"
        assert filter_criteria["industry"] == "Technology"
        assert filter_criteria["remote_policy"] == "remote"
        assert filter_criteria["experience_level"] == "senior"
        assert "$regex" in filter_criteria["location"]
    
    def test_get_jobs_by_company(self):
        """Test getting all jobs for a company."""
        mock_collection = Mock()
        mock_collection.find.return_value = [
            {"job_title": "Engineer", "company_id": "comp1"},
            {"job_title": "Designer", "company_id": "comp1"}
        ]
        
        store = CompanyStore(mock_collection)
        jobs = store.get_jobs_by_company("comp1")
        
        assert len(jobs) == 2
        mock_collection.find.assert_called_once_with({"company_id": "comp1"})
    
    @patch.object(CompanyStore, 'update_document')
    def test_update_job_status(self, mock_update):
        """Test updating job status."""
        mock_collection = Mock()
        mock_update.return_value = True
        
        store = CompanyStore(mock_collection)
        success = store.update_job_status("job123", "closed")
        
        assert success is True
        mock_update.assert_called_once_with("job123", {"status": "closed"})
    
    def test_filter_by_metadata_no_filters(self):
        """Test filtering by metadata with no filters."""
        mock_collection = Mock()
        mock_cursor = Mock()
        mock_cursor.limit.return_value = [{"job_title": "Engineer"}]
        mock_collection.find.return_value = mock_cursor
        
        store = CompanyStore(mock_collection)
        results = store.filter_by_metadata(limit=10)
        
        mock_collection.find.assert_called_once_with({"status": "active"})
        mock_cursor.limit.assert_called_once_with(10)
    
    def test_filter_by_metadata_with_all_filters(self):
        """Test filtering by metadata with all filters."""
        mock_collection = Mock()
        mock_cursor = Mock()
        mock_cursor.limit.return_value = []
        mock_collection.find.return_value = mock_cursor
        
        store = CompanyStore(mock_collection)
        store.filter_by_metadata(
            company_size="51-200",
            location="SF",
            industry="Tech",
            remote_policy="remote",
            salary_min=100000,
            limit=20
        )
        
        call_args = mock_collection.find.call_args[0][0]
        assert call_args["company_size"] == "51-200"
        assert call_args["industry"] == "Tech"
        assert call_args["remote_policy"] == "remote"
        assert "$regex" in call_args["location"]
        assert call_args["salary_range.max"]["$gte"] == 100000
