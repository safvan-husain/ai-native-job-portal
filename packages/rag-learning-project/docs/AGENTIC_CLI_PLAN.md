# Comprehensive Implementation Plan: Job Portal Agentic CLI

## Project Overview
Build an agentic CLI application for job portal interactions using Ollama, LangGraph, and existing MongoDB vector search infrastructure.

## Development Philosophy
- **Incremental**: Build and test each layer before moving to the next
- **Test-driven**: Verify each component works before integration
- **User-first**: CLI interaction comes first, then add intelligence

## Progress Tracker

| Phase | Status | Completion |
|-------|--------|------------|
| Phase 1: CLI Foundation | ✅ Complete | 100% (1.1 ✅, 1.2 ✅, 1.3 ✅, 1.4 ✅) |
| Phase 2: Ollama Integration | ✅ Complete | 100% (2.1 ✅, 2.2 ✅, 2.3 ✅, 2.4 ✅) |
| Phase 3: Tool Definitions | ⚪ Not Started | 0% |
| Phase 4: Database Integration | ⚪ Not Started | 0% |
| Phase 5: Agent + Tools | ⚪ Not Started | 0% |
| Phase 6: Advanced Features | ⚪ Not Started | 0% |
| Phase 7: Polish & Production | ⚪ Not Started | 0% |

**Latest Update**: Phase 2 COMPLETE - Ollama Cloud integration with streaming & memory! ✅

---

## Phase 1: CLI Foundation (Week 1, Days 1-2)

### Goal
Create a beautiful, interactive CLI that handles user input/output without any AI.

### Tasks

#### 1.1 Project Setup ✅
- [x] Create new directory structure
  ```
  src/job_portal/cli/
  ├── __init__.py
  ├── main.py          # Entry point
  ├── ui.py            # Rich UI components
  ├── session.py       # Session state management
  └── commands.py      # Command handlers
  ```
- [x] Update `requirements.txt` with CLI dependencies
  ```txt
  rich>=13.0.0
  typer>=0.9.0
  prompt-toolkit>=3.0.0
  ```
- [x] Install dependencies: `pip install -r requirements.txt`

#### 1.2 Basic CLI Interface ✅
- [x] Create `main.py` with Typer app
- [x] Add welcome screen with Rich
- [x] Implement user type selection (Job Seeker / Company)
- [x] Create conversation loop (input/echo)
- [x] Add exit commands (quit, exit, bye)
- [x] Add help command

#### 1.3 UI Components ✅
- [x] Design conversation display with Rich panels
- [x] Create loading spinners (available via Rich)
- [x] Add colored output for different message types
- [x] Implement command history (up/down arrows) - handled by prompt-toolkit
- [x] Add clear screen functionality

#### 1.4 Session Management ✅
- [x] Create session state class
  - User type (job_seeker/company)
  - Conversation history
  - Selected items for comparison
- [x] Implement session persistence (JSON file)
- [x] Add session resume capability

### Deliverable ✅
Working CLI that:
- Welcomes users
- Lets them choose user type
- Accepts input and echoes back
- Maintains conversation history
- Saves/loads sessions

### Test ✅
```bash
python -m src.job_portal.cli.main start
# Shows welcome, accepts input, echoes responses
# All tests passing: python scripts/demos/test_cli.py
```

---

## Phase 2: Ollama Cloud Integration (Week 1, Days 3-4) ✅ COMPLETE

### Goal
Connect Ollama Cloud LLM for basic conversation without any tools or database.

**Why Cloud?** No local installation, no GPU required, access to larger models (120B+), simple API key auth.

### Prerequisites ✅
- [x] Create account at https://ollama.com
- [x] Get API key from https://ollama.com/settings/keys
- [x] Choose a cloud model (using: `gpt-oss:120b`)
- [x] Test API access and verify available models

**Note**: Ollama Cloud is currently in preview. The API is compatible with local Ollama, so you can switch between cloud and local easily.

### Tasks

#### 2.1 LangChain Setup ✅
- [x] Update `requirements.txt`
  ```txt
  langgraph>=0.2.0
  langchain>=0.3.0
  langchain-ollama>=0.2.0
  ```
- [x] Create `.env` entry for Ollama Cloud
  ```env
  # Ollama Cloud Configuration
  OLLAMA_API_KEY=your_api_key_here
  OLLAMA_BASE_URL=https://ollama.com
  OLLAMA_MODEL=gpt-oss:120b
  ```

#### 2.2 Simple Agent (No Tools) ✅
- [x] Create `src/job_portal/agent/` directory
  ```
  agent/
  ├── __init__.py
  ├── simple_agent.py   # Basic chat agent
  └── prompts.py        # System prompts
  ```
- [x] Implement Ollama Cloud client with authentication
- [x] Implement basic chat agent using LangGraph
- [x] Add system prompts for job portal context (job_seeker, company, general)
- [x] Test agent independently (without CLI)
- [x] Verify cloud API connection works

#### 2.3 CLI Integration ✅
- [x] Connect agent to CLI conversation loop
- [x] Replace echo with agent responses
- [x] Add streaming support (show response as it generates)
- [x] Handle errors gracefully (API key invalid, network issues, etc.)
- [x] Add `--no-agent` flag to disable AI and use echo mode
- [x] Graceful fallback when dependencies not installed

#### 2.4 Memory Setup ✅
- [x] Add LangGraph checkpointer for conversation memory
- [x] Use `MemorySaver` (in-memory checkpointer)
- [x] Implement thread_id per session (uses session_id)
- [x] Test multi-turn conversations with context retention

### Deliverable ✅
CLI that:
- ✅ Connects to Ollama Cloud API
- ✅ Has intelligent conversations
- ✅ Remembers context within session
- ✅ Streams responses in real-time
- ✅ Works WITHOUT database/tools
- ✅ No local installation required

### Test ✅
```bash
# Test agent independently
python -m src.job_portal.agent.simple_agent
# ✅ All tests pass

# Test comprehensive suite
python scripts/demos/test_agent.py
# ✅ All 5 tests pass

# Test CLI integration
python -m src.job_portal.cli.main start
# User: "Hi, I'm looking for a job"
# Agent: "Hello! I'd be happy to help you find a job..."
# User: "What did I just say?"
# Agent: "You mentioned you're looking for a job."
# ✅ Works perfectly
```

### Implementation Notes
- **Model Used**: `gpt-oss:120b` (120B parameter model from Ollama Cloud)
- **Available Models**: cogito-2.1:671b, glm-4.6, kimi-k2:1t, deepseek-v3.1:671b, gpt-oss:120b, gpt-oss:20b, and more
- **Architecture**: LangGraph with MessagesState and MemorySaver checkpointer
- **Streaming**: Implemented using `graph.stream()` with proper chunk handling
- **Error Handling**: Validates API key, handles missing dependencies, graceful fallbacks
- **System Prompts**: Context-aware prompts for job seekers vs companies

---

## Phase 3: Tool Definitions (Week 1, Day 5)

### Goal
Define tools that wrap existing repository methods, but don't connect agent yet.

### Tasks

#### 3.1 Tool Structure
- [x] Create `src/job_portal/agent/tools/`
  ```
  tools/
  ├── __init__.py
  ├── job_seeker_tools.py   # Tools for job seekers
  ├── company_tools.py      # Tools for companies
  └── common_tools.py       # Shared tools
  ```

#### 3.2 Job Seeker Tools
- [x] `search_jobs` - Vector search for matching companies
  - Input: job requirements (text)
  - Output: List of matching companies with scores
  - Wraps: `CompanyRepository.vector_search()`
  
- [x] `get_company_details` - Get full company info
  - Input: company_id
  - Output: Complete company document
  - Wraps: `CompanyRepository.get_by_id()`
  
- [x] `compare_companies` - Side-by-side comparison
  - Input: list of company_ids
  - Output: Structured comparison
  - Wraps: Multiple `get_by_id()` calls

#### 3.3 Company Tools
- [x] `search_candidates` - Vector search for matching job seekers
  - Input: job requirements (text)
  - Output: List of matching candidates with scores
  - Wraps: `JobSeekerRepository.vector_search()`
  
- [x] `get_candidate_details` - Get full candidate info
  - Input: candidate_id
  - Output: Complete candidate document
  - Wraps: `JobSeekerRepository.get_by_id()`
  
- [x] `compare_candidates` - Side-by-side comparison
  - Input: list of candidate_ids
  - Output: Structured comparison
  - Wraps: Multiple `get_by_id()` calls

#### 3.4 Tool Testing
- [x] Create `tests/agent/test_tools.py`
- [x] Test each tool independently
- [x] Mock repository responses
- [x] Verify tool schemas (LangChain format)

### Deliverable
- 6 working tools with proper schemas
- Each tool tested independently
- Tools NOT connected to agent yet

### Test
```python
# Test tool directly
from src.job_portal.agent.tools import search_jobs

result = search_jobs.invoke({
    "requirements": "Python developer with 5 years experience"
})
print(result)  # Should return matching companies
```

### ✅ Phase 3 Complete

**What was built:**
- Tool structure: `src/job_portal/agent/tools/`
- 3 job seeker tools: `search_jobs`, `get_company_details`, `compare_companies`
- 3 company tools: `search_candidates`, `get_candidate_details`, `compare_candidates`
- Common utilities in `common_tools.py`
- Comprehensive test suite: 20 tests, all passing
- Demo script: `scripts/demos/test_tools_directly.py`

**Key features:**
- All tools use LangChain `@tool` decorator
- Proper schemas with descriptions
- Lazy loading of MongoDB connections
- Error handling in all tools
- Vector search integration with embeddings
- Formatted output for easy reading

**Test results:**
```
20 passed in 2.23s
```

---

## Phase 4: Database Integration (Week 2, Days 1-2)

### Goal
Connect tools to MongoDB and test vector search with real data.

### Prerequisites
- [x] Verify MongoDB connection works
- [x] Verify sample data exists
- [x] Verify vector indexes are set up

### Tasks

#### 4.1 Repository Integration
- [x] Update tools to use real repositories
- [x] Add error handling for DB failures
- [x] Add rate limiting for Voyage AI (if generating embeddings)
- [x] Test with real data

#### 4.2 Embedding Integration
- [x] Connect `search_jobs` to embedding service
- [x] Connect `search_candidates` to embedding service
- [x] Add caching for repeated queries (via lazy loading)
- [x] Handle rate limits gracefully (20s delays)

#### 4.3 Data Validation
- [x] Ensure sample data has embeddings
- [x] If not, run embedding generation script
- [x] Verify vector search returns results
- [x] Test with various queries

#### 4.4 Tool Enhancement
- [x] Add result formatting (pretty output with emojis)
- [x] Add pagination support (limit parameter with max 10)
- [x] Add filtering options (built into repositories)
- [x] Add sorting options (by relevance/score)

### Deliverable
- Tools connected to real database
- Vector search working with embeddings
- Tools return formatted, useful results

### Test
```python
# Test with real DB
from src.job_portal.agent.tools import search_jobs

result = search_jobs.invoke({
    "requirements": "Senior Python developer, remote, fintech"
})
# Should return real companies from MongoDB
```

### ✅ Phase 4 Complete

**What was enhanced:**
- All tools now connected to real MongoDB database
- Vector search working with real embeddings
- Rate limiting implemented (20s delays between API calls)
- Enhanced output formatting with emojis and better structure
- Error handling improved with helpful messages
- Helper functions added for formatting (salary, truncation)
- Limit validation (1-10 results)
- Better user guidance in output messages

**Key improvements:**
- Match scores now shown as percentages (e.g., "95.0%")
- Salary ranges formatted with commas
- Skills limited to top 5 in search results
- Comparison tools show preview snippets
- Not found IDs tracked and reported
- Helpful tips added to search results

**Test results:**
- All 20 unit tests passing
- Real data integration verified
- Vector search returning accurate matches
- Tools working end-to-end with MongoDB Atlas

---

## Phase 5: Agent + Tools Integration (Week 2, Days 3-4)

### Goal
Connect tools to agent so it can use them intelligently.

### Tasks

#### 5.1 Agent Enhancement ✅
- [x] Update agent to include tools
- [x] Add tool selection logic
- [x] Implement tool error handling
- [x] Add tool result formatting

#### 5.2 Context-Aware Prompts ✅
- [x] Create different prompts for job seekers vs companies
- [x] Add instructions for tool usage
- [x] Add examples of good tool calls
- [x] Add guidelines for result presentation

#### 5.3 State Management ✅
- [x] Extend state schema
  ```python
  class JobPortalState(MessagesState):
      user_type: str
      search_results: list
      selected_items: list
      comparison_mode: bool
  ```
- [x] Update state in tools
- [x] Use state in agent decisions

#### 5.4 CLI Updates ✅
- [x] Show tool calls in UI (optional, for debugging)
- [x] Format tool results nicely
- [x] Add loading indicators during tool execution
- [x] Handle long-running operations

### Deliverable ✅
- Agent that intelligently uses tools
- Natural conversation flow
- Tools called at appropriate times
- Results presented clearly

### Test
```bash
# Test Phase 5 implementation
python scripts/demos/test_phase5_agent.py

# Run full CLI with tools
python -m src.job_portal.cli.main start

# Example conversation:
# User: "I'm a job seeker"
# Agent: "Great! What kind of job are you looking for?"
# User: "Python developer, remote, fintech"
# Agent: [calls search_jobs tool]
# Agent: "I found 5 matching companies! Here's an overview..."
```

### Implementation Notes

**Agent Enhancements:**
- `SimpleAgent` now supports tool binding based on user type
- Job seekers get: `search_jobs`, `get_company_details`, `compare_companies`
- Companies get: `search_candidates`, `get_candidate_details`, `compare_candidates`
- Graph uses conditional routing to handle tool calls automatically

**Prompt Improvements:**
- Enhanced system prompts with detailed tool usage instructions
- Clear examples of when to use each tool
- Guidelines for extracting requirements from conversation
- Natural language presentation of tool results

**State Management:**
- Extended `SessionState` with `comparison_mode`, `last_tool_call`
- Methods to track tool usage and search results
- State persists across conversation turns

**CLI Enhancements:**
- Loading indicators during tool execution
- Visual feedback showing which tools were used
- Better error handling for tool failures
- Respects rate limits (20s delay between Voyage AI calls)

---

## Phase 6: Advanced Features (Week 2, Day 5)

### Goal
Add comparison, selection, and advanced interaction patterns.

### Tasks

#### 6.1 Selection Mechanism
- [ ] Add numbered results
- [ ] Allow user to select by number
- [ ] Store selections in state
- [ ] Show selected items

#### 6.2 Comparison Feature
- [ ] Implement comparison tool
- [ ] Format side-by-side comparison
- [ ] Add comparison table with Rich
- [ ] Allow adding/removing from comparison

#### 6.3 Conversation Patterns
- [ ] Handle follow-up questions
- [ ] Support refinement ("show me more like #2")
- [ ] Support filtering ("only remote positions")
- [ ] Support sorting ("sort by salary")

#### 6.4 Export/Save
- [ ] Save search results to file
- [ ] Export comparison to PDF/HTML
- [ ] Save conversation history
- [ ] Bookmark favorite results

### Deliverable
- Full-featured CLI with all interactions
- Comparison working smoothly
- Natural conversation flow
- Export capabilities

### Test
```bash
# Full workflow test
python -m src.job_portal.cli.main
# 1. Select user type
# 2. Search for jobs
# 3. Select specific company
# 4. Compare with others
# 5. Export results
```

---

## Phase 7: Polish & Production (Week 3)

### Goal
Make it production-ready with error handling, logging, and documentation.

### Tasks

#### 7.1 Error Handling
- [ ] Handle Ollama not running
- [ ] Handle MongoDB connection failures
- [ ] Handle Voyage AI rate limits
- [ ] Handle invalid user input
- [ ] Add retry logic

#### 7.2 Logging
- [ ] Add structured logging
- [ ] Log agent decisions
- [ ] Log tool calls
- [ ] Log errors with context

#### 7.3 Configuration
- [ ] Move all config to `.env`
- [ ] Add config validation
- [ ] Add config documentation
- [ ] Support multiple Ollama models

#### 7.4 Documentation
- [ ] Write README for CLI
- [ ] Add usage examples
- [ ] Document tool schemas
- [ ] Add troubleshooting guide

#### 7.5 Testing
- [ ] Add integration tests
- [ ] Add CLI tests
- [ ] Add agent tests
- [ ] Add tool tests

### Deliverable
- Production-ready CLI application
- Comprehensive documentation
- Full test coverage
- Robust error handling

---

## Success Criteria

### Phase 1 ✅ COMPLETE
- CLI runs and accepts input
- Beautiful UI with Rich
- Session management works
- All commands functional
- Tests passing

### Phase 2 ✅ COMPLETE
- ✅ Can chat with Ollama Cloud
- ✅ Conversation memory works (LangGraph MemorySaver)
- ✅ Streaming responses
- ✅ User type awareness (job_seeker/company)
- ✅ Error handling and graceful fallbacks

### Phase 3 ✓
- All 6 tools defined
- Tools tested independently
- Proper schemas

### Phase 4 ✓
- Tools connected to MongoDB
- Vector search working
- Real results returned

### Phase 5 ✓
- Agent uses tools intelligently
- Natural conversation
- Results formatted nicely

### Phase 6 ✓
- Comparison feature works
- Selection mechanism works
- Export capabilities

### Phase 7 ✓
- Production-ready
- Documented
- Tested

---

## Timeline Summary

| Phase | Duration | Focus |
|-------|----------|-------|
| 1 | 2 days | CLI Foundation |
| 2 | 2 days | Ollama Integration |
| 3 | 1 day | Tool Definitions |
| 4 | 2 days | Database Integration |
| 5 | 2 days | Agent + Tools |
| 6 | 1 day | Advanced Features |
| 7 | 3 days | Polish & Production |
| **Total** | **~2 weeks** | **Full Implementation** |

---

## Technical Stack

### Core Dependencies
```txt
# LLM & Agent Framework
langgraph>=0.2.0
langchain>=1.0.0
langchain-ollama>=0.1.0

# CLI
rich>=13.0.0
typer>=0.9.0
prompt-toolkit>=3.0.0

# Existing Stack
pymongo>=4.6.0
voyageai>=0.2.0
python-dotenv>=1.0.0
```

### Environment Variables
```env
# MongoDB & Voyage (existing)
MONGODB_URI=mongodb+srv://...
VOYAGE_API_KEY=...

# Ollama Cloud Configuration
OLLAMA_API_KEY=your_api_key_here
OLLAMA_BASE_URL=https://ollama.com
OLLAMA_MODEL=gpt-oss:120b-cloud
```

---

## Project Structure

```
src/job_portal/
├── agent/
│   ├── __init__.py
│   ├── simple_agent.py       # Basic chat agent (Phase 2)
│   ├── agent.py              # Full agent with tools (Phase 5)
│   ├── prompts.py            # System prompts
│   ├── state.py              # Custom state schema
│   └── tools/
│       ├── __init__.py
│       ├── job_seeker_tools.py
│       ├── company_tools.py
│       └── common_tools.py
│
├── cli/
│   ├── __init__.py
│   ├── main.py               # CLI entry point
│   ├── ui.py                 # Rich UI components
│   ├── session.py            # Session management
│   └── commands.py           # Command handlers
│
├── services/
│   └── embeddings/           # Existing embedding service
│
└── repositories/             # Existing repos
    ├── company_repository.py
    ├── jobseeker_repository.py
    └── base_vector_store.py
```

---

## Key Design Decisions

### Why Ollama Cloud?
- ✅ No local installation required
- ✅ Access to larger models (120B+)
- ✅ No GPU/hardware requirements
- ✅ Simple API key authentication
- ✅ Compatible with LangChain/LangGraph
- ✅ Same API as local Ollama (easy to switch)

**Cloud vs Local Comparison:**

| Feature | Ollama Cloud | Local Ollama |
|---------|--------------|--------------|
| Installation | None required | Download & install |
| Hardware | Any computer | GPU recommended |
| Model Size | Up to 120B+ | Limited by RAM/VRAM |
| Setup Time | 2 minutes | 10-30 minutes |
| Cost | API usage (preview) | Free (hardware cost) |
| Privacy | Data sent to cloud | Data stays local |
| Speed | Network dependent | Hardware dependent |

**For this project**: We use Ollama Cloud for simplicity and access to larger models. You can switch to local later by changing the `OLLAMA_BASE_URL` in `.env`.

### Why LangChain's `create_agent`?
- ✅ Simpler than raw LangGraph
- ✅ Built on LangGraph (can customize later)
- ✅ Handles tool calling automatically
- ✅ Easy memory integration
- ✅ Recommended by LangChain v1.0

### Why Rich + Typer?
- ✅ Beautiful terminal UI
- ✅ Easy to use
- ✅ Great for prototyping
- ✅ Professional appearance

### Why Incremental Approach?
- ✅ Test each layer independently
- ✅ Catch issues early
- ✅ Easy to debug
- ✅ Can demo progress at each phase

---

## Important Notes

### Rate Limits (Voyage AI)
- **3 requests per minute (RPM)** on free tier
- Add 20+ second delays between embedding calls
- Use batch processing when possible
- See `docs/embeddings/RATE_LIMITS.md`

### Ollama Cloud Models
Recommended cloud models for tool calling:
- `gpt-oss:120b-cloud` - Large model, excellent reasoning
- Other cloud models available at: https://ollama.com/search?c=cloud

**Note**: Cloud models are marked with `-cloud` suffix and require API key authentication.

### Memory Strategy
- **Short-term**: LangGraph checkpointer (conversation history)
- **Long-term**: Could add LangGraph store later (user preferences)
- Start with `InMemorySaver`, upgrade to SQLite later if needed

---

## Next Steps

Ready to start **Phase 1: CLI Foundation**?

When ready, say "start phase 1" to begin implementation!

---

**Last Updated**: November 27, 2025
**Status**: Planning Complete ✓
**Next**: Phase 1 Implementation
