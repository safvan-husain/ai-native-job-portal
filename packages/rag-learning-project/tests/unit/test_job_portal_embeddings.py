"""Unit tests for JobPortalEmbeddings service."""
import pytest
from unittest.mock import Mock, patch

from src.job_portal.services.embeddings.job_portal_embeddings import JobPortalEmbeddings


class TestJobPortalEmbeddings:
    """Test suite for JobPortalEmbeddings class."""
    
    @patch('src.job_portal.services.embeddings.job_portal_embeddings.VoyageEmbeddingService')
    def test_init(self, mock_service_class):
        """Test initialization."""
        embeddings = JobPortalEmbeddings(api_key="test_key")
        mock_service_class.assert_called_once_with(api_key="test_key")
    
    @patch('src.job_portal.services.embeddings.job_portal_embeddings.VoyageEmbeddingService')
    def test_embed_job_posting_basic(self, mock_service_class):
        """Test embedding a basic job posting."""
        mock_service = Mock()
        mock_service.embed_document.return_value = [0.1, 0.2, 0.3]
        mock_service_class.return_value = mock_service
        
        embeddings = JobPortalEmbeddings(api_key="test_key")
        result = embeddings.embed_job_posting(
            job_title="Software Engineer",
            job_description="Build great software",
            required_skills=["Python", "Django"]
        )
        
        assert result == [0.1, 0.2, 0.3]
        mock_service.embed_document.assert_called_once()
        call_args = mock_service.embed_document.call_args
        assert "Software Engineer" in call_args[0][0]
        assert "Build great software" in call_args[0][0]
        assert "Python" in call_args[0][0]
    
    @patch('src.job_portal.services.embeddings.job_portal_embeddings.VoyageEmbeddingService')
    def test_embed_job_posting_with_all_fields(self, mock_service_class):
        """Test embedding a job posting with all optional fields."""
        mock_service = Mock()
        mock_service.embed_document.return_value = [0.1, 0.2, 0.3]
        mock_service_class.return_value = mock_service
        
        embeddings = JobPortalEmbeddings(api_key="test_key")
        result = embeddings.embed_job_posting(
            job_title="Senior Engineer",
            job_description="Lead development",
            required_skills=["Python", "AWS"],
            experience_level="senior",
            additional_context="Must have startup experience"
        )
        
        call_args = mock_service.embed_document.call_args[0][0]
        assert "Senior Engineer" in call_args
        assert "senior" in call_args
        assert "startup experience" in call_args
    
    @patch('src.job_portal.services.embeddings.job_portal_embeddings.VoyageEmbeddingService')
    def test_embed_job_posting_chunked_response(self, mock_service_class):
        """Test handling chunked embedding response."""
        mock_service = Mock()
        mock_service.embed_document.return_value = {
            "embeddings": [[0.1, 0.2], [0.3, 0.4]],
            "chunks": ["chunk1", "chunk2"],
            "num_chunks": 2
        }
        mock_service_class.return_value = mock_service
        
        embeddings = JobPortalEmbeddings(api_key="test_key")
        result = embeddings.embed_job_posting(
            job_title="Engineer",
            job_description="Long description",
            required_skills=["Python"]
        )
        
        # Should return first chunk's embedding
        assert result == [0.1, 0.2]
    
    @patch('src.job_portal.services.embeddings.job_portal_embeddings.VoyageEmbeddingService')
    def test_embed_candidate_profile_basic(self, mock_service_class):
        """Test embedding a basic candidate profile."""
        mock_service = Mock()
        mock_service.embed_document.return_value = [0.5, 0.6, 0.7]
        mock_service_class.return_value = mock_service
        
        embeddings = JobPortalEmbeddings(api_key="test_key")
        result = embeddings.embed_candidate_profile(
            name="John Doe",
            current_title="Software Engineer",
            profile_summary="Experienced developer",
            skills=["Python", "JavaScript"],
            years_of_experience=5.0
        )
        
        assert result == [0.5, 0.6, 0.7]
        call_args = mock_service.embed_document.call_args[0][0]
        assert "John Doe" in call_args
        assert "Software Engineer" in call_args
        assert "5" in call_args
        assert "Python" in call_args
    
    @patch('src.job_portal.services.embeddings.job_portal_embeddings.VoyageEmbeddingService')
    def test_embed_candidate_profile_with_all_fields(self, mock_service_class):
        """Test embedding a candidate profile with all fields."""
        mock_service = Mock()
        mock_service.embed_document.return_value = [0.5, 0.6, 0.7]
        mock_service_class.return_value = mock_service
        
        embeddings = JobPortalEmbeddings(api_key="test_key")
        result = embeddings.embed_candidate_profile(
            name="Jane Smith",
            current_title="Senior Engineer",
            profile_summary="Expert developer",
            skills=["Python", "Go"],
            years_of_experience=8.0,
            education="Masters in CS",
            work_history="Worked at Google, Amazon"
        )
        
        call_args = mock_service.embed_document.call_args[0][0]
        assert "Masters in CS" in call_args
        assert "Google" in call_args
    
    @patch('src.job_portal.services.embeddings.job_portal_embeddings.VoyageEmbeddingService')
    def test_embed_search_query(self, mock_service_class):
        """Test embedding a search query."""
        mock_service = Mock()
        mock_service.embed_query.return_value = [0.8, 0.9, 1.0]
        mock_service_class.return_value = mock_service
        
        embeddings = JobPortalEmbeddings(api_key="test_key")
        result = embeddings.embed_search_query("Python developer jobs")
        
        assert result == [0.8, 0.9, 1.0]
        mock_service.embed_query.assert_called_once_with("Python developer jobs")
    
    @patch('src.job_portal.services.embeddings.job_portal_embeddings.VoyageEmbeddingService')
    def test_embed_job_search_query_full(self, mock_service_class):
        """Test embedding a job search query with all parameters."""
        mock_service = Mock()
        mock_service.embed_query.return_value = [0.1, 0.2]
        mock_service_class.return_value = mock_service
        
        embeddings = JobPortalEmbeddings(api_key="test_key")
        result = embeddings.embed_job_search_query(
            desired_role="ML Engineer",
            desired_skills=["Python", "TensorFlow"],
            experience_level="senior",
            additional_preferences="Remote work preferred"
        )
        
        assert result == [0.1, 0.2]
        call_args = mock_service.embed_query.call_args[0][0]
        assert "ML Engineer" in call_args
        assert "Python" in call_args
        assert "senior" in call_args
        assert "Remote" in call_args
    
    @patch('src.job_portal.services.embeddings.job_portal_embeddings.VoyageEmbeddingService')
    def test_embed_job_search_query_minimal(self, mock_service_class):
        """Test embedding a minimal job search query."""
        mock_service = Mock()
        mock_service.embed_query.return_value = [0.1, 0.2]
        mock_service_class.return_value = mock_service
        
        embeddings = JobPortalEmbeddings(api_key="test_key")
        result = embeddings.embed_job_search_query(desired_role="Developer")
        
        assert result == [0.1, 0.2]
        call_args = mock_service.embed_query.call_args[0][0]
        assert "Developer" in call_args
    
    @patch('src.job_portal.services.embeddings.job_portal_embeddings.VoyageEmbeddingService')
    def test_embed_candidate_search_query_full(self, mock_service_class):
        """Test embedding a candidate search query with all parameters."""
        mock_service = Mock()
        mock_service.embed_query.return_value = [0.3, 0.4]
        mock_service_class.return_value = mock_service
        
        embeddings = JobPortalEmbeddings(api_key="test_key")
        result = embeddings.embed_candidate_search_query(
            job_title="Backend Engineer",
            required_skills=["Go", "Kubernetes"],
            experience_level="mid",
            additional_requirements="Must have distributed systems experience"
        )
        
        assert result == [0.3, 0.4]
        call_args = mock_service.embed_query.call_args[0][0]
        assert "Backend Engineer" in call_args
        assert "Go" in call_args
        assert "mid" in call_args
        assert "distributed systems" in call_args
    
    @patch('src.job_portal.services.embeddings.job_portal_embeddings.VoyageEmbeddingService')
    def test_embed_candidate_search_query_minimal(self, mock_service_class):
        """Test embedding a minimal candidate search query."""
        mock_service = Mock()
        mock_service.embed_query.return_value = [0.3, 0.4]
        mock_service_class.return_value = mock_service
        
        embeddings = JobPortalEmbeddings(api_key="test_key")
        result = embeddings.embed_candidate_search_query(job_title="Engineer")
        
        assert result == [0.3, 0.4]
        call_args = mock_service.embed_query.call_args[0][0]
        assert "Engineer" in call_args
