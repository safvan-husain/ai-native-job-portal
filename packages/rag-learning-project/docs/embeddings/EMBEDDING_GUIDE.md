# Voyage AI Contextualized Embeddings - Implementation Guide

## Overview

This job portal now uses **Voyage AI's `voyage-context-3`** model for generating contextualized chunk embeddings. This provides superior retrieval accuracy compared to standard embeddings, especially when job descriptions or candidate profiles are split across multiple chunks.

## Why Voyage AI Contextualized Embeddings?

### Key Benefits

1. **Context-Aware Chunking**: When documents are split into chunks, each chunk maintains awareness of the surrounding context
2. **Perfect Dimension Match**: 1024 dimensions (default) matches your existing MongoDB vector indexes
3. **Optimized for Retrieval**: Built specifically for search/retrieval tasks with query and document modes
4. **Drop-in Replacement**: Works seamlessly with your existing MongoDB Atlas Vector Search setup

### Example Problem Solved

**Without Contextualized Embeddings:**
```
Chunk 1: "The company's revenue increased by 15%"
Chunk 2: "This is Leafy Inc.'s Q2 2024 SEC filing"
```
❌ Chunk 1 loses context about which company it refers to

**With Contextualized Embeddings:**
```
Chunk 1: "The company's revenue increased by 15%" [knows it's about Leafy Inc. Q2 2024]
Chunk 2: "This is Leafy Inc.'s Q2 2024 SEC filing" [provides context to other chunks]
```
✅ Both chunks maintain document-level context

## Setup

### 1. Install Dependencies

```bash
pip install voyageai langchain-text-splitters
```

Or install all requirements:
```bash
pip install -r requirements.txt
```

### 2. Get Voyage AI API Key

1. Visit [https://www.voyageai.com](https://www.voyageai.com)
2. Sign up for an account
3. Navigate to API Keys section
4. Create a new API key

### 3. Configure Environment

Create a `.env` file (copy from `.env.example`):

```bash
cp .env.example .env
```

Add your API keys:
```env
MONGODB_URI=mongodb+srv://your_connection_string
VOYAGE_API_KEY=your_voyage_api_key_here
```

## Usage

### Basic Embedding Service

```python
from src.db.embedding_service import VoyageEmbeddingService

# Initialize service
embeddings = VoyageEmbeddingService()

# Embed a query
query_embedding = embeddings.embed_query("Looking for Python developer")

# Embed a document
doc_embedding = embeddings.embed_document(
    "Senior Python Developer with 5 years experience...",
    auto_chunk=True  # Automatically chunk long documents
)

# Batch embed multiple documents
doc_embeddings = embeddings.embed_documents_batch([
    "Job posting 1...",
    "Job posting 2...",
    "Job posting 3..."
])
```

### Job Portal High-Level Interface

```python
from src.db.job_portal_embeddings import JobPortalEmbeddings

# Initialize
embeddings = JobPortalEmbeddings()

# Embed a job posting
job_embedding = embeddings.embed_job_posting(
    job_title="Senior Python Developer",
    job_description="We are seeking an experienced Python developer...",
    required_skills=["Python", "Django", "PostgreSQL"],
    experience_level="senior"
)

# Embed a candidate profile
candidate_embedding = embeddings.embed_candidate_profile(
    name="Alice Johnson",
    current_title="Senior Software Engineer",
    profile_summary="Experienced Python developer with 6 years...",
    skills=["Python", "Django", "FastAPI"],
    years_of_experience=6.0,
    education="Bachelor's in Computer Science"
)

# Embed a job search query
search_embedding = embeddings.embed_job_search_query(
    desired_role="Python Backend Developer",
    desired_skills=["Python", "Django"],
    experience_level="senior"
)
```

### Complete Example with MongoDB

```python
from dotenv import load_dotenv
from src.db.connection import MongoDBConnection
from src.db.company_store import CompanyStore
from src.db.job_portal_embeddings import JobPortalEmbeddings

load_dotenv()

# Initialize
embeddings = JobPortalEmbeddings()

with MongoDBConnection() as db:
    company_store = CompanyStore(db["companies"])
    
    # Generate embedding
    job_embedding = embeddings.embed_job_posting(
        job_title="Senior Python Developer",
        job_description="Build scalable APIs...",
        required_skills=["Python", "Django"],
        experience_level="senior"
    )
    
    # Store with embedding
    job_id = company_store.store_job_posting(
        company_id="tech_001",
        company_name="TechCorp",
        job_title="Senior Python Developer",
        job_description="Build scalable APIs...",
        job_requirements_embedding=job_embedding,
        company_size="51-200",
        location="San Francisco, CA",
        industry="Technology",
        remote_policy="hybrid",
        required_skills=["Python", "Django"],
        experience_level="senior"
    )
    
    # Search for matching candidates
    search_query = embeddings.embed_candidate_search_query(
        job_title="Senior Python Developer",
        required_skills=["Python", "Django"]
    )
    
    matches = company_store.search_matching_candidates(
        candidate_profile_embedding=search_query,
        location="San Francisco",
        limit=10
    )
```

## Model Specifications

### voyage-context-3

- **Dimensions**: 1024 (default), also supports 256, 512, 2048
- **Context Length**: 32,000 tokens
- **Similarity**: Cosine (normalized embeddings)
- **Use Cases**: General-purpose and multilingual retrieval

### Input Types

- **`query`**: For search queries (adds retrieval-optimized prompt)
- **`document`**: For storing documents (adds document-optimized prompt)
- **`None`**: Raw embeddings without prompts

### Output Types

- **`float`**: 32-bit floating point (default, highest precision)
- **`int8`**: 8-bit integers (-128 to 127)
- **`uint8`**: 8-bit unsigned integers (0 to 255)
- **`binary`**: Bit-packed binary embeddings
- **`ubinary`**: Unsigned bit-packed binary embeddings

## Best Practices

### 1. Chunking Strategy

```python
# Voyage recommends NO overlap for contextualized embeddings
text_splitter = RecursiveCharacterTextSplitter(
    separators=["\n\n", "\n", ". ", " "],
    chunk_size=1000,
    chunk_overlap=0  # No overlap!
)
```

### 2. Query vs Document Embeddings

```python
# Always use input_type for better retrieval
query_emb = embeddings.embed_query("search text")  # input_type="query"
doc_emb = embeddings.embed_document("doc text")    # input_type="document"
```

### 3. Batch Processing

```python
# Process multiple documents at once for efficiency
embeddings_list = embeddings.embed_documents_batch([
    "document 1",
    "document 2",
    "document 3"
])
```

### 4. Long Documents

```python
# Enable auto-chunking for long documents
result = embeddings.embed_document(
    long_document,
    auto_chunk=True  # Automatically chunks if needed
)

# Result can be:
# - Single embedding (if document is short)
# - Dict with 'embeddings' and 'chunks' keys (if chunked)
```

## Pricing

Voyage AI pricing is based on tokens processed. Check current pricing at:
https://docs.voyageai.com/docs/pricing

Typical costs:
- `voyage-context-3`: ~$0.12 per 1M tokens

## Troubleshooting

### API Key Not Found

```
ValueError: Voyage API key not found
```

**Solution**: Set `VOYAGE_API_KEY` in your `.env` file or environment variables.

### Import Error

```
ModuleNotFoundError: No module named 'voyageai'
```

**Solution**: Install the package:
```bash
pip install voyageai
```

### Dimension Mismatch

```
Vector dimension mismatch
```

**Solution**: Ensure `output_dimension=1024` matches your MongoDB index configuration.

## Migration from Dummy Embeddings

If you have existing data with dummy embeddings:

1. **Regenerate embeddings** for all existing documents
2. **Update documents** with new embeddings
3. **Test search quality** with real embeddings

```python
# Example migration script
from src.db.connection import MongoDBConnection
from src.db.job_portal_embeddings import JobPortalEmbeddings

embeddings = JobPortalEmbeddings()

with MongoDBConnection() as db:
    companies = db["companies"]
    
    # Update all job postings
    for job in companies.find({}):
        new_embedding = embeddings.embed_job_posting(
            job_title=job["job_title"],
            job_description=job["job_description"],
            required_skills=job.get("required_skills", []),
            experience_level=job.get("experience_level")
        )
        
        companies.update_one(
            {"_id": job["_id"]},
            {"$set": {"requirements_embedding": new_embedding}}
        )
```

## Additional Resources

- **Voyage AI Documentation**: https://docs.voyageai.com
- **Contextualized Embeddings Guide**: https://docs.voyageai.com/docs/contextualized-chunk-embeddings
- **MongoDB Vector Search**: https://www.mongodb.com/docs/atlas/atlas-vector-search/
- **Example Code**: `scripts/demos/example_with_embeddings.py`

## Support

For issues or questions:
- Voyage AI: https://docs.voyageai.com/docs/contact-email
- MongoDB: https://www.mongodb.com/docs/atlas/support/
