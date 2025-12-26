import asyncio
from database import init_db
from models import Candidate

async def check():
    await init_db()
    count = await Candidate.count()
    print(f"Candidate Count: {count}")
    
    # Try Beanie's distinct
    try:
        keywords = await Candidate.distinct("keywords")
        print(f"Distinct Keywords (Beanie): {keywords}")
    except Exception as e:
        print(f"Beanie Distinct Error: {e}")
        
    # Check one document
    doc = await Candidate.find_one()
    if doc:
        print(f"Sample Candidate: {doc.name}, Keywords: {doc.keywords}")
    else:
        print("No candidates found in DB.")

if __name__ == "__main__":
    asyncio.run(check())
