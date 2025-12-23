"""Tests for LangChain tools."""
import pytest
from unittest.mock import Mock, patch, MagicMock
from bson import ObjectId

# Import tools
from src.job_portal.agent.tools.job_seeker_tools import (
    search_jobs,
    get_company_details,
    compare_companies
)
from src.job_portal.agent.tools.company_tools import (
    search_candidates,
    get_candidate_details,
    compare_candidates
)


class TestJobSeekerTools:
    """Test job seeker tools."""
    
    @patch('src.job_portal.agent.tools.job_seeker_tools._get_embeddings')
    @patch('src.job_portal.agent.tools.job_seeker_tools._get_company_store')
    def test_search_jobs_success(self, mock_store, mock_embeddings):
        """Test successful job search."""
        # Mock embedding service
        mock_emb_service = Mock()
        mock_emb_service.embed_search_query.return_value = [0.1] * 1024
        mock_embeddings.return_value = mock_emb_service
        
        # Mock company store
        mock_company_store = Mock()
        mock_company_store.vector_search.return_value = [
            {
                '_id': ObjectId(),
                'company_name': 'Tech Corp',
                'job_title': 'Python Developer',
                'location': 'San Francisco, CA',
                'remote_policy': 'hybrid',
                'experience_level': 'mid',
                'score': 0.95
            },
            {
                '_id': ObjectId(),
                'company_name': 'Data Inc',
                'job_title': 'Senior Python Engineer',
                'location': 'New York, NY',
                'remote_policy': 'remote',
                'experience_level': 'senior',
                'score': 0.88
            }
        ]
        mock_store.return_value = mock_company_store
        
        # Execute tool
        result = search_jobs.invoke({"requirements": "Python developer with 5 years experience"})
        
        # Verify
        assert "Found 2 matching job posting(s)" in result
        assert "Tech Corp" in result
        assert "Python Developer" in result
        assert "Data Inc" in result
        assert "95.0%" in result  # Changed from "0.950" to match new format
        
        # Verify calls
        mock_emb_service.embed_search_query.assert_called_once()
        mock_company_store.vector_search.assert_called_once()
    
    @patch('src.job_portal.agent.tools.job_seeker_tools._get_embeddings')
    @patch('src.job_portal.agent.tools.job_seeker_tools._get_company_store')
    def test_search_jobs_no_results(self, mock_store, mock_embeddings):
        """Test job search with no results."""
        # Mock services
        mock_emb_service = Mock()
        mock_emb_service.embed_search_query.return_value = [0.1] * 1024
        mock_embeddings.return_value = mock_emb_service
        
        mock_company_store = Mock()
        mock_company_store.vector_search.return_value = []
        mock_store.return_value = mock_company_store
        
        # Execute tool
        result = search_jobs.invoke({"requirements": "Unicorn developer"})
        
        # Verify
        assert "No matching job postings found" in result
    
    @patch('src.job_portal.agent.tools.job_seeker_tools._get_company_store')
    def test_get_company_details_success(self, mock_store):
        """Test getting company details."""
        company_id = str(ObjectId())
        
        # Mock company store
        mock_company_store = Mock()
        mock_company_store.get_by_id.return_value = {
            '_id': ObjectId(company_id),
            'company_name': 'Tech Corp',
            'job_title': 'Python Developer',
            'company_size': '51-200',
            'industry': 'Technology',
            'location': 'San Francisco, CA',
            'remote_policy': 'hybrid',
            'experience_level': 'mid',
            'salary_range': {'min': 80000, 'max': 120000},
            'required_skills': ['Python', 'Django', 'PostgreSQL'],
            'job_description': 'We are looking for a talented Python developer...'
        }
        mock_store.return_value = mock_company_store
        
        # Execute tool
        result = get_company_details.invoke({"company_id": company_id})
        
        # Verify
        assert "Tech Corp" in result
        assert "Python Developer" in result
        assert "$80,000 - $120,000" in result
        assert "Python, Django, PostgreSQL" in result
        
        # Verify calls
        mock_company_store.get_by_id.assert_called_once_with(company_id)
    
    @patch('src.job_portal.agent.tools.job_seeker_tools._get_company_store')
    def test_get_company_details_not_found(self, mock_store):
        """Test getting company details when not found."""
        company_id = str(ObjectId())
        
        # Mock company store
        mock_company_store = Mock()
        mock_company_store.get_by_id.return_value = None
        mock_store.return_value = mock_company_store
        
        # Execute tool
        result = get_company_details.invoke({"company_id": company_id})
        
        # Verify
        assert "not found" in result
    
    @patch('src.job_portal.agent.tools.job_seeker_tools._get_company_store')
    def test_compare_companies_success(self, mock_store):
        """Test comparing multiple companies."""
        id1 = str(ObjectId())
        id2 = str(ObjectId())
        
        # Mock company store
        mock_company_store = Mock()
        mock_company_store.get_by_id.side_effect = [
            {
                '_id': ObjectId(id1),
                'company_name': 'Tech Corp',
                'job_title': 'Python Developer',
                'location': 'San Francisco, CA',
                'remote_policy': 'hybrid',
                'experience_level': 'mid',
                'company_size': '51-200',
                'industry': 'Technology',
                'salary_range': {'min': 80000, 'max': 120000},
                'required_skills': ['Python', 'Django']
            },
            {
                '_id': ObjectId(id2),
                'company_name': 'Data Inc',
                'job_title': 'Senior Python Engineer',
                'location': 'New York, NY',
                'remote_policy': 'remote',
                'experience_level': 'senior',
                'company_size': '201-500',
                'industry': 'Data Science',
                'salary_range': {'min': 100000, 'max': 150000},
                'required_skills': ['Python', 'ML']
            }
        ]
        mock_store.return_value = mock_company_store
        
        # Execute tool
        result = compare_companies.invoke({"company_ids": f"{id1},{id2}"})
        
        # Verify
        assert "Comparing 2" in result  # Changed to be more flexible with format
        assert "Tech Corp" in result
        assert "Data Inc" in result
        assert "Option 1" in result
        assert "Option 2" in result
    
    @patch('src.job_portal.agent.tools.job_seeker_tools._get_company_store')
    def test_compare_companies_too_few(self, mock_store):
        """Test comparing with too few companies."""
        result = compare_companies.invoke({"company_ids": str(ObjectId())})
        assert "at least 2 company IDs" in result
    
    @patch('src.job_portal.agent.tools.job_seeker_tools._get_company_store')
    def test_compare_companies_too_many(self, mock_store):
        """Test comparing with too many companies."""
        ids = ','.join([str(ObjectId()) for _ in range(6)])
        result = compare_companies.invoke({"company_ids": ids})
        assert "Maximum 5 companies" in result


class TestCompanyTools:
    """Test company tools."""
    
    @patch('src.job_portal.agent.tools.company_tools._get_embeddings')
    @patch('src.job_portal.agent.tools.company_tools._get_jobseeker_store')
    def test_search_candidates_success(self, mock_store, mock_embeddings):
        """Test successful candidate search."""
        # Mock embedding service
        mock_emb_service = Mock()
        mock_emb_service.embed_search_query.return_value = [0.1] * 1024
        mock_embeddings.return_value = mock_emb_service
        
        # Mock jobseeker store
        mock_jobseeker_store = Mock()
        mock_jobseeker_store.vector_search.return_value = [
            {
                '_id': ObjectId(),
                'name': 'John Doe',
                'current_title': 'Python Developer',
                'years_of_experience': 5,
                'desired_location': 'San Francisco, CA',
                'desired_remote_policy': 'hybrid',
                'education_level': 'bachelors',
                'score': 0.92
            },
            {
                '_id': ObjectId(),
                'name': 'Jane Smith',
                'current_title': 'Senior Python Engineer',
                'years_of_experience': 8,
                'desired_location': 'Remote',
                'desired_remote_policy': 'remote',
                'education_level': 'masters',
                'score': 0.89
            }
        ]
        mock_store.return_value = mock_jobseeker_store
        
        # Execute tool
        result = search_candidates.invoke({"job_requirements": "Senior Python developer"})
        
        # Verify
        assert "Found 2 matching candidate(s)" in result
        assert "John Doe" in result
        assert "Jane Smith" in result
        assert "92.0%" in result  # Changed from "0.920" to match new format
        
        # Verify calls
        mock_emb_service.embed_search_query.assert_called_once()
        mock_jobseeker_store.vector_search.assert_called_once()
    
    @patch('src.job_portal.agent.tools.company_tools._get_embeddings')
    @patch('src.job_portal.agent.tools.company_tools._get_jobseeker_store')
    def test_search_candidates_no_results(self, mock_store, mock_embeddings):
        """Test candidate search with no results."""
        # Mock services
        mock_emb_service = Mock()
        mock_emb_service.embed_search_query.return_value = [0.1] * 1024
        mock_embeddings.return_value = mock_emb_service
        
        mock_jobseeker_store = Mock()
        mock_jobseeker_store.vector_search.return_value = []
        mock_store.return_value = mock_jobseeker_store
        
        # Execute tool
        result = search_candidates.invoke({"job_requirements": "Unicorn developer"})
        
        # Verify
        assert "No matching candidates found" in result
    
    @patch('src.job_portal.agent.tools.company_tools._get_jobseeker_store')
    def test_get_candidate_details_success(self, mock_store):
        """Test getting candidate details."""
        candidate_id = str(ObjectId())
        
        # Mock jobseeker store
        mock_jobseeker_store = Mock()
        mock_jobseeker_store.get_by_id.return_value = {
            '_id': ObjectId(candidate_id),
            'name': 'John Doe',
            'current_title': 'Python Developer',
            'years_of_experience': 5,
            'education_level': 'bachelors',
            'desired_location': 'San Francisco, CA',
            'desired_remote_policy': 'hybrid',
            'availability': 'immediately',
            'desired_salary_min': 100000,
            'skills': ['Python', 'Django', 'PostgreSQL', 'Docker'],
            'industries_of_interest': ['Technology', 'FinTech'],
            'profile_summary': 'Experienced Python developer with strong backend skills...'
        }
        mock_store.return_value = mock_jobseeker_store
        
        # Execute tool
        result = get_candidate_details.invoke({"candidate_id": candidate_id})
        
        # Verify
        assert "John Doe" in result
        assert "Python Developer" in result
        assert "$100,000+" in result
        assert "Python, Django, PostgreSQL, Docker" in result
        
        # Verify calls
        mock_jobseeker_store.get_by_id.assert_called_once_with(candidate_id)
    
    @patch('src.job_portal.agent.tools.company_tools._get_jobseeker_store')
    def test_get_candidate_details_not_found(self, mock_store):
        """Test getting candidate details when not found."""
        candidate_id = str(ObjectId())
        
        # Mock jobseeker store
        mock_jobseeker_store = Mock()
        mock_jobseeker_store.get_by_id.return_value = None
        mock_store.return_value = mock_jobseeker_store
        
        # Execute tool
        result = get_candidate_details.invoke({"candidate_id": candidate_id})
        
        # Verify
        assert "not found" in result
    
    @patch('src.job_portal.agent.tools.company_tools._get_jobseeker_store')
    def test_compare_candidates_success(self, mock_store):
        """Test comparing multiple candidates."""
        id1 = str(ObjectId())
        id2 = str(ObjectId())
        
        # Mock jobseeker store
        mock_jobseeker_store = Mock()
        mock_jobseeker_store.get_by_id.side_effect = [
            {
                '_id': ObjectId(id1),
                'name': 'John Doe',
                'current_title': 'Python Developer',
                'years_of_experience': 5,
                'education_level': 'bachelors',
                'desired_location': 'San Francisco, CA',
                'desired_remote_policy': 'hybrid',
                'availability': 'immediately',
                'desired_salary_min': 100000,
                'skills': ['Python', 'Django']
            },
            {
                '_id': ObjectId(id2),
                'name': 'Jane Smith',
                'current_title': 'Senior Python Engineer',
                'years_of_experience': 8,
                'education_level': 'masters',
                'desired_location': 'Remote',
                'desired_remote_policy': 'remote',
                'availability': '2_weeks',
                'desired_salary_min': 130000,
                'skills': ['Python', 'ML']
            }
        ]
        mock_store.return_value = mock_jobseeker_store
        
        # Execute tool
        result = compare_candidates.invoke({"candidate_ids": f"{id1},{id2}"})
        
        # Verify
        assert "Comparing 2" in result  # Changed to be more flexible with format
        assert "John Doe" in result
        assert "Jane Smith" in result
        assert "Candidate 1" in result
        assert "Candidate 2" in result
    
    @patch('src.job_portal.agent.tools.company_tools._get_jobseeker_store')
    def test_compare_candidates_too_few(self, mock_store):
        """Test comparing with too few candidates."""
        result = compare_candidates.invoke({"candidate_ids": str(ObjectId())})
        assert "at least 2 candidate IDs" in result
    
    @patch('src.job_portal.agent.tools.company_tools._get_jobseeker_store')
    def test_compare_candidates_too_many(self, mock_store):
        """Test comparing with too many candidates."""
        ids = ','.join([str(ObjectId()) for _ in range(6)])
        result = compare_candidates.invoke({"candidate_ids": ids})
        assert "Maximum 5 candidates" in result


class TestToolSchemas:
    """Test that tools have proper LangChain schemas."""
    
    def test_search_jobs_schema(self):
        """Test search_jobs tool has proper schema."""
        assert hasattr(search_jobs, 'name')
        assert hasattr(search_jobs, 'description')
        assert search_jobs.name == 'search_jobs'
        assert 'requirements' in search_jobs.description.lower()
    
    def test_get_company_details_schema(self):
        """Test get_company_details tool has proper schema."""
        assert hasattr(get_company_details, 'name')
        assert hasattr(get_company_details, 'description')
        assert get_company_details.name == 'get_company_details'
    
    def test_compare_companies_schema(self):
        """Test compare_companies tool has proper schema."""
        assert hasattr(compare_companies, 'name')
        assert hasattr(compare_companies, 'description')
        assert compare_companies.name == 'compare_companies'
    
    def test_search_candidates_schema(self):
        """Test search_candidates tool has proper schema."""
        assert hasattr(search_candidates, 'name')
        assert hasattr(search_candidates, 'description')
        assert search_candidates.name == 'search_candidates'
    
    def test_get_candidate_details_schema(self):
        """Test get_candidate_details tool has proper schema."""
        assert hasattr(get_candidate_details, 'name')
        assert hasattr(get_candidate_details, 'description')
        assert get_candidate_details.name == 'get_candidate_details'
    
    def test_compare_candidates_schema(self):
        """Test compare_candidates tool has proper schema."""
        assert hasattr(compare_candidates, 'name')
        assert hasattr(compare_candidates, 'description')
        assert compare_candidates.name == 'compare_candidates'
