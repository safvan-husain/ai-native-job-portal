"""MongoDB connection manager for Atlas Vector Search."""
import os
from typing import Optional
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection


class MongoDBConnection:
    """Manages MongoDB Atlas connection and database access."""
    
    def __init__(self, connection_string: Optional[str] = None, database_name: str = "job_portal"):
        """
        Initialize MongoDB connection.
        
        Args:
            connection_string: MongoDB Atlas connection string. If None, reads from MONGODB_URI env var
            database_name: Name of the database to use
        """
        self.connection_string = connection_string or os.getenv("MONGODB_URI")
        if not self.connection_string:
            raise ValueError("MongoDB connection string not provided. Set MONGODB_URI environment variable.")
        
        self.database_name = database_name
        self._client: Optional[MongoClient] = None
        self._db: Optional[Database] = None
    
    def connect(self) -> Database:
        """
        Establish connection to MongoDB Atlas.
        
        Returns:
            Database instance
        """
        if self._client is None:
            self._client = MongoClient(self.connection_string)
            self._db = self._client[self.database_name]
            # Test connection
            self._client.admin.command('ping')
            print(f"Successfully connected to MongoDB Atlas - Database: {self.database_name}")
        
        return self._db
    
    def get_database(self) -> Database:
        """Get database instance, connecting if necessary."""
        if self._db is None:
            return self.connect()
        return self._db
    
    def get_collection(self, collection_name: str) -> Collection:
        """
        Get a collection from the database.
        
        Args:
            collection_name: Name of the collection
            
        Returns:
            Collection instance
        """
        db = self.get_database()
        return db[collection_name]
    
    def close(self):
        """Close the MongoDB connection."""
        if self._client:
            self._client.close()
            self._client = None
            self._db = None
            print("MongoDB connection closed")
    
    def __enter__(self):
        """Context manager entry."""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
