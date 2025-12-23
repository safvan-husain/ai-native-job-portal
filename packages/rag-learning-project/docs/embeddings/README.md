# Job Portal Vector Database

MongoDB Atlas Vector Search implementation for a job portal system with **Voyage AI contextualized embeddings** for superior semantic matching.

## Features

- **Contextualized Embeddings**: Uses Voyage AI's `voyage-context-3` for context-aware embeddings
- **Vector Search**: Semantic matching between job seekers and companies
- **Hybrid Search**: Combine vector similarity with metadata filtering
- **Dual Collections**: Separate stores for companies (job postings) and job seekers (profiles)
- **Rich Metadata**: Filter by location, experience, skills, company size, remote policy, etc.
- **Auto-Chunking**: Automatically handles long documents while maintaining context

## 🚀 Quick Start

**New to embeddings?** Start here: [`QUICKSTART_EMBEDDINGS.md`](./QUICKSTART_EMBEDDINGS.md)

**Need detailed docs?** See: [`EMBEDDING_GUIDE.md`](./EMBEDDING_GUIDE.md)

## Architecture

### Collections

1. **companies**: Job postings with requirements embeddings
2. **jobseekers**: Candidate profiles with profile embeddings

### Key Components

**Database Layer:**
- `MongoDBConnection`: Connection manager for MongoDB Atlas
- `VectorStore`: Base class with core vector operations
- `CompanyStore`: Company-specific operations (job postings)
- `JobSeekerStore`: Job seeker-specific operations (profiles)

**Embedding Layer (NEW):**
- `VoyageEmbeddingService`: Low-level Voyage AI API wrapper
- `JobPortalEmbeddings`: High-level interface for job portal use cases

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `pymongo` - MongoDB driver
- `voyageai` - Voyage AI embeddings
- `langchain-text-splitters` - Document chunking

### 2. Configure Environment

Create `.env` file:

```env
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority
VOYAGE_API_KEY=pa-your_voyage_api_key_here
```

Get your Voyage API key at: https://www.voyageai.com

### 3. Create Vector Search Indexes

In MongoDB Atlas UI:

1. Navigate to your cluster → Search → Create Search Index
2. Choose "JSON Editor"
3. Use the definitions from `index_definitions.json`

**For Job Seekers Collection:**
- Index name: `jobseeker_vector_index`
- Collection: `jobseekers`
- Vector field: `profile_embedding`
- Dimensions: 1024 (adjust based on your embedding model)
- Similarity: cosine

**For Companies Collection:**
- Index name: `company_vector_index`
- Collection: `companies`
- Vector field: `requirements_embedding`
- Dimensions: 1024 (adjust based on your embedding model)
- Similarity: cosine

## Usage

### Company Operations

```python
from db import MongoDBConnection, CompanyStore

with MongoDBConnection() as conn:
    company_store = CompanyStore(conn.get_collection("companies"))
    
    # Store job posting
    job_id = company_store.store_job_posting(
        company_id="comp_123",
        company_name="TechCorp",
        job_title="Senior Python Developer",
        job_description="Looking for experienced developer...",
        job_requirements_embedding=[0.1] * 1024,  # Your embedding
        company_size="51-200",
        location="San Francisco, CA",
        industry="Technology",
        remote_policy="hybrid",
        required_skills=["Python", "Django", "PostgreSQL"],
        experience_level="senior"
    )
    
    # Search for matching candidates
    matches = company_store.search_matching_candidates(
        candidate_profile_embedding=[0.15] * 1024,
        location="San Francisco",
        remote_policy="hybrid",
        limit=10
    )
```

### Job Seeker Operations

```python
from db import MongoDBConnection, JobSeekerStore

with MongoDBConnection() as conn:
    jobseeker_store = JobSeekerStore(conn.get_collection("jobseekers"))
    
    # Store profile
    profile_id = jobseeker_store.store_profile(
        user_id="user_456",
        name="Jane Doe",
        profile_summary="Experienced Python developer...",
        profile_embedding=[0.2] * 1024,  # Your embedding
        years_of_experience=5.0,
        skills=["Python", "Django", "React"],
        desired_location="San Francisco, CA",
        desired_remote_policy="hybrid",
        desired_salary_min=120000
    )
    
    # Search for matching jobs
    matches = jobseeker_store.search_matching_jobs(
        job_requirements_embedding=[0.18] * 1024,
        min_experience=3.0,
        max_experience=7.0,
        required_skills=["Python"],
        location="San Francisco",
        limit=10
    )
```

## Vector Embeddings

The system expects vector embeddings to be generated from your chosen embedding model. Common options:

- **OpenAI**: `text-embedding-3-small` (1536 dims), `text-embedding-3-large` (3072 dims)
- **Voyage AI**: `voyage-3-large` (2048 dims)
- **Sentence Transformers**: Various models with different dimensions
- **Cohere**: `embed-english-v3.0` (1024 dims)

**Important**: Update `numDimensions` in `index_definitions.json` to match your embedding model.

## Metadata Filtering

Both stores support rich metadata filtering:

### Company Metadata
- `company_size`: "1-10", "11-50", "51-200", "201-500", "500+"
- `location`: City, state, country
- `industry`: Industry sector
- `remote_policy`: "onsite", "hybrid", "remote"
- `experience_level`: "entry", "mid", "senior", "lead"
- `required_skills`: List of skills
- `salary_range`: {"min": float, "max": float}

### Job Seeker Metadata
- `years_of_experience`: Float value
- `skills`: List of skills
- `desired_location`: Preferred location
- `desired_remote_policy`: "onsite", "hybrid", "remote", "any"
- `education_level`: "high_school", "bachelors", "masters", "phd"
- `industries_of_interest`: List of industries
- `availability`: "immediately", "2_weeks", "1_month", "3_months"

## Advanced Features

### Hybrid Search

Combine vector similarity with strict metadata filters:

```python
results = company_store.hybrid_search(
    query_vector=embedding,
    filter_criteria={
        "status": "active",
        "company_size": {"$in": ["51-200", "201-500"]},
        "remote_policy": {"$ne": "onsite"},
        "salary_range.max": {"$gte": 150000}
    },
    limit=10
)
```

### Metadata-Only Filtering

Filter without vector search for traditional queries:

```python
jobs = company_store.filter_by_metadata(
    industry="Technology",
    remote_policy="hybrid",
    salary_min=100000,
    limit=50
)
```

## Best Practices

1. **Index Configuration**: Ensure vector dimensions match your embedding model
2. **Candidate Pool**: Set `num_candidates` to 10-20x your `limit` for better accuracy
3. **Similarity Function**: Use `cosine` for normalized embeddings, `euclidean` or `dotProduct` for others
4. **Filter Strategy**: Apply filters in vector search for better performance vs post-filtering
5. **Embedding Quality**: Use domain-specific or fine-tuned models for better matching

## References

- [MongoDB Atlas Vector Search Documentation](https://www.mongodb.com/docs/atlas/atlas-vector-search/)
- [Vector Search Quick Start](https://www.mongodb.com/docs/atlas/atlas-vector-search/tutorials/vector-search-quick-start/)
- [Create Vector Embeddings](https://www.mongodb.com/docs/atlas/atlas-vector-search/create-embeddings/)
