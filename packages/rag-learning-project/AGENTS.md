# AI Agent Guide - RAG Learning Project

This document provides guidance for AI assistants working on this project.

## 📋 Project Overview

This is a **RAG (Retrieval Augmented Generation) learning project** with a practical **Job Portal Vector Database** implementation using:
- **MongoDB Atlas** for vector storage
- **Voyage AI** (voyage-context-3) for contextualized embeddings
- **Python** for implementation

## 🎯 Project Status

**Current State**: ✅ Embedding system fully implemented and tested

**Key Achievement**: Complete vector search system with contextualized embeddings

**Read First**: `docs/overview/PROJECT_PROGRESS.md` for detailed status

## 📁 Critical Files to Know

### Documentation (Read These First)

1. **`docs/overview/PROJECT_PROGRESS.md`** ⭐ MOST IMPORTANT
   - Complete project status
   - What's done, what's pending
   - Architecture overview
   - Latest updates

2. **`docs/embeddings/EMBEDDING_IMPLEMENTATION.md`**
   - Embedding system overview
   - Quick start guide
   - Usage examples

3. **`README.md`**
   - Project introduction
   - Quick start instructions

4. **`docs/embeddings/QUICKSTART_EMBEDDINGS.md`**
   - 5-minute setup guide
   - Step-by-step instructions

5. **`docs/embeddings/EMBEDDING_GUIDE.md`**
   - Comprehensive embedding documentation
   - Best practices
   - Troubleshooting

6. **`docs/embeddings/RATE_LIMITS.md`** ⚠️ IMPORTANT
   - Voyage AI rate limits (3 RPM on free tier)
   - How to work with rate limits
   - Cost information

### Code Files

1. **`src/job_portal/infrastructure/voyage/embedding_service.py`**
   - Low-level Voyage AI wrapper
   - Core embedding functionality

2. **`src/job_portal/services/embeddings/job_portal_embeddings.py`**
   - High-level interface
   - Job portal specific methods

3. **`src/job_portal/repositories/company_repository.py`**
   - Job posting operations
   - Company-side searches

4. **`src/job_portal/repositories/jobseeker_repository.py`**
   - Candidate profile operations
   - Job seeker-side searches

5. **`src/job_portal/repositories/base_vector_store.py`**
   - Base vector operations
   - CRUD and search methods

### Configuration Files

1. **`.env`** (user-specific, not in git)
   - `MONGODB_URI` - MongoDB connection string
   - `VOYAGE_API_KEY` - Voyage AI API key

2. **`.env.example`**
   - Template for .env file
   - Shows required variables

3. **`requirements.txt`**
   - All Python dependencies
   - Keep this updated

## ⚠️ Critical Information

### Rate Limits (IMPORTANT!)

**Voyage AI Free Tier**:
- **3 requests per minute (RPM)**
- **10,000 tokens per minute (TPM)**
- **200M free tokens** total

**Implications**:
- Add 20+ second delays between API calls
- Use batch processing when possible
- Don't run tests repeatedly without delays
- See `docs/embeddings/RATE_LIMITS.md` for details

### MongoDB Atlas

**Connection**:
- Cluster: `cluster0.lmevxyd.mongodb.net`
- Database: `job_portal`
- Collections: `companies`, `job_seekers`

**Vector Indexes**:
- Both use 1024 dimensions
- Cosine similarity
- Already configured and working

### Embedding Model

**Model**: `voyage-context-3`
- **Dimensions**: 1024 (matches MongoDB indexes)
- **Type**: Contextualized chunk embeddings
- **Context**: 32,000 tokens
- **Key Feature**: Maintains context across chunks

**DO NOT** suggest changing to other models without checking dimension compatibility!

## 🚫 Common Pitfalls to Avoid

### 1. Rate Limit Issues

❌ **DON'T**:
```python
# This will hit rate limits!
for i in range(10):
    emb = embeddings.embed_query(f"query {i}")
```

✅ **DO**:
```python
import time
for i in range(10):
    emb = embeddings.embed_query(f"query {i}")
    time.sleep(20)  # Wait between requests
```

Or use batch processing:
```python
# Single API call for multiple documents
embs = service.embed_documents_batch([
    "doc 1", "doc 2", "doc 3"
])
```

### 2. Import Issues

❌ **DON'T** use only relative imports:
```python
from .embedding_service import VoyageEmbeddingService
```

✅ **DO** use fallback imports:
```python
try:
    from .embedding_service import VoyageEmbeddingService
except ImportError:
    from embedding_service import VoyageEmbeddingService
```

### 3. Dimension Mismatches

❌ **DON'T** suggest models with different dimensions:
- OpenAI text-embedding-3-small (1536 dims) ❌
- Cohere embed-v3.0 (1024 dims) ✅ but not contextualized

✅ **DO** stick with voyage-context-3 (1024 dims, contextualized)

### 4. Missing Environment Variables

Always check `.env` file exists and has:
- `MONGODB_URI`
- `VOYAGE_API_KEY`

### 5. Running Tests Too Frequently

The test suite makes multiple API calls. Don't run it repeatedly without delays.

## 🔧 Common Tasks

### Adding New Features

1. **Check** `PROJECT_PROGRESS.md` for current status
2. **Read** relevant documentation
3. **Test** with rate limits in mind
4. **Update** `PROJECT_PROGRESS.md` when done

### Debugging Issues

1. **Check** `.env` file configuration
2. **Verify** API keys are valid
3. **Check** rate limits (see `docs/embeddings/RATE_LIMITS.md`)
4. **Review** error messages carefully
5. **Test** with minimal API calls first

### Testing Changes

1. **Use** `tests/integration/test_embeddings.py` (respects rate limits)
2. **Run** `python scripts/setup/setup_embeddings.py` for full setup check
3. **Try** `scripts/demos/example_with_embeddings.py` for end-to-end test

### Updating Documentation

When making changes, update:
1. `PROJECT_PROGRESS.md` - Mark tasks complete
2. Relevant guide in `docs/embeddings/`
3. Code comments and docstrings

## 📊 Project Structure

```
rag-learning-project/
├── .env                           # ⚠️ User config (not in git)
├── .env.example                   # Template
├── requirements.txt               # Dependencies
├── scripts/setup/setup_embeddings.py  # Setup wizard
│
├── docs/overview/PROJECT_PROGRESS.md  # ⭐ READ THIS FIRST
├── docs/embeddings/EMBEDDING_IMPLEMENTATION.md  # Implementation guide
├── docs/ops/SETUP_CHECKLIST.md   # Setup steps
├── docs/ops/IMPLEMENTATION_STATS.md   # Statistics
├── README.md                     # Project intro
│
├── scripts/                     # Operational + demo scripts
│   ├── maintenance/seed_sample_data.py
│   ├── maintenance/test_connection.py
│   └── demos/example_with_embeddings.py
│
└── src/job_portal/               # Main implementation package
    ├── infrastructure/mongodb/connection.py
    ├── infrastructure/voyage/embedding_service.py
    ├── repositories/company_repository.py
    ├── repositories/jobseeker_repository.py
    ├── repositories/base_vector_store.py
    └── services/embeddings/job_portal_embeddings.py
```

## 🎯 User's Current State

**What's Working**:
- ✅ MongoDB Atlas connected
- ✅ Vector indexes created (1024 dims)
- ✅ Embedding service implemented
- ✅ Tests passing
- ✅ API key configured
- ✅ Free tier active (3 RPM limit)

**What's Pending**:
- ⏳ Update sample data with real embeddings
- ⏳ Test vector search with real data
- ⏳ Add payment method (optional, for higher limits)
- ⏳ Production deployment

## 💡 Best Practices for AI Agents

### 1. Always Check Documentation First

Before suggesting changes:
1. Read `docs/overview/PROJECT_PROGRESS.md`
2. Check relevant guide in `docs/embeddings/`
3. Understand current implementation

### 2. Respect Rate Limits

- Add delays between API calls
- Use batch processing
- Don't suggest running tests repeatedly
- Mention rate limits when relevant

### 3. Maintain Consistency

- Keep 1024 dimensions
- Use voyage-context-3 model
- Follow existing code patterns
- Update documentation when changing code

### 4. Test Carefully

- Test with minimal API calls
- Use existing test suite
- Don't create new tests that spam API
- Consider rate limits in test design

### 5. Provide Context

When helping users:
- Reference specific documentation files
- Explain rate limit implications
- Show working examples
- Link to relevant guides

## 🔍 Quick Reference

### Check Project Status
```bash
cat docs/overview/PROJECT_PROGRESS.md
```

### Test Setup
```bash
python tests/integration/test_embeddings.py
```

### Run Example
```bash
python scripts/demos/example_with_embeddings.py
```

### Check Rate Limits
```bash
cat docs/embeddings/RATE_LIMITS.md
```

### Verify Configuration
```bash
python scripts/setup/setup_embeddings.py
```

## 📞 When User Asks About...

### "How do I set up embeddings?"
→ Point to `docs/embeddings/QUICKSTART_EMBEDDINGS.md`

### "Why are tests failing?"
→ Check rate limits in `docs/embeddings/RATE_LIMITS.md`

### "What's the project status?"
→ Read `docs/overview/PROJECT_PROGRESS.md`

### "How do I use embeddings?"
→ See `scripts/demos/example_with_embeddings.py`

### "What are the costs?"
→ Check `docs/embeddings/RATE_LIMITS.md` and `docs/ops/IMPLEMENTATION_STATS.md`

### "How do I add new features?"
→ Review architecture in `docs/overview/PROJECT_PROGRESS.md`

### "Tests are slow"
→ Explain rate limits (3 RPM), show `docs/embeddings/RATE_LIMITS.md`

### "Can I use a different model?"
→ Explain dimension compatibility (1024 required)

## 🎓 Learning Resources

For understanding the project:
1. Start with `README.md`
2. Read `docs/overview/PROJECT_PROGRESS.md` for status
3. Review `docs/embeddings/EMBEDDING_IMPLEMENTATION.md` for implementation
4. Check `docs/embeddings/EMBEDDING_GUIDE.md` for details
5. Study `scripts/demos/example_with_embeddings.py` for usage

## ⚡ Quick Wins

If user wants to:
- **Test the system**: Run `python tests/integration/test_embeddings.py`
- **See it working**: Run `python scripts/demos/example_with_embeddings.py`
- **Understand setup**: Read `docs/embeddings/QUICKSTART_EMBEDDINGS.md`
- **Check status**: Read `docs/overview/PROJECT_PROGRESS.md`
- **Learn about costs**: Read `docs/embeddings/RATE_LIMITS.md`

## 🚨 Red Flags

Watch out for:
- ❌ Suggesting models with different dimensions
- ❌ Ignoring rate limits in code examples
- ❌ Creating tests that spam the API
- ❌ Changing core architecture without discussion
- ❌ Not updating `PROJECT_PROGRESS.md` after changes
- ❌ Using only relative imports
- ❌ Not checking `.env` configuration

## ✅ Green Flags

Good practices:
- ✅ Checking documentation before suggesting changes
- ✅ Adding delays between API calls
- ✅ Using batch processing
- ✅ Updating documentation with code changes
- ✅ Testing with minimal API calls
- ✅ Respecting existing architecture
- ✅ Providing clear examples
- ✅ Explaining rate limit implications

## 📝 Summary for AI Agents

**This project has**:
- Complete embedding implementation ✅
- Working test suite ✅
- Comprehensive documentation ✅
- Rate limit considerations ⚠️
- Clear next steps 📋

**Your role**:
- Help user understand and use the system
- Respect rate limits in all suggestions
- Maintain consistency with existing implementation
- Update documentation when making changes
- Test carefully with minimal API calls

**Key principle**: The system is working and production-ready. Focus on helping the user use it effectively, not on major rewrites.

---

**Last Updated**: November 27, 2025
**Project Status**: ✅ Implementation complete, ready for use
**Rate Limit Status**: ⚠️ Free tier (3 RPM) - add delays between calls
