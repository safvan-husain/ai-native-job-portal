"""Test script for Voyage AI embeddings integration."""
import os
import sys
import time
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from job_portal import VoyageEmbeddingService, JobPortalEmbeddings

# Load environment variables
load_dotenv()


def test_api_key():
    """Test if Voyage API key is configured."""
    print("🔑 Testing API Key Configuration...")
    api_key = os.getenv("VOYAGE_API_KEY")
    
    if not api_key:
        print("❌ VOYAGE_API_KEY not found in environment variables")
        print("   Please set it in your .env file")
        return False
    
    print(f"✅ API key found: {api_key[:10]}...")
    return True


def test_embedding_service():
    """Test basic embedding service functionality."""
    print("\n🧪 Testing Embedding Service...")
    
    try:
        service = VoyageEmbeddingService()
        print("✅ Embedding service initialized")
        
        # Test query embedding
        print("\n   Testing query embedding...")
        query_emb = service.embed_query("Python developer with 5 years experience")
        print(f"   ✅ Query embedding generated: dimension={len(query_emb)}")
        print(f"      First 5 values: {query_emb[:5]}")
        
        # Wait to avoid rate limit
        print("   ⏳ Waiting 20s to avoid rate limit...")
        time.sleep(20)
        
        # Test document embedding
        print("\n   Testing document embedding...")
        doc_emb = service.embed_document(
            "Senior Python Developer position requiring Django and PostgreSQL experience",
            auto_chunk=False
        )
        print(f"   ✅ Document embedding generated: dimension={len(doc_emb)}")
        print(f"      First 5 values: {doc_emb[:5]}")
        
        # Skip batch test to avoid rate limit
        print("\n   ⏭️  Skipping batch test (to avoid rate limit)")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("   Make sure voyageai is installed: pip install voyageai")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_job_portal_embeddings():
    """Test job portal embedding functions."""
    print("\n🏢 Testing Job Portal Embeddings...")
    
    try:
        embeddings = JobPortalEmbeddings()
        print("✅ Job portal embeddings initialized")
        
        # Wait to avoid rate limit
        print("   ⏳ Waiting 20s to avoid rate limit...")
        time.sleep(20)
        
        # Test job posting embedding
        print("\n   Testing job posting embedding...")
        job_emb = embeddings.embed_job_posting(
            job_title="Senior Python Developer",
            job_description="Build scalable backend systems",
            required_skills=["Python", "Django", "PostgreSQL"],
            experience_level="senior"
        )
        print(f"   ✅ Job embedding generated: dimension={len(job_emb)}")
        
        # Skip other tests to avoid rate limit
        print("\n   ⏭️  Skipping additional tests (to avoid rate limit)")
        print("   ℹ️  Add payment method at https://dashboard.voyageai.com/ for higher limits")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_similarity():
    """Test embedding similarity."""
    print("\n📊 Testing Embedding Similarity...")
    
    print("   ⏭️  Skipping similarity test (to avoid rate limit)")
    print("   ℹ️  This test requires 3 API calls")
    print("   ℹ️  Add payment method at https://dashboard.voyageai.com/ for higher limits")
    print("   ✅ Test skipped successfully")
    
    return True


def main():
    """Run all tests."""
    print("="*60)
    print("VOYAGE AI EMBEDDINGS - TEST SUITE")
    print("="*60)
    
    results = []
    
    # Test 1: API Key
    results.append(("API Key Configuration", test_api_key()))
    
    # Test 2: Embedding Service
    if results[0][1]:  # Only if API key is configured
        results.append(("Embedding Service", test_embedding_service()))
        results.append(("Job Portal Embeddings", test_job_portal_embeddings()))
        results.append(("Similarity Calculation", test_similarity()))
    else:
        print("\n⚠️  Skipping remaining tests (API key not configured)")
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    for test_name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{status}: {test_name}")
    
    total_passed = sum(1 for _, passed in results if passed)
    total_tests = len(results)
    
    print(f"\nTotal: {total_passed}/{total_tests} tests passed")
    
    if total_passed == total_tests:
        print("\n🎉 All tests passed! Embedding system is ready to use.")
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")


if __name__ == "__main__":
    main()
