"""Voyage AI Contextualized Embedding Service for Job Portal."""
import os
from typing import List, Dict, Any, Optional, Union
import voyageai
from langchain_text_splitters import RecursiveCharacterTextSplitter


class VoyageEmbeddingService:
    """
    Service for generating contextualized embeddings using Voyage AI.
    
    Uses voyage-context-3 model which provides context-aware embeddings
    that maintain document-level context across chunks, improving retrieval
    accuracy for job postings and candidate profiles.
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "voyage-context-3",
        output_dimension: int = 1024
    ):
        """
        Initialize Voyage AI embedding service.
        
        Args:
            api_key: Voyage AI API key (defaults to VOYAGE_API_KEY env var)
            model: Model name (default: voyage-context-3)
            output_dimension: Embedding dimension (default: 1024)
        """
        self.api_key = api_key or os.getenv("VOYAGE_API_KEY")
        if not self.api_key:
            raise ValueError(
                "Voyage API key not found. Set VOYAGE_API_KEY environment variable "
                "or pass api_key parameter."
            )
        
        self.client = voyageai.Client(api_key=self.api_key)
        self.model = model
        self.output_dimension = output_dimension
        
        # Text splitter for chunking long documents
        self.text_splitter = RecursiveCharacterTextSplitter(
            separators=["\n\n", "\n", ". ", " "],
            chunk_size=1000,
            chunk_overlap=0  # Voyage recommends no overlap for contextualized embeddings
        )
    
    def embed_query(self, query: str) -> List[float]:
        """
        Generate embedding for a search query.
        
        Args:
            query: Search query text
            
        Returns:
            Query embedding vector
        """
        result = self.client.contextualized_embed(
            inputs=[[query]],
            model=self.model,
            input_type="query",
            output_dimension=self.output_dimension
        )
        return result.results[0].embeddings[0]
    
    def embed_document(
        self,
        document: str,
        auto_chunk: bool = True
    ) -> Union[List[float], Dict[str, Any]]:
        """
        Generate contextualized embedding for a document.
        
        Args:
            document: Document text (job posting or candidate profile)
            auto_chunk: If True, automatically chunk long documents
            
        Returns:
            If auto_chunk=False: Single embedding vector
            If auto_chunk=True: Dict with 'embeddings' and 'chunks' keys
        """
        if auto_chunk:
            chunks = self.text_splitter.split_text(document)
            
            # If document is short enough, don't chunk
            if len(chunks) == 1:
                result = self.client.contextualized_embed(
                    inputs=[[document]],
                    model=self.model,
                    input_type="document",
                    output_dimension=self.output_dimension
                )
                return result.results[0].embeddings[0]
            
            # Generate contextualized embeddings for chunks
            result = self.client.contextualized_embed(
                inputs=[chunks],
                model=self.model,
                input_type="document",
                output_dimension=self.output_dimension
            )
            
            return {
                "embeddings": result.results[0].embeddings,
                "chunks": chunks,
                "num_chunks": len(chunks)
            }
        else:
            result = self.client.contextualized_embed(
                inputs=[[document]],
                model=self.model,
                input_type="document",
                output_dimension=self.output_dimension
            )
            return result.results[0].embeddings[0]
    
    def embed_documents_batch(
        self,
        documents: List[str],
        auto_chunk: bool = False
    ) -> List[List[float]]:
        """
        Generate embeddings for multiple documents in batch.
        
        Args:
            documents: List of document texts
            auto_chunk: If True, automatically chunk each document
            
        Returns:
            List of embedding vectors (one per document)
            
        Note:
            If auto_chunk=True, each document's chunks are averaged into
            a single embedding for simplicity. For advanced use cases,
            use embed_document() individually.
        """
        if auto_chunk:
            # Chunk each document
            chunked_docs = [self.text_splitter.split_text(doc) for doc in documents]
        else:
            # Treat each document as a single chunk
            chunked_docs = [[doc] for doc in documents]
        
        # Generate contextualized embeddings
        result = self.client.contextualized_embed(
            inputs=chunked_docs,
            model=self.model,
            input_type="document",
            output_dimension=self.output_dimension
        )
        
        # Return first embedding from each document (or average if multiple chunks)
        embeddings = []
        for doc_result in result.results:
            if len(doc_result.embeddings) == 1:
                embeddings.append(doc_result.embeddings[0])
            else:
                # Average embeddings if document has multiple chunks
                import numpy as np
                avg_embedding = np.mean(doc_result.embeddings, axis=0).tolist()
                embeddings.append(avg_embedding)
        
        return embeddings
