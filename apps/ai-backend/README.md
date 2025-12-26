# AI-Native Job Portal - AI Backend

This is the AI-powered backend for the Job Portal, built with **FastAPI**, **MongoDB (Beanie)**, and **LangGraph**. It features a natural language candidate filtering system that maps user queries to specific skills and keywords.

## 🚀 Features

- **AI Candidate Filtering**: Filter candidates using natural language (e.g., "Find me a Python developer who knows AI").
- **LangGraph Orchestration**: Uses a stateful graph to manage AI agent logic and tool calls.
- **MongoDB Integration**: Asynchronous database operations using Beanie ODM and Motor.
- **Ollama LLM**: Powered by local LLMs via Ollama (default: `llama3.1:8b`).

---

## 🛠️ Prerequisites

1.  **Python 3.10+**
2.  **MongoDB**: A running MongoDB instance (local or Atlas).
3.  **Ollama**: Install [Ollama](https://ollama.com/) and pull the required model:
    ```bash
    ollama pull llama3.1:8b
    ```

---

## ⚙️ Setup & Installation

### 1. Project Setup

Navigate to the backend directory and create a virtual environment:

```powershell
cd apps/ai-backend
python -m venv venv
.\venv\Scripts\Activate
pip install -r requirements.txt
```

### 2. Environment Variables

Create a `.env` file in `apps/ai-backend/` with the following content:

```env
MONGODB_URI=your_mongodb_connection_string
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b
```

---

## 🏃 Running the Application

### 1. Seed the Database
Before running the server, populate the database with sample candidate data:

```powershell
python seed.py
```

### 2. Start the FastAPI Server
Run the application using Uvicorn:

```powershell
uvicorn main:app --reload --port 8006
```
The server will be available at `http://127.0.0.1:8006`.

---

## 🧪 Testing

### 1. Test AI Filtering
With the server running, you can test the natural language filtering using the provided test script:

```powershell
python test_ai_filter.py
```
This script sends several natural language queries to the `/candidates/ai-filter` endpoint and prints the AI's response.

### 2. Verify Database
Check if the candidates were correctly seeded and keywords are being indexed:

```powershell
python check_db.py
```

### 3. Test Ollama Connection
Verify that your local Ollama instance is reachable:

```powershell
python test_ollama.py
```

---

## 📡 API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/` | Root health check |
| `GET` | `/health` | Application health status |
| `POST` | `/candidates/ai-filter` | Filter candidates using natural language |

**Example Request:**
```json
{
  "query": "I need a Python developer who knows AI"
}
```

---

## 🏗️ Project Structure

- `main.py`: Entry point for the FastAPI application.
- `database.py`: MongoDB connection and Beanie initialization.
- `models.py`: BSON/Pydantic models for candidates.
- `agent/`: LangGraph agent logic (nodes, tools, graphs).
- `seed.py`: Database seeding utility.
- `test_ai_filter.py`: Integration test for AI filtering.
