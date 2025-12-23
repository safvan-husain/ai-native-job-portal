"""Integration tests for bidirectional matching between job seekers and companies."""
import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from job_portal import MongoDBConnection, CompanyStore, JobSeekerStore


class TestBidirectionalMatching(unittest.TestCase):
    """Test bidirectional matching functionality."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures."""
        cls.conn = MongoDBConnection(database_name="job_portal")
        cls.conn.__enter__()
        cls.company_store = CompanyStore(cls.conn.get_collection("companies"))
        cls.jobseeker_store = JobSeekerStore(cls.conn.get_collection("job_seekers"))
    
    @classmethod
    def tearDownClass(cls):
        """Clean up."""
        cls.conn.__exit__(None, None, None)
    
    def test_job_seekers_can_find_companies(self):
        """Test that job seekers can find matching companies."""
        # Get a job seeker
        seeker = self.conn.get_collection("job_seekers").find_one({"name": "Alice Johnson"})
        self.assertIsNotNone(seeker, "Alice Johnson profile should exist")
        
        # Search for matching jobs
        matches = self.company_store.search_matching_candidates(
            candidate_profile_embedding=seeker['profile_embedding'],
            limit=5
        )
        
        # Assertions
        self.assertIsInstance(matches, list, "Should return a list")
        self.assertGreater(len(matches), 0, "Should find at least one match")
        
        # Check match structure
        first_match = matches[0]
        self.assertIn('company_name', first_match)
        self.assertIn('job_title', first_match)
        self.assertIn('score', first_match)
        self.assertGreater(first_match['score'], 0, "Score should be positive")
    
    def test_companies_can_find_candidates(self):
        """Test that companies can find matching candidates."""
        # Get a company
        company = self.conn.get_collection("companies").find_one({"company_name": "TechCorp"})
        self.assertIsNotNone(company, "TechCorp should exist")
        
        # Search for matching candidates
        matches = self.jobseeker_store.search_matching_jobs(
            job_requirements_embedding=company['requirements_embedding'],
            limit=5
        )
        
        # Assertions
        self.assertIsInstance(matches, list, "Should return a list")
        self.assertGreater(len(matches), 0, "Should find at least one match")
        
        # Check match structure
        first_match = matches[0]
        self.assertIn('name', first_match)
        self.assertIn('current_title', first_match)
        self.assertIn('score', first_match)
        self.assertGreater(first_match['score'], 0, "Score should be positive")
    
    def test_alice_matches_techcorp(self):
        """Test that Alice Johnson matches well with TechCorp."""
        # Alice: Senior Python dev, wants work-life balance, equity, hybrid in SF
        # TechCorp: Senior Python role, emphasizes work-life balance, equity, hybrid in SF
        
        seeker = self.conn.get_collection("job_seekers").find_one({"name": "Alice Johnson"})
        self.assertIsNotNone(seeker)
        
        matches = self.company_store.search_matching_candidates(
            candidate_profile_embedding=seeker['profile_embedding'],
            limit=5
        )
        
        company_names = [m['company_name'] for m in matches]
        self.assertIn('TechCorp', company_names, 
                     "Alice should match with TechCorp based on culture and requirements")
    
    def test_bob_matches_dataco(self):
        """Test that Bob Smith matches well with DataCo."""
        # Bob: ML engineer, wants remote, profitable company
        # DataCo: ML role, fully remote, bootstrapped and profitable
        
        seeker = self.conn.get_collection("job_seekers").find_one({"name": "Bob Smith"})
        self.assertIsNotNone(seeker)
        
        matches = self.company_store.search_matching_candidates(
            candidate_profile_embedding=seeker['profile_embedding'],
            limit=5
        )
        
        company_names = [m['company_name'] for m in matches]
        self.assertIn('DataCo', company_names,
                     "Bob should match with DataCo based on ML focus and remote preference")
    
    def test_carol_matches_startupxyz(self):
        """Test that Carol Davis matches well with StartupXYZ."""
        # Carol: Full stack, wants early-stage startup, equity, hybrid in Austin
        # StartupXYZ: Pre-seed startup, generous equity, hybrid in Austin
        
        seeker = self.conn.get_collection("job_seekers").find_one({"name": "Carol Davis"})
        self.assertIsNotNone(seeker)
        
        matches = self.company_store.search_matching_candidates(
            candidate_profile_embedding=seeker['profile_embedding'],
            limit=5
        )
        
        company_names = [m['company_name'] for m in matches]
        self.assertIn('StartupXYZ', company_names,
                     "Carol should match with StartupXYZ based on startup culture and location")
    
    def test_david_matches_financeai(self):
        """Test that David Chen matches well with FinanceAI."""
        # David: Senior backend, wants mature company, work-life balance, remote
        # FinanceAI: Series D, emphasizes work-life balance, remote, backend role
        
        seeker = self.conn.get_collection("job_seekers").find_one({"name": "David Chen"})
        self.assertIsNotNone(seeker)
        
        matches = self.company_store.search_matching_candidates(
            candidate_profile_embedding=seeker['profile_embedding'],
            limit=5
        )
        
        company_names = [m['company_name'] for m in matches]
        self.assertIn('FinanceAI', company_names,
                     "David should match with FinanceAI based on maturity and work-life balance")
    
    def test_match_scores_are_reasonable(self):
        """Test that match scores are in reasonable range."""
        seeker = self.conn.get_collection("job_seekers").find_one()
        self.assertIsNotNone(seeker)
        
        matches = self.company_store.search_matching_candidates(
            candidate_profile_embedding=seeker['profile_embedding'],
            limit=5
        )
        
        for match in matches:
            score = match.get('score', 0)
            self.assertGreater(score, 0, "Score should be positive")
            self.assertLess(score, 1.1, "Score should be <= 1.0 (with small margin for floating point)")
    
    def test_filtering_by_location(self):
        """Test that location filtering works."""
        seeker = self.conn.get_collection("job_seekers").find_one({"name": "Alice Johnson"})
        self.assertIsNotNone(seeker)
        
        # Search with location filter
        matches = self.company_store.search_matching_candidates(
            candidate_profile_embedding=seeker['profile_embedding'],
            location="San Francisco",
            limit=5
        )
        
        # All matches should be in San Francisco
        for match in matches:
            self.assertIn("San Francisco", match['location'],
                         "Filtered results should match location")
    
    def test_filtering_by_remote_policy(self):
        """Test that remote policy filtering works."""
        seeker = self.conn.get_collection("job_seekers").find_one({"name": "Bob Smith"})
        self.assertIsNotNone(seeker)
        
        # Search with remote filter
        matches = self.company_store.search_matching_candidates(
            candidate_profile_embedding=seeker['profile_embedding'],
            remote_policy="remote",
            limit=5
        )
        
        # All matches should be remote
        for match in matches:
            self.assertEqual(match['remote_policy'], "remote",
                           "Filtered results should match remote policy")
    
    def test_filtering_by_experience_level(self):
        """Test that experience level filtering works."""
        company = self.conn.get_collection("companies").find_one({"experience_level": "senior"})
        self.assertIsNotNone(company)
        
        # Search with experience filter
        matches = self.jobseeker_store.search_matching_jobs(
            job_requirements_embedding=company['requirements_embedding'],
            min_experience=5.0,
            limit=5
        )
        
        # All matches should have sufficient experience
        for match in matches:
            self.assertGreaterEqual(match['years_of_experience'], 5.0,
                                   "Filtered results should meet experience requirement")
    
    def test_all_seekers_have_embeddings(self):
        """Test that all job seekers have valid embeddings."""
        seekers = list(self.conn.get_collection("job_seekers").find({}))
        
        for seeker in seekers:
            self.assertIn('profile_embedding', seeker,
                         f"{seeker['name']} should have profile_embedding")
            self.assertIsInstance(seeker['profile_embedding'], list,
                                "Embedding should be a list")
            self.assertEqual(len(seeker['profile_embedding']), 1024,
                           "Embedding should have 1024 dimensions")
    
    def test_all_companies_have_embeddings(self):
        """Test that all companies have valid embeddings."""
        companies = list(self.conn.get_collection("companies").find({}))
        
        for company in companies:
            self.assertIn('requirements_embedding', company,
                         f"{company['company_name']} should have requirements_embedding")
            self.assertIsInstance(company['requirements_embedding'], list,
                                "Embedding should be a list")
            self.assertEqual(len(company['requirements_embedding']), 1024,
                           "Embedding should have 1024 dimensions")


if __name__ == '__main__':
    unittest.main(verbosity=2)
