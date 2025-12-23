# LangChain Tools Reference

This document provides a quick reference for all available tools in the job portal agent.

## Overview

The job portal has **6 LangChain tools** divided into two categories:
- **Job Seeker Tools** (3): For candidates searching for jobs
- **Company Tools** (3): For companies searching for candidates

All tools use vector similarity search powered by MongoDB Atlas and Voyage AI embeddings.

---

## Job Seeker Tools

### 1. search_jobs

**Purpose**: Search for job postings that match given requirements.

**Input**:
- `requirements` (str): Job requirements as natural language text
- `limit` (int, optional): Maximum results to return (default: 5)

**Output**: Formatted string with matching job postings including:
- Company name
- Job title
- Location
- Remote policy
- Experience level
- Match score
- Document ID

**Example**:
```python
from src.job_portal.agent.tools import search_jobs

result = search_jobs.invoke({
    "requirements": "Python developer with 5 years experience in Django",
    "limit": 3
})
print(result)
```

**Sample Output**:
```
Found 2 matching job posting(s):

1. Tech Corp
   Job: Senior Python Developer
   Location: San Francisco, CA
   Remote: hybrid
   Experience: mid
   Match Score: 0.950
   ID: 507f1f77bcf86cd799439011

2. Data Inc
   Job: Python Engineer
   Location: New York, NY
   Remote: remote
   Experience: senior
   Match Score: 0.880
   ID: 507f1f77bcf86cd799439012
```

---

### 2. get_company_details

**Purpose**: Get detailed information about a specific company and job posting.

**Input**:
- `company_id` (str): MongoDB ObjectId of the company document

**Output**: Formatted string with complete company details including:
- Company name and size
- Job title and description
- Industry and location
- Remote policy
- Experience level
- Salary range
- Required skills

**Example**:
```python
from src.job_portal.agent.tools import get_company_details

result = get_company_details.invoke({
    "company_id": "507f1f77bcf86cd799439011"
})
print(result)
```

**Sample Output**:
```
Company: Tech Corp
Job Title: Senior Python Developer
Company Size: 51-200
Industry: Technology
Location: San Francisco, CA
Remote Policy: hybrid
Experience Level: mid
Salary Range: $80,000 - $120,000
Required Skills: Python, Django, PostgreSQL, Docker

Job Description:
We are looking for a talented Python developer to join our growing team...
```

---

### 3. compare_companies

**Purpose**: Compare multiple companies side-by-side.

**Input**:
- `company_ids` (str): Comma-separated list of MongoDB ObjectIds

**Output**: Formatted comparison table of companies.

**Constraints**:
- Minimum: 2 companies
- Maximum: 5 companies

**Example**:
```python
from src.job_portal.agent.tools import compare_companies

result = compare_companies.invoke({
    "company_ids": "507f1f77bcf86cd799439011,507f1f77bcf86cd799439012"
})
print(result)
```

**Sample Output**:
```
Comparing 2 job opportunities:

============================================================
Option 1: Tech Corp
============================================================
Job Title: Senior Python Developer
Location: San Francisco, CA
Remote: hybrid
Experience: mid
Company Size: 51-200
Industry: Technology
Salary: $80,000 - $120,000
Skills: Python, Django, PostgreSQL, Docker, AWS

============================================================
Option 2: Data Inc
============================================================
Job Title: Python Engineer
Location: New York, NY
Remote: remote
Experience: senior
Company Size: 201-500
Industry: Data Science
Salary: $100,000 - $150,000
Skills: Python, ML, TensorFlow, Spark, AWS
```

---

## Company Tools

### 4. search_candidates

**Purpose**: Search for candidates that match given job requirements.

**Input**:
- `job_requirements` (str): Job requirements as natural language text
- `limit` (int, optional): Maximum results to return (default: 5)

**Output**: Formatted string with matching candidates including:
- Name
- Current title
- Years of experience
- Location preference
- Remote preference
- Education level
- Match score
- Document ID

**Example**:
```python
from src.job_portal.agent.tools import search_candidates

result = search_candidates.invoke({
    "job_requirements": "Senior Python developer with ML experience",
    "limit": 3
})
print(result)
```

**Sample Output**:
```
Found 2 matching candidate(s):

1. John Doe
   Title: Python Developer
   Experience: 5 years
   Location: San Francisco, CA
   Remote Preference: hybrid
   Education: bachelors
   Match Score: 0.920
   ID: 507f1f77bcf86cd799439021

2. Jane Smith
   Title: Senior Python Engineer
   Experience: 8 years
   Location: Remote
   Remote Preference: remote
   Education: masters
   Match Score: 0.890
   ID: 507f1f77bcf86cd799439022
```

---

### 5. get_candidate_details

**Purpose**: Get detailed information about a specific candidate.

**Input**:
- `candidate_id` (str): MongoDB ObjectId of the candidate document

**Output**: Formatted string with complete candidate details including:
- Name and current title
- Years of experience
- Education level
- Location and remote preferences
- Availability
- Desired salary
- Skills
- Industries of interest
- Profile summary

**Example**:
```python
from src.job_portal.agent.tools import get_candidate_details

result = get_candidate_details.invoke({
    "candidate_id": "507f1f77bcf86cd799439021"
})
print(result)
```

**Sample Output**:
```
Candidate: John Doe
Current Title: Python Developer
Experience: 5 years
Education: bachelors
Desired Location: San Francisco, CA
Remote Preference: hybrid
Availability: immediately
Desired Salary: $100,000+
Skills: Python, Django, PostgreSQL, Docker, AWS, React
Industries of Interest: Technology, FinTech

Profile Summary:
Experienced Python developer with strong backend skills and a passion for building
scalable web applications. Proficient in Django, REST APIs, and cloud deployment...
```

---

### 6. compare_candidates

**Purpose**: Compare multiple candidates side-by-side.

**Input**:
- `candidate_ids` (str): Comma-separated list of MongoDB ObjectIds

**Output**: Formatted comparison table of candidates.

**Constraints**:
- Minimum: 2 candidates
- Maximum: 5 candidates

**Example**:
```python
from src.job_portal.agent.tools import compare_candidates

result = compare_candidates.invoke({
    "candidate_ids": "507f1f77bcf86cd799439021,507f1f77bcf86cd799439022"
})
print(result)
```

**Sample Output**:
```
Comparing 2 candidates:

============================================================
Candidate 1: John Doe
============================================================
Title: Python Developer
Experience: 5 years
Education: bachelors
Location: San Francisco, CA
Remote: hybrid
Availability: immediately
Desired Salary: $100,000+
Skills: Python, Django, PostgreSQL, Docker, AWS

============================================================
Candidate 2: Jane Smith
============================================================
Title: Senior Python Engineer
Experience: 8 years
Education: masters
Location: Remote
Remote: remote
Availability: 2_weeks
Desired Salary: $130,000+
Skills: Python, ML, TensorFlow, Spark, Kubernetes
```

---

## Technical Details

### Tool Implementation

All tools are implemented using LangChain's `@tool` decorator:

```python
from langchain_core.tools import tool

@tool
def search_jobs(requirements: str, limit: int = 5) -> str:
    """
    Search for job postings that match the given requirements.
    
    Args:
        requirements: Job requirements as natural language text
        limit: Maximum number of results to return
        
    Returns:
        Formatted string with matching job postings
    """
    # Implementation...
```

### Architecture

```
Tool Layer (LangChain tools)
    ↓
Service Layer (JobPortalEmbeddings)
    ↓
Repository Layer (CompanyStore, JobSeekerStore)
    ↓
Infrastructure Layer (MongoDB, Voyage AI)
```

### Dependencies

- **LangChain**: Tool framework
- **MongoDB Atlas**: Vector storage
- **Voyage AI**: Embedding generation
- **PyMongo**: MongoDB driver

### Lazy Loading

All tools use lazy loading for database connections:

```python
_db_connection = None
_company_store = None
_embeddings = None

def _get_company_store() -> CompanyStore:
    """Get or create company store instance."""
    global _db_connection, _company_store
    if _company_store is None:
        _db_connection = MongoDBConnection()
        collection = _db_connection.get_collection("companies")
        _company_store = CompanyStore(collection)
    return _company_store
```

This ensures:
- Fast import times
- Connections only created when needed
- Shared connections across tool calls

### Error Handling

All tools include try-except blocks:

```python
try:
    # Tool logic
    return formatted_result
except Exception as e:
    return f"Error: {str(e)}"
```

---

## Testing

### Unit Tests

Run all tool tests:
```bash
python -m pytest tests/agent/test_tools.py -v
```

Expected output:
```
20 passed in 2.23s
```

### Manual Testing

Test tools directly without agent:
```bash
python scripts/demos/test_tools_directly.py
```

### Test Coverage

- ✅ Successful searches
- ✅ Empty results
- ✅ Document retrieval
- ✅ Not found cases
- ✅ Comparison with valid IDs
- ✅ Comparison with too few IDs
- ✅ Comparison with too many IDs
- ✅ Tool schema validation

---

## Usage in Agent

These tools will be integrated into the LangChain agent in Phase 4:

```python
from langchain.agents import create_react_agent
from src.job_portal.agent.tools import (
    search_jobs,
    get_company_details,
    compare_companies
)

tools = [search_jobs, get_company_details, compare_companies]
agent = create_react_agent(llm, tools, prompt)
```

---

## Rate Limits

⚠️ **Important**: All search tools use Voyage AI embeddings.

**Free Tier Limits**:
- 3 requests per minute (RPM)
- 10,000 tokens per minute (TPM)

**Recommendation**: Add delays between tool calls in production:
```python
import time
result1 = search_jobs.invoke({"requirements": "..."})
time.sleep(20)  # Wait 20 seconds
result2 = search_jobs.invoke({"requirements": "..."})
```

See `docs/embeddings/RATE_LIMITS.md` for details.

---

## Next Steps

- **Phase 4**: Integrate tools with LangChain agent
- **Phase 5**: Build CLI interface
- **Phase 6**: Add conversation memory
- **Phase 7**: Production deployment

---

**Last Updated**: November 27, 2025
**Status**: ✅ Phase 3 Complete - All 6 tools implemented and tested
