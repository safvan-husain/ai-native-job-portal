"""Backward-compatible shim for the new ``job_portal`` package."""

from job_portal import (
    MongoDBConnection,
    VectorStore,
    CompanyStore,
    JobSeekerStore,
    VoyageEmbeddingService,
    JobPortalEmbeddings,
)

__all__ = [
    "MongoDBConnection",
    "VectorStore",
    "CompanyStore",
    "JobSeekerStore",
    "VoyageEmbeddingService",
    "JobPortalEmbeddings",
]
