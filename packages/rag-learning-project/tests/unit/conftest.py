"""Shared fixtures for unit tests."""
import pytest
from unittest.mock import Mock


@pytest.fixture
def mock_mongodb_collection():
    """Create a mock MongoDB collection."""
    return Mock()


@pytest.fixture
def mock_voyage_client():
    """Create a mock Voyage AI client."""
    mock_client = Mock()
    mock_result = Mock()
    mock_result.results = [Mock(embeddings=[[0.1, 0.2, 0.3]])]
    mock_client.contextualized_embed.return_value = mock_result
    return mock_client


@pytest.fixture
def sample_embedding():
    """Sample embedding vector."""
    return [0.1] * 1024


@pytest.fixture
def sample_job_posting():
    """Sample job posting document."""
    return {
        "company_id": "comp1",
        "company_name": "TechCorp",
        "job_title": "Software Engineer",
        "job_description": "Build great software",
        "requirements_embedding": [0.1] * 1024,
        "company_size": "51-200",
        "location": "San Francisco",
        "industry": "Technology",
        "remote_policy": "hybrid",
        "required_skills": ["Python", "JavaScript"],
        "experience_level": "mid",
        "status": "active"
    }


@pytest.fixture
def sample_candidate_profile():
    """Sample candidate profile document."""
    return {
        "user_id": "user1",
        "name": "John Doe",
        "profile_summary": "Experienced software engineer",
        "profile_embedding": [0.1] * 1024,
        "years_of_experience": 5.0,
        "skills": ["Python", "JavaScript", "React"],
        "desired_location": "San Francisco",
        "desired_remote_policy": "hybrid",
        "education_level": "bachelors",
        "current_title": "Software Engineer",
        "status": "active"
    }
