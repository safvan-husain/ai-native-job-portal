from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from contextlib import asynccontextmanager
from database import init_db, get_unique_keywords
from agent.graph import CandidateFilterAgent

# Define models
class QueryRequest(BaseModel):
    query: str

# Create a singleton for the agent
agent = CandidateFilterAgent()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize DB connection on startup
    await init_db()
    yield

app = FastAPI(
    title="FastAPI AI Backend",
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/")
def root():
    return {"message": "AI-Native Job Portal Backend is running 🚀"}

@app.post("/candidates/ai-filter")
async def ai_filter_candidates(request: QueryRequest):
    """
    Filter candidates using a natural language query.
    The AI maps the query to existing keywords in the database.
    """
    try:
        print(f"DEBUG: Endpoint called with query: {request.query}")
        # Fetch current vocabulary from the DB
        unique_keywords = await get_unique_keywords()
        print(f"DEBUG: Keywords from DB: {unique_keywords}")
        with open("keywords.log", "w") as f:
            f.write(str(unique_keywords))
        
        # Run the agent
        response = await agent.run(request.query, unique_keywords)
        print(f"DEBUG: Agent response: {response}")
        
        return {"response": response}
    except Exception as e:
        import traceback
        with open("error.trace", "w") as f:
            traceback.print_exc(file=f)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    return {"status": "ok"}
