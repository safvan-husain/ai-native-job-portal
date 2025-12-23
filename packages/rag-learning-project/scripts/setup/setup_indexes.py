"""
Setup script for creating MongoDB Atlas Vector Search indexes.

Note: Vector search indexes must be created through MongoDB Atlas UI or Atlas CLI.
This script provides the index definitions and instructions.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
INDEX_DEFINITIONS = ROOT / "src" / "job_portal" / "infrastructure" / "mongodb" / "index_definitions.json"


def get_index_definitions():
    """Get vector search index definitions."""
    with open(INDEX_DEFINITIONS, 'r', encoding='utf-8') as f:
        return json.load(f)


def print_setup_instructions():
    """Print instructions for setting up vector search indexes."""
    
    print("=" * 80)
    print("MongoDB Atlas Vector Search Index Setup")
    print("=" * 80)
    print()
    print("IMPORTANT: Vector search indexes must be created in MongoDB Atlas UI.")
    print()
    print("Steps:")
    print("1. Go to: https://cloud.mongodb.com")
    print("2. Navigate to your cluster")
    print("3. Click 'Search' tab")
    print("4. Click 'Create Search Index'")
    print("5. Choose 'JSON Editor'")
    print("6. Use the definitions below:")
    print()
    
    definitions = get_index_definitions()
    
    print("-" * 80)
    print("INDEX 1: Job Seekers Vector Index")
    print("-" * 80)
    print(f"Database: job_portal")
    print(f"Collection: job_seekers")
    print(f"Index Name: {definitions['jobseeker_vector_index']['name']}")
    print()
    print("JSON Definition:")
    print(json.dumps(definitions['jobseeker_vector_index']['definition'], indent=2))
    print()
    
    print("-" * 80)
    print("INDEX 2: Companies Vector Index")
    print("-" * 80)
    print(f"Database: job_portal")
    print(f"Collection: companies")
    print(f"Index Name: {definitions['company_vector_index']['name']}")
    print()
    print("JSON Definition:")
    print(json.dumps(definitions['company_vector_index']['definition'], indent=2))
    print()
    
    print("=" * 80)
    print("After creating indexes, you can use the vector search functionality!")
    print("=" * 80)


if __name__ == "__main__":
    print_setup_instructions()
