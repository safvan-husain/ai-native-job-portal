from fastapi import FastAPI

app = FastAPI(
    title="FastAPI Backend",
    version="1.0.0"
)

@app.get("/")
def root():
    return {"message": "FastAPI is running 🚀"}

@app.get("/health")
def health_check():
    return {"status": "ok"}
