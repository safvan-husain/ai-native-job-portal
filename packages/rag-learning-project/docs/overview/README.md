# RAG Learning Project

A project to learn Retrieval Augmented Generation (RAG) with a practical **Job Portal Vector Database** implementation using MongoDB Atlas and Voyage AI embeddings.

## 🎉 Latest: Voyage AI Embeddings Implemented!

The job portal now has a complete embedding system using **Voyage AI's contextualized embeddings**. See [`docs/embeddings/EMBEDDING_IMPLEMENTATION.md`](../embeddings/EMBEDDING_IMPLEMENTATION.md) for details.

## What is RAG?

RAG enhances LLM responses by:
1. **Retrieving** relevant documents from a knowledge base
2. **Augmenting** the LLM prompt with retrieved context
3. **Generating** responses based on both the query and retrieved information

## Project Structure

```
rag-learning-project/
├── docs/
│   ├── overview/                 # README, PROJECT_PROGRESS, learning path
│   ├── embeddings/               # Guides, quick start, rate limits
│   └── ops/                      # Setup checklist, implementation stats
├── scripts/
│   ├── setup/                    # Environment + index setup helpers
│   ├── maintenance/              # Connection + data seeding scripts
│   └── demos/                    # Example flows with embeddings
├── src/
│   └── job_portal/               # Installable package for vector DB logic
│       ├── infrastructure/       # MongoDB + Voyage adapters
│       ├── repositories/         # Company + job seeker stores
│       ├── services/             # Embedding + matching services
│       └── workflows/            # Future orchestration layers
├── tests/                        # Unit / integration / e2e suites
├── data/                         # Sample KB docs
├── notebooks/                    # Learning notebooks
└── requirements.txt              # Python dependencies
```

## Learning Path

1. **Document Processing**: Learn to load and chunk documents
2. **Embeddings**: Convert text to vector representations
3. **Vector Database**: Store and search embeddings
4. **Retrieval**: Find relevant documents based on queries
5. **Generation**: Use LLM with retrieved context
6. **Evaluation**: Measure RAG system performance

## Technologies

### Job Portal Implementation
- **Embeddings**: Voyage AI (voyage-context-3) - Contextualized embeddings
- **Vector DB**: MongoDB Atlas Vector Search
- **Dimensions**: 1024 (cosine similarity)
- **Features**: Hybrid search, metadata filtering, context-aware chunking

### General RAG Stack
- **Embeddings**: Sentence Transformers, OpenAI Embeddings
- **Vector DB**: ChromaDB, FAISS, Pinecone
- **LLMs**: OpenAI GPT, Anthropic Claude, Local models (Ollama)
- **Frameworks**: LangChain, LlamaIndex

## Getting Started

### Quick Start (Job Portal with Embeddings)

```bash
# 1. Run setup wizard
python scripts/setup/setup_embeddings.py

# 2. Configure API keys in .env
# VOYAGE_API_KEY=your_key_here
# MONGODB_URI=your_connection_string

# 3. Test embeddings (respects rate limits)
python tests/integration/test_embeddings.py

# 4. Run example
python scripts/demos/example_with_embeddings.py
```

See [`docs/embeddings/EMBEDDING_IMPLEMENTATION.md`](../embeddings/EMBEDDING_IMPLEMENTATION.md) for the complete guide.

### General RAG Learning

1. Create a virtual environment
2. Install dependencies: `pip install -r requirements.txt`
3. Explore the notebooks in order
4. Run example scripts in `src/`

## Resources

- [RAG Paper](https://arxiv.org/abs/2005.11401)
- [LangChain RAG Tutorial](https://python.langchain.com/docs/use_cases/question_answering/)
- [Pinecone RAG Guide](https://www.pinecone.io/learn/retrieval-augmented-generation/)
