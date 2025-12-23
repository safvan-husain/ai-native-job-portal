# RAG Learning Project

The RAG learning workspace now follows a docs-first, src-layout structure:

```
rag-learning-project/
├── docs/
│   ├── overview/           # Project status, learning roadmap
│   ├── embeddings/         # Embedding-specific guides and rate limits
│   └── ops/                # Setup checklist, implementation stats
├── scripts/
│   ├── setup/              # Environment and index setup helpers
│   ├── maintenance/        # Connection checks, data seeding
│   └── demos/              # Example flows using the vector database
├── src/job_portal/         # Installable package for the vector DB
└── tests/                  # Unit / integration test suites
```

Head over to `docs/overview/README.md` for the full primer, learning path, and
links to every embedding guide. Common entrypoints:

- `python scripts/setup/setup_embeddings.py` – guided setup for Voyage AI + MongoDB
- `python scripts/maintenance/test_connection.py` – validates Atlas connectivity
- `python scripts/demos/example_with_embeddings.py` – runs the end-to-end demo
- `python tests/integration/test_embeddings.py` – rate-limited Voyage AI tests

All embedding documentation (quick start, implementation guide, rate limits) now
lives in `docs/embeddings/`. Operational notes (project progress, stats, setup
checklist) are under `docs/overview/` and `docs/ops/`.
