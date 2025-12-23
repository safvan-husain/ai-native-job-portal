# Unit Tests

This directory contains unit tests for the Job Portal RAG system.

## Overview

Unit tests are fast, isolated tests that verify individual components without external dependencies. All external services (MongoDB, Voyage AI) are mocked.

## Test Coverage

### Infrastructure Layer
- **`test_mongodb_connection.py`** - MongoDB connection manager
  - Connection initialization
  - Database/collection access
  - Context manager behavior
  - Error handling

- **`test_embedding_service.py`** - Voyage AI embedding service
  - Query embeddings
  - Document embeddings
  - Batch processing
  - Chunking behavior

### Repository Layer
- **`test_base_vector_store.py`** - Base vector store operations
  - CRUD operations
  - Vector search
  - Hybrid search
  - Document counting

- **`test_company_repository.py`** - Company/job posting repository
  - Storing job postings
  - Searching for candidates
  - Metadata filtering
  - Status updates

- **`test_jobseeker_repository.py`** - Job seeker repository
  - Storing profiles
  - Searching for jobs
  - Metadata filtering
  - Status updates

### Service Layer
- **`test_job_portal_embeddings.py`** - High-level embedding service
  - Job posting embeddings
  - Candidate profile embeddings
  - Search query embeddings
  - Query builders

## Running Tests

### Run all unit tests
```bash
pytest tests/unit/
```

### Run specific test file
```bash
pytest tests/unit/test_embedding_service.py
```

### Run specific test
```bash
pytest tests/unit/test_embedding_service.py::TestVoyageEmbeddingService::test_embed_query
```

### Run with coverage
```bash
pytest tests/unit/ --cov=src --cov-report=html
```

### Run with verbose output
```bash
pytest tests/unit/ -v
```

### Run only fast tests (exclude slow ones)
```bash
pytest tests/unit/ -m "not slow"
```

## Test Structure

Each test file follows this pattern:

```python
"""Unit tests for [module name]."""
import pytest
from unittest.mock import Mock, patch

from src.job_portal.[module] import [Class]


class Test[ClassName]:
    """Test suite for [ClassName] class."""
    
    def test_[feature]_[scenario](self):
        """Test [what is being tested]."""
        # Arrange
        mock_dependency = Mock()
        
        # Act
        result = function_under_test()
        
        # Assert
        assert result == expected
```

## Fixtures

Shared fixtures are defined in `conftest.py`:

- `mock_mongodb_collection` - Mock MongoDB collection
- `mock_voyage_client` - Mock Voyage AI client
- `sample_embedding` - Sample 1024-dim embedding vector
- `sample_job_posting` - Sample job posting document
- `sample_candidate_profile` - Sample candidate profile

## Best Practices

1. **Fast**: Unit tests should run in milliseconds
2. **Isolated**: No external API calls or database connections
3. **Focused**: Test one thing per test
4. **Clear**: Test names describe what is being tested
5. **Mocked**: All external dependencies are mocked

## Coverage Goals

Target: **80%+ code coverage** for core modules

Current coverage by module:
- Infrastructure: ✅ Fully tested
- Repositories: ✅ Fully tested
- Services: ✅ Fully tested
- CLI: ⏳ Pending
- Agent: ⏳ Pending

## Adding New Tests

When adding new functionality:

1. Create test file: `test_[module_name].py`
2. Create test class: `Test[ClassName]`
3. Add test methods: `test_[feature]_[scenario]`
4. Mock external dependencies
5. Use fixtures from `conftest.py`
6. Run tests to verify coverage

## Troubleshooting

### Import Errors
If you get import errors, ensure you're running from the project root:
```bash
cd /path/to/rag-learning-project
pytest tests/unit/
```

### Mock Not Working
Make sure to patch at the point of use, not where it's defined:
```python
# Correct
@patch('src.job_portal.services.embeddings.job_portal_embeddings.VoyageEmbeddingService')

# Incorrect
@patch('src.job_portal.infrastructure.voyage.embedding_service.VoyageEmbeddingService')
```

### Coverage Not Showing
Install pytest-cov:
```bash
pip install pytest-cov
```

## Related Documentation

- Integration tests: `tests/integration/README.md`
- Project progress: `docs/overview/PROJECT_PROGRESS.md`
- Embedding guide: `docs/embeddings/EMBEDDING_GUIDE.md`
