# RAG Learning Path

> **Current Project**: Job Portal with MongoDB Atlas Vector Search
> **Progress**: See [PROJECT_PROGRESS.md](PROJECT_PROGRESS.md) for detailed status

## Phase 1: Foundations (Week 1)

### Day 1-2: Understanding RAG
- [x] Learn about vector embeddings and semantic search
- [x] Explore use cases: Job matching system
- [ ] Read the original RAG paper
- [ ] Understand the difference between RAG and fine-tuning

### Day 3-4: Embeddings
- [x] Learn how text embeddings work
- [x] Understand embedding dimensions and similarity metrics
- [ ] Experiment with different embedding models
- [ ] Practice: Convert sample texts to embeddings

### Day 5-7: Vector Databases
- [x] Set up MongoDB Atlas with Vector Search
- [x] Learn CRUD operations on vector stores
- [x] Understand similarity search (cosine, euclidean)
- [x] Practice: Store and query document embeddings
- [x] Implement hybrid search (vector + metadata filters)

## Phase 2: Basic RAG (Week 2)

### Day 8-10: Document Processing
- [ ] Load different document types (PDF, DOCX, TXT)
- [ ] Implement text chunking strategies
- [ ] Handle document metadata
- [ ] Practice: Create a document ingestion pipeline

### Day 11-14: Simple RAG System
- [ ] Build a basic retrieval system
- [ ] Integrate with an LLM (start with OpenAI or local model)
- [ ] Implement query → retrieve → generate flow
- [ ] Practice: Build a Q&A system over your documents

## Phase 3: Advanced Techniques (Week 3-4)

### Week 3: Optimization
- [ ] Experiment with different chunking strategies
- [ ] Try multiple embedding models
- [ ] Implement re-ranking
- [ ] Add metadata filtering
- [ ] Optimize retrieval parameters (top-k, similarity threshold)

### Week 4: Production Concepts
- [ ] Add error handling and logging
- [ ] Implement caching strategies
- [ ] Learn about RAG evaluation metrics
- [ ] Explore advanced patterns (HyDE, Multi-query, etc.)
- [ ] Build a simple web interface

## Projects to Build

1. **Personal Document Q&A**: Query your own PDF collection
2. **Code Documentation Assistant**: RAG over a codebase
3. **Research Paper Summarizer**: Analyze academic papers
4. **Company Knowledge Base**: Internal wiki search

## Key Concepts to Master

- Text splitting and chunking
- Embedding generation and storage
- Vector similarity search
- Prompt engineering for RAG
- Context window management
- Evaluation and iteration

## Common Challenges

- **Chunking**: Finding optimal chunk size for your use case
- **Retrieval Quality**: Getting relevant documents consistently
- **Context Length**: Fitting retrieved docs in LLM context window
- **Latency**: Balancing quality with response time
- **Cost**: Managing API costs for embeddings and LLM calls

## Next Steps After RAG

- Multi-modal RAG (text + images)
- Graph RAG
- Agentic RAG (with tools and reasoning)
- Fine-tuning retrieval models
- Building production RAG systems
