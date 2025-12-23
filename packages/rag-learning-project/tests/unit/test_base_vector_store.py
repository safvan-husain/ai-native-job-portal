"""Unit tests for base vector store."""
import pytest
from unittest.mock import Mock, MagicMock
from bson import ObjectId

from src.job_portal.repositories.base_vector_store import VectorStore


class TestVectorStore:
    """Test suite for VectorStore class."""
    
    def test_init(self):
        """Test initialization."""
        mock_collection = Mock()
        store = VectorStore(mock_collection, vector_index_name="test_index")
        
        assert store.collection == mock_collection
        assert store.vector_index_name == "test_index"
    
    def test_init_default_index_name(self):
        """Test initialization with default index name."""
        mock_collection = Mock()
        store = VectorStore(mock_collection)
        
        assert store.vector_index_name == "vector_index"
    
    def test_insert_document(self):
        """Test inserting a single document."""
        mock_collection = Mock()
        mock_result = Mock()
        mock_result.inserted_id = ObjectId("507f1f77bcf86cd799439011")
        mock_collection.insert_one.return_value = mock_result
        
        store = VectorStore(mock_collection)
        doc = {"name": "test", "embedding": [0.1, 0.2]}
        doc_id = store.insert_document(doc)
        
        mock_collection.insert_one.assert_called_once_with(doc)
        assert doc_id == "507f1f77bcf86cd799439011"
    
    def test_insert_documents(self):
        """Test inserting multiple documents."""
        mock_collection = Mock()
        mock_result = Mock()
        mock_result.inserted_ids = [
            ObjectId("507f1f77bcf86cd799439011"),
            ObjectId("507f1f77bcf86cd799439012")
        ]
        mock_collection.insert_many.return_value = mock_result
        
        store = VectorStore(mock_collection)
        docs = [
            {"name": "test1", "embedding": [0.1, 0.2]},
            {"name": "test2", "embedding": [0.3, 0.4]}
        ]
        doc_ids = store.insert_documents(docs)
        
        mock_collection.insert_many.assert_called_once_with(docs)
        assert len(doc_ids) == 2
        assert doc_ids[0] == "507f1f77bcf86cd799439011"
    
    def test_vector_search_basic(self):
        """Test basic vector search."""
        mock_collection = Mock()
        mock_collection.aggregate.return_value = [
            {"_id": "1", "name": "doc1", "score": 0.95},
            {"_id": "2", "name": "doc2", "score": 0.85}
        ]
        
        store = VectorStore(mock_collection, vector_index_name="test_index")
        query_vector = [0.1, 0.2, 0.3]
        results = store.vector_search(query_vector, limit=2)
        
        assert len(results) == 2
        assert results[0]["score"] == 0.95
        
        # Check pipeline structure
        call_args = mock_collection.aggregate.call_args[0][0]
        assert call_args[0]["$vectorSearch"]["index"] == "test_index"
        assert call_args[0]["$vectorSearch"]["queryVector"] == query_vector
        assert call_args[0]["$vectorSearch"]["limit"] == 2
    
    def test_vector_search_with_filter(self):
        """Test vector search with filter criteria."""
        mock_collection = Mock()
        mock_collection.aggregate.return_value = []
        
        store = VectorStore(mock_collection)
        query_vector = [0.1, 0.2]
        filter_criteria = {"status": "active", "location": "SF"}
        
        store.vector_search(
            query_vector,
            limit=5,
            filter_criteria=filter_criteria
        )
        
        call_args = mock_collection.aggregate.call_args[0][0]
        assert call_args[0]["$vectorSearch"]["filter"] == filter_criteria
    
    def test_vector_search_custom_vector_field(self):
        """Test vector search with custom vector field name."""
        mock_collection = Mock()
        mock_collection.aggregate.return_value = []
        
        store = VectorStore(mock_collection)
        query_vector = [0.1, 0.2]
        
        store.vector_search(
            query_vector,
            vector_field="custom_embedding"
        )
        
        call_args = mock_collection.aggregate.call_args[0][0]
        assert call_args[0]["$vectorSearch"]["path"] == "custom_embedding"
    
    def test_hybrid_search(self):
        """Test hybrid search (vector + metadata)."""
        mock_collection = Mock()
        mock_collection.aggregate.return_value = []
        
        store = VectorStore(mock_collection)
        query_vector = [0.1, 0.2]
        filter_criteria = {"category": "tech"}
        
        store.hybrid_search(
            query_vector,
            filter_criteria,
            limit=10
        )
        
        # Should call aggregate with filter
        call_args = mock_collection.aggregate.call_args[0][0]
        assert call_args[0]["$vectorSearch"]["filter"] == filter_criteria
    
    def test_get_by_id_found(self):
        """Test retrieving document by ID when found."""
        mock_collection = Mock()
        mock_collection.find_one.return_value = {"_id": "123", "name": "test"}
        
        store = VectorStore(mock_collection)
        doc = store.get_by_id("507f1f77bcf86cd799439011")
        
        assert doc["name"] == "test"
        mock_collection.find_one.assert_called_once()
    
    def test_get_by_id_not_found(self):
        """Test retrieving document by ID when not found."""
        mock_collection = Mock()
        mock_collection.find_one.return_value = None
        
        store = VectorStore(mock_collection)
        doc = store.get_by_id("507f1f77bcf86cd799439011")
        
        assert doc is None
    
    def test_update_document_success(self):
        """Test updating a document successfully."""
        mock_collection = Mock()
        mock_result = Mock()
        mock_result.modified_count = 1
        mock_collection.update_one.return_value = mock_result
        
        store = VectorStore(mock_collection)
        success = store.update_document(
            "507f1f77bcf86cd799439011",
            {"status": "inactive"}
        )
        
        assert success is True
        mock_collection.update_one.assert_called_once()
    
    def test_update_document_not_modified(self):
        """Test updating a document that doesn't exist."""
        mock_collection = Mock()
        mock_result = Mock()
        mock_result.modified_count = 0
        mock_collection.update_one.return_value = mock_result
        
        store = VectorStore(mock_collection)
        success = store.update_document(
            "507f1f77bcf86cd799439011",
            {"status": "inactive"}
        )
        
        assert success is False
    
    def test_delete_document_success(self):
        """Test deleting a document successfully."""
        mock_collection = Mock()
        mock_result = Mock()
        mock_result.deleted_count = 1
        mock_collection.delete_one.return_value = mock_result
        
        store = VectorStore(mock_collection)
        success = store.delete_document("507f1f77bcf86cd799439011")
        
        assert success is True
        mock_collection.delete_one.assert_called_once()
    
    def test_delete_document_not_found(self):
        """Test deleting a document that doesn't exist."""
        mock_collection = Mock()
        mock_result = Mock()
        mock_result.deleted_count = 0
        mock_collection.delete_one.return_value = mock_result
        
        store = VectorStore(mock_collection)
        success = store.delete_document("507f1f77bcf86cd799439011")
        
        assert success is False
    
    def test_count_documents_no_filter(self):
        """Test counting all documents."""
        mock_collection = Mock()
        mock_collection.count_documents.return_value = 42
        
        store = VectorStore(mock_collection)
        count = store.count_documents()
        
        assert count == 42
        mock_collection.count_documents.assert_called_once_with({})
    
    def test_count_documents_with_filter(self):
        """Test counting documents with filter."""
        mock_collection = Mock()
        mock_collection.count_documents.return_value = 10
        
        store = VectorStore(mock_collection)
        count = store.count_documents({"status": "active"})
        
        assert count == 10
        mock_collection.count_documents.assert_called_once_with({"status": "active"})
