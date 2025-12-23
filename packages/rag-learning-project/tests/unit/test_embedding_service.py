"""Unit tests for Voyage AI embedding service."""
import os
import pytest
from unittest.mock import Mock, patch, MagicMock

from src.job_portal.infrastructure.voyage.embedding_service import VoyageEmbeddingService


class TestVoyageEmbeddingService:
    """Test suite for VoyageEmbeddingService class."""
    
    def test_init_with_api_key(self):
        """Test initialization with explicit API key."""
        with patch('src.job_portal.infrastructure.voyage.embedding_service.voyageai.Client'):
            service = VoyageEmbeddingService(api_key="test_key")
            assert service.api_key == "test_key"
            assert service.model == "voyage-context-3"
            assert service.output_dimension == 1024
    
    def test_init_with_env_variable(self):
        """Test initialization using environment variable."""
        with patch.dict(os.environ, {"VOYAGE_API_KEY": "env_key"}):
            with patch('src.job_portal.infrastructure.voyage.embedding_service.voyageai.Client'):
                service = VoyageEmbeddingService()
                assert service.api_key == "env_key"
    
    def test_init_without_api_key_raises_error(self):
        """Test that missing API key raises ValueError."""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError, match="Voyage API key not found"):
                VoyageEmbeddingService()
    
    def test_init_custom_model_and_dimension(self):
        """Test initialization with custom model and dimension."""
        with patch('src.job_portal.infrastructure.voyage.embedding_service.voyageai.Client'):
            service = VoyageEmbeddingService(
                api_key="test_key",
                model="voyage-3",
                output_dimension=512
            )
            assert service.model == "voyage-3"
            assert service.output_dimension == 512
    
    @patch('src.job_portal.infrastructure.voyage.embedding_service.voyageai.Client')
    def test_embed_query(self, mock_client_class):
        """Test embedding a query."""
        # Setup mock
        mock_client = Mock()
        mock_result = Mock()
        mock_result.results = [Mock(embeddings=[[0.1, 0.2, 0.3]])]
        mock_client.contextualized_embed.return_value = mock_result
        mock_client_class.return_value = mock_client
        
        # Test
        service = VoyageEmbeddingService(api_key="test_key")
        embedding = service.embed_query("test query")
        
        # Assertions
        assert embedding == [0.1, 0.2, 0.3]
        mock_client.contextualized_embed.assert_called_once_with(
            inputs=[["test query"]],
            model="voyage-context-3",
            input_type="query",
            output_dimension=1024
        )
    
    @patch('src.job_portal.infrastructure.voyage.embedding_service.voyageai.Client')
    def test_embed_document_no_chunking(self, mock_client_class):
        """Test embedding a short document without chunking."""
        # Setup mock
        mock_client = Mock()
        mock_result = Mock()
        mock_result.results = [Mock(embeddings=[[0.1, 0.2, 0.3]])]
        mock_client.contextualized_embed.return_value = mock_result
        mock_client_class.return_value = mock_client
        
        # Test
        service = VoyageEmbeddingService(api_key="test_key")
        embedding = service.embed_document("short document", auto_chunk=False)
        
        # Assertions
        assert embedding == [0.1, 0.2, 0.3]
        mock_client.contextualized_embed.assert_called_once_with(
            inputs=[["short document"]],
            model="voyage-context-3",
            input_type="document",
            output_dimension=1024
        )
    
    @patch('src.job_portal.infrastructure.voyage.embedding_service.voyageai.Client')
    def test_embed_document_with_auto_chunking_single_chunk(self, mock_client_class):
        """Test embedding a document that results in a single chunk."""
        # Setup mock
        mock_client = Mock()
        mock_result = Mock()
        mock_result.results = [Mock(embeddings=[[0.1, 0.2, 0.3]])]
        mock_client.contextualized_embed.return_value = mock_result
        mock_client_class.return_value = mock_client
        
        # Test
        service = VoyageEmbeddingService(api_key="test_key")
        embedding = service.embed_document("short document", auto_chunk=True)
        
        # Should return single embedding, not dict
        assert embedding == [0.1, 0.2, 0.3]
    
    @patch('src.job_portal.infrastructure.voyage.embedding_service.voyageai.Client')
    def test_embed_document_with_auto_chunking_multiple_chunks(self, mock_client_class):
        """Test embedding a long document that gets chunked."""
        # Setup mock
        mock_client = Mock()
        mock_result = Mock()
        mock_result.results = [Mock(embeddings=[[0.1, 0.2], [0.3, 0.4]])]
        mock_client.contextualized_embed.return_value = mock_result
        mock_client_class.return_value = mock_client
        
        # Test with a long document
        long_doc = "word " * 300  # Will be chunked
        service = VoyageEmbeddingService(api_key="test_key")
        result = service.embed_document(long_doc, auto_chunk=True)
        
        # Should return dict with embeddings and chunks
        assert isinstance(result, dict)
        assert "embeddings" in result
        assert "chunks" in result
        assert "num_chunks" in result
        assert result["embeddings"] == [[0.1, 0.2], [0.3, 0.4]]
        assert result["num_chunks"] == 2
    
    @patch('src.job_portal.infrastructure.voyage.embedding_service.voyageai.Client')
    def test_embed_documents_batch_no_chunking(self, mock_client_class):
        """Test batch embedding without chunking."""
        # Setup mock
        mock_client = Mock()
        mock_result = Mock()
        mock_result.results = [
            Mock(embeddings=[[0.1, 0.2]]),
            Mock(embeddings=[[0.3, 0.4]])
        ]
        mock_client.contextualized_embed.return_value = mock_result
        mock_client_class.return_value = mock_client
        
        # Test
        service = VoyageEmbeddingService(api_key="test_key")
        embeddings = service.embed_documents_batch(
            ["doc1", "doc2"],
            auto_chunk=False
        )
        
        # Assertions
        assert embeddings == [[0.1, 0.2], [0.3, 0.4]]
        mock_client.contextualized_embed.assert_called_once()
    
    @patch('src.job_portal.infrastructure.voyage.embedding_service.voyageai.Client')
    def test_embed_documents_batch_with_averaging(self, mock_client_class):
        """Test batch embedding with multiple chunks (averaging)."""
        # Setup mock
        mock_client = Mock()
        mock_result = Mock()
        mock_result.results = [
            Mock(embeddings=[[0.1, 0.2], [0.3, 0.4]]),  # 2 chunks
            Mock(embeddings=[[0.5, 0.6]])  # 1 chunk
        ]
        mock_client.contextualized_embed.return_value = mock_result
        mock_client_class.return_value = mock_client
        
        # Test
        service = VoyageEmbeddingService(api_key="test_key")
        embeddings = service.embed_documents_batch(
            ["long doc", "short doc"],
            auto_chunk=False
        )
        
        # First doc should be averaged, second should be as-is
        assert len(embeddings) == 2
        # First embedding is averaged (numpy does this internally)
        assert len(embeddings[0]) == 2
        assert embeddings[1] == [0.5, 0.6]  # Single chunk
    
    @patch('src.job_portal.infrastructure.voyage.embedding_service.voyageai.Client')
    def test_text_splitter_configuration(self, mock_client_class):
        """Test that text splitter is configured correctly."""
        service = VoyageEmbeddingService(api_key="test_key")
        
        # Text splitter uses _chunk_size internally
        assert service.text_splitter._chunk_size == 1000
        assert service.text_splitter._chunk_overlap == 0
        assert service.text_splitter._separators == ["\n\n", "\n", ". ", " "]
