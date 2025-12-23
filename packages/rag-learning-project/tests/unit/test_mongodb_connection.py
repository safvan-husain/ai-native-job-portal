"""Unit tests for MongoDB connection manager."""
import os
import pytest
from unittest.mock import Mock, patch, MagicMock
from pymongo.errors import ConnectionFailure

from src.job_portal.infrastructure.mongodb.connection import MongoDBConnection


class TestMongoDBConnection:
    """Test suite for MongoDBConnection class."""
    
    def test_init_with_connection_string(self):
        """Test initialization with explicit connection string."""
        conn_str = "mongodb+srv://test:test@cluster.mongodb.net/"
        conn = MongoDBConnection(connection_string=conn_str, database_name="test_db")
        
        assert conn.connection_string == conn_str
        assert conn.database_name == "test_db"
        assert conn._client is None
        assert conn._db is None
    
    def test_init_with_env_variable(self):
        """Test initialization using environment variable."""
        with patch.dict(os.environ, {"MONGODB_URI": "mongodb://localhost:27017"}):
            conn = MongoDBConnection(database_name="test_db")
            assert conn.connection_string == "mongodb://localhost:27017"
    
    def test_init_without_connection_string_raises_error(self):
        """Test that missing connection string raises ValueError."""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError, match="MongoDB connection string not provided"):
                MongoDBConnection()
    
    @patch('src.job_portal.infrastructure.mongodb.connection.MongoClient')
    def test_connect_success(self, mock_client_class):
        """Test successful connection to MongoDB."""
        # Setup mocks
        mock_client = MagicMock()
        mock_db = Mock()
        mock_client.__getitem__ = Mock(return_value=mock_db)
        mock_client.admin.command.return_value = {"ok": 1}
        mock_client_class.return_value = mock_client
        
        # Test connection
        conn = MongoDBConnection(
            connection_string="mongodb://localhost:27017",
            database_name="test_db"
        )
        db = conn.connect()
        
        # Assertions
        mock_client_class.assert_called_once_with("mongodb://localhost:27017")
        mock_client.admin.command.assert_called_once_with('ping')
        assert db == mock_db
        assert conn._client == mock_client
        assert conn._db == mock_db
    
    @patch('src.job_portal.infrastructure.mongodb.connection.MongoClient')
    def test_connect_failure(self, mock_client_class):
        """Test connection failure handling."""
        mock_client = MagicMock()
        mock_client.__getitem__ = Mock(return_value=Mock())
        mock_client.admin.command.side_effect = ConnectionFailure("Connection failed")
        mock_client_class.return_value = mock_client
        
        conn = MongoDBConnection(
            connection_string="mongodb://localhost:27017",
            database_name="test_db"
        )
        
        with pytest.raises(ConnectionFailure):
            conn.connect()
    
    @patch('src.job_portal.infrastructure.mongodb.connection.MongoClient')
    def test_get_database_when_not_connected(self, mock_client_class):
        """Test get_database connects if not already connected."""
        mock_client = MagicMock()
        mock_db = Mock()
        mock_client.__getitem__ = Mock(return_value=mock_db)
        mock_client.admin.command.return_value = {"ok": 1}
        mock_client_class.return_value = mock_client
        
        conn = MongoDBConnection(
            connection_string="mongodb://localhost:27017",
            database_name="test_db"
        )
        
        db = conn.get_database()
        
        assert db == mock_db
        mock_client_class.assert_called_once()
    
    @patch('src.job_portal.infrastructure.mongodb.connection.MongoClient')
    def test_get_database_when_already_connected(self, mock_client_class):
        """Test get_database returns existing connection."""
        mock_client = MagicMock()
        mock_db = Mock()
        mock_client.__getitem__ = Mock(return_value=mock_db)
        mock_client.admin.command.return_value = {"ok": 1}
        mock_client_class.return_value = mock_client
        
        conn = MongoDBConnection(
            connection_string="mongodb://localhost:27017",
            database_name="test_db"
        )
        conn.connect()
        
        # Reset mock to check it's not called again
        mock_client_class.reset_mock()
        
        db = conn.get_database()
        
        assert db == mock_db
        mock_client_class.assert_not_called()
    
    @patch('src.job_portal.infrastructure.mongodb.connection.MongoClient')
    def test_get_collection(self, mock_client_class):
        """Test getting a collection from the database."""
        mock_client = MagicMock()
        mock_db = MagicMock()
        mock_collection = Mock()
        mock_client.__getitem__ = Mock(return_value=mock_db)
        mock_db.__getitem__ = Mock(return_value=mock_collection)
        mock_client.admin.command.return_value = {"ok": 1}
        mock_client_class.return_value = mock_client
        
        conn = MongoDBConnection(
            connection_string="mongodb://localhost:27017",
            database_name="test_db"
        )
        
        collection = conn.get_collection("test_collection")
        
        mock_db.__getitem__.assert_called_once_with("test_collection")
        assert collection == mock_collection
    
    @patch('src.job_portal.infrastructure.mongodb.connection.MongoClient')
    def test_close(self, mock_client_class):
        """Test closing the connection."""
        mock_client = MagicMock()
        mock_db = Mock()
        mock_client.__getitem__ = Mock(return_value=mock_db)
        mock_client.admin.command.return_value = {"ok": 1}
        mock_client_class.return_value = mock_client
        
        conn = MongoDBConnection(
            connection_string="mongodb://localhost:27017",
            database_name="test_db"
        )
        conn.connect()
        conn.close()
        
        mock_client.close.assert_called_once()
        assert conn._client is None
        assert conn._db is None
    
    @patch('src.job_portal.infrastructure.mongodb.connection.MongoClient')
    def test_context_manager(self, mock_client_class):
        """Test using connection as context manager."""
        mock_client = MagicMock()
        mock_db = Mock()
        mock_client.__getitem__ = Mock(return_value=mock_db)
        mock_client.admin.command.return_value = {"ok": 1}
        mock_client_class.return_value = mock_client
        
        with MongoDBConnection(
            connection_string="mongodb://localhost:27017",
            database_name="test_db"
        ) as conn:
            assert conn._client is not None
            assert conn._db is not None
        
        mock_client.close.assert_called_once()
