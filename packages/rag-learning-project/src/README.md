# Source Code

Python modules for your RAG implementation.

## Structure

```
src/
├── __init__.py
├── embeddings/
│   ├── __init__.py
│   └── embedding_generator.py    # Generate embeddings
├── retrieval/
│   ├── __init__.py
│   ├── vector_store.py           # Vector database interface
│   └── retriever.py              # Retrieval logic
├── generation/
│   ├── __init__.py
│   └── llm_client.py             # LLM integration
├── processing/
│   ├── __init__.py
│   ├── document_loader.py        # Load various file types
│   └── text_splitter.py          # Chunk documents
└── rag_system.py                 # Main RAG orchestrator
```

## Usage Pattern

```python
from src.rag_system import RAGSystem

# Initialize
rag = RAGSystem()

# Ingest documents
rag.ingest_documents("./data")

# Query
response = rag.query("What is RAG?")
print(response)
```

## Development

- Follow PEP 8 style guidelines
- Add docstrings to all functions
- Write unit tests for core functionality
- Use type hints where appropriate
