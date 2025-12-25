import os
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from dotenv import load_dotenv
from models import Candidate

load_dotenv()

async def init_db():
    # Get MongoDB URI from environment
    mongodb_uri = os.getenv("MONGODB_URI")
    if not mongodb_uri:
        raise ValueError("MONGODB_URI not found in .env file")

    # Create Motor client
    client = AsyncIOMotorClient(mongodb_uri)
    
    # Extract DB name from URI or use a default
    # The URI in .env is: mongodb+srv://...cluster0.lmevxyd.mongodb.net/?...
    # We'll use 'job_portal' as the database name
    db_name = "job_portal"
    
    # Initialize beanie with the Candidate document class
    await init_beanie(database=client[db_name], document_models=[Candidate])
    print(f"Connected to MongoDB: {db_name}")
