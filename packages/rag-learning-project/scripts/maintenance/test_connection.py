"""Test MongoDB connection and basic operations."""
from pathlib import Path
import sys

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from job_portal import MongoDBConnection

# Load environment variables
load_dotenv()


def test_connection():
    """Test basic MongoDB connection."""
    print("Testing MongoDB connection...")
    
    try:
        with MongoDBConnection(database_name="job_portal") as conn:
            db = conn.get_database()
            
            # List collections
            collections = db.list_collection_names()
            print(f"✓ Connected successfully!")
            print(f"✓ Database: {db.name}")
            print(f"✓ Collections: {collections}")
            
            # Test inserting a sample document
            test_collection = db["test_collection"]
            result = test_collection.insert_one({"test": "data", "status": "active"})
            print(f"✓ Test insert successful: {result.inserted_id}")
            
            # Clean up test
            test_collection.delete_one({"_id": result.inserted_id})
            print(f"✓ Test cleanup successful")
            
            return True
            
    except Exception as e:
        print(f"✗ Connection failed: {e}")
        return False


def check_collections():
    """Check if required collections exist."""
    print("\nChecking collections...")
    
    try:
        with MongoDBConnection(database_name="job_portal") as conn:
            db = conn.get_database()
            collections = db.list_collection_names()
            
            required = ["companies", "job_seekers"]
            for coll in required:
                if coll in collections:
                    count = db[coll].count_documents({})
                    print(f"✓ {coll}: {count} documents")
                else:
                    print(f"✗ {coll}: NOT FOUND (will be created on first insert)")
            
            return True
            
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def check_indexes():
    """Check if vector search indexes exist."""
    print("\nChecking vector search indexes...")
    
    try:
        with MongoDBConnection(database_name="job_portal") as conn:
            db = conn.get_database()
            
            # Check job_seekers indexes
            js_indexes = list(db["job_seekers"].list_indexes())
            print(f"job_seekers indexes: {len(js_indexes)}")
            for idx in js_indexes:
                print(f"  - {idx.get('name', 'unnamed')}")
            
            # Check companies indexes
            comp_indexes = list(db["companies"].list_indexes())
            print(f"companies indexes: {len(comp_indexes)}")
            for idx in comp_indexes:
                print(f"  - {idx.get('name', 'unnamed')}")
            
            # Note about vector search indexes
            print("\nNote: Vector search indexes don't appear in list_indexes().")
            print("They must be created in MongoDB Atlas UI under the 'Search' tab.")
            
            return True
            
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("MongoDB Connection Test")
    print("=" * 60)
    
    if test_connection():
        check_collections()
        check_indexes()
        
        print("\n" + "=" * 60)
        print("Next steps:")
        print("1. Run: python scripts/setup/setup_indexes.py")
        print("2. Create vector search indexes in MongoDB Atlas UI")
        print("3. Run: python scripts/demos/example_usage.py")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("Please check your MONGODB_URI in .env file")
        print("=" * 60)
