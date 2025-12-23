"""Base vector store interface for MongoDB Atlas Vector Search."""
from typing import List, Dict, Any, Optional
from pymongo.collection import Collection


class VectorStore:
    """Base class for vector storage and retrieval operations."""
    
    def __init__(self, collection: Collection, vector_index_name: str = "vector_index"):
        """
        Initialize vector store.
        
        Args:
            collection: MongoDB collection instance
            vector_index_name: Name of the vector search index
        """
        self.collection = collection
        self.vector_index_name = vector_index_name
    
    def insert_document(self, document: Dict[str, Any]) -> str:
        """
        Insert a single document with vector embedding.
        
        Args:
            document: Document containing vector embedding and metadata
            
        Returns:
            Inserted document ID as string
        """
        result = self.collection.insert_one(document)
        return str(result.inserted_id)
    
    def insert_documents(self, documents: List[Dict[str, Any]]) -> List[str]:
        """
        Insert multiple documents with vector embeddings.
        
        Args:
            documents: List of documents containing vector embeddings and metadata
            
        Returns:
            List of inserted document IDs as strings
        """
        result = self.collection.insert_many(documents)
        return [str(id) for id in result.inserted_ids]
    
    def vector_search(
        self,
        query_vector: List[float],
        limit: int = 10,
        num_candidates: int = 100,
        filter_criteria: Optional[Dict[str, Any]] = None,
        vector_field: str = "embedding"
    ) -> List[Dict[str, Any]]:
        """
        Perform vector similarity search using MongoDB Atlas Vector Search.
        
        Args:
            query_vector: Query vector embedding
            limit: Number of results to return
            num_candidates: Number of candidates for ANN search (should be >= limit)
            filter_criteria: Optional pre-filter criteria for hybrid search
            vector_field: Name of the field containing vector embeddings
            
        Returns:
            List of matching documents with similarity scores
        """
        pipeline = [
            {
                "$vectorSearch": {
                    "index": self.vector_index_name,
                    "path": vector_field,
                    "queryVector": query_vector,
                    "numCandidates": num_candidates,
                    "limit": limit
                }
            },
            {
                "$addFields": {
                    "score": {"$meta": "vectorSearchScore"}
                }
            }
        ]
        
        # Add filter if provided
        if filter_criteria:
            pipeline[0]["$vectorSearch"]["filter"] = filter_criteria
        
        results = list(self.collection.aggregate(pipeline))
        return results
    
    def hybrid_search(
        self,
        query_vector: List[float],
        filter_criteria: Dict[str, Any],
        limit: int = 10,
        num_candidates: int = 100,
        vector_field: str = "embedding"
    ) -> List[Dict[str, Any]]:
        """
        Perform hybrid search combining vector similarity and metadata filtering.
        
        Args:
            query_vector: Query vector embedding
            filter_criteria: Metadata filter criteria (e.g., location, company_size)
            limit: Number of results to return
            num_candidates: Number of candidates for ANN search
            vector_field: Name of the field containing vector embeddings
            
        Returns:
            List of matching documents with similarity scores
        """
        return self.vector_search(
            query_vector=query_vector,
            limit=limit,
            num_candidates=num_candidates,
            filter_criteria=filter_criteria,
            vector_field=vector_field
        )
    
    def get_by_id(self, document_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a document by its ID.
        
        Args:
            document_id: Document ID
            
        Returns:
            Document if found, None otherwise
        """
        from bson import ObjectId
        return self.collection.find_one({"_id": ObjectId(document_id)})
    
    def update_document(self, document_id: str, update_data: Dict[str, Any]) -> bool:
        """
        Update a document.
        
        Args:
            document_id: Document ID
            update_data: Fields to update
            
        Returns:
            True if updated, False otherwise
        """
        from bson import ObjectId
        result = self.collection.update_one(
            {"_id": ObjectId(document_id)},
            {"$set": update_data}
        )
        return result.modified_count > 0
    
    def delete_document(self, document_id: str) -> bool:
        """
        Delete a document.
        
        Args:
            document_id: Document ID
            
        Returns:
            True if deleted, False otherwise
        """
        from bson import ObjectId
        result = self.collection.delete_one({"_id": ObjectId(document_id)})
        return result.deleted_count > 0
    
    def count_documents(self, filter_criteria: Optional[Dict[str, Any]] = None) -> int:
        """
        Count documents matching filter criteria.
        
        Args:
            filter_criteria: Optional filter criteria
            
        Returns:
            Number of matching documents
        """
        return self.collection.count_documents(filter_criteria or {})
