# Phase 5 Complete: Agent with Tools ✅

**Completion Date**: November 28, 2025  
**Status**: ✅ All tasks completed

## Overview

Phase 5 enhanced the conversational agent with intelligent tool usage, context-aware prompts, extended state management, and improved CLI experience. The agent now proactively uses tools to search for jobs/candidates, retrieve details, and compare options based on natural conversation.

## What Was Implemented

### 1. Agent Enhancement ✅

**File**: `src/job_portal/agent/simple_agent.py`

**Changes**:
- Extended `MessagesState` to `JobPortalState` with additional fields:
  - `user_type`: Track whether user is job seeker or company
  - `search_results`: Store search results for reference
  - `selected_items`: Track items user is interested in
  - `comparison_mode`: Flag for comparison operations

- Added tool binding based on user type:
  ```python
  def _get_tools_for_user_type(self, user_type):
      if user_type == "job_seeker":
          return [search_jobs, get_company_details, compare_companies]
      elif user_type == "company":
          return [search_candidates, get_candidate_details, compare_candidates]
  ```

- Implemented conditional routing in graph:
  - Agent → Tools (if tool calls present)
  - Tools → Agent (for processing results)
  - Agent → END (if no tool calls)

- Added tool error handling and result formatting

**Key Features**:
- Automatic tool selection based on conversation context
- Seamless integration with LangGraph workflow
- Dynamic tool binding when user type changes
- Memory-aware conversations with tool results

### 2. Context-Aware Prompts ✅

**File**: `src/job_portal/agent/prompts.py`

**Changes**:
- Enhanced `JOB_SEEKER_SYSTEM_PROMPT` with:
  - Detailed tool descriptions
  - Usage guidelines for each tool
  - Examples of when to use tools
  - Instructions for natural result presentation

- Enhanced `COMPANY_SYSTEM_PROMPT` with:
  - Company-specific tool instructions
  - Candidate search guidelines
  - Professional tone guidance

- Added `get_system_prompt_with_tools()` function

**Example Prompt Section**:
```
Available Tools:
- search_jobs: Search for job postings matching requirements
- get_company_details: Get full details about a specific company/job
- compare_companies: Compare multiple job opportunities side-by-side

Tool Usage Guidelines:
- Use search_jobs when the user describes their job requirements
- Extract key requirements from conversation
- After showing results, offer to provide more details
...
```

**Benefits**:
- Agent knows exactly when to use tools
- Natural conversation flow maintained
- Clear examples guide tool usage
- Results presented conversationally

### 3. State Management ✅

**File**: `src/job_portal/cli/session.py`

**Changes**:
- Extended `SessionState` dataclass:
  ```python
  @dataclass
  class SessionState:
      session_id: str
      user_type: Optional[str] = None
      conversation_history: List[Dict[str, str]]
      selected_items: List[str]
      search_results: List[Dict[str, Any]]
      comparison_mode: bool = False
      last_tool_call: Optional[str] = None
      created_at: str
      updated_at: str
  ```

- Added state management methods:
  - `set_comparison_mode(enabled)`: Toggle comparison mode
  - `record_tool_call(tool_name)`: Track tool usage
  - `add_search_results(results)`: Store search results

**Benefits**:
- Track conversation context across turns
- Remember what user searched for
- Enable follow-up questions about results
- Support multi-turn tool interactions

### 4. CLI Updates ✅

**File**: `src/job_portal/cli/main.py`

**Changes**:
- Added loading indicators during tool execution:
  ```python
  with console.status("[bold cyan]Thinking...", spinner="dots"):
      # Agent processing with tools
  ```

- Tool call visualization:
  ```python
  if tool_calls_made:
      tool_list = ", ".join(set(tool_calls_made))
      console.print(f"[dim]🔧 Used tools: {tool_list}[/dim]")
  ```

- Event streaming from graph to track tool calls
- Better error handling for tool failures
- Session state updates after tool usage

**User Experience**:
- Visual feedback during processing
- See which tools were used
- Smooth conversation flow
- Clear error messages

## Architecture

### Tool Flow

```
User Input
    ↓
Agent (LLM with tools)
    ↓
Tool Call? ──No──→ Response to User
    ↓ Yes
Tool Execution
    ↓
Tool Results
    ↓
Agent (process results)
    ↓
Response to User
```

### State Flow

```
Session Start
    ↓
User Type Selection → Update SessionState.user_type
    ↓
Conversation → Update conversation_history
    ↓
Tool Call → Update last_tool_call
    ↓
Search Results → Update search_results
    ↓
Item Selection → Update selected_items
    ↓
Comparison → Update comparison_mode
    ↓
Session Save → Persist to .sessions/
```

## Testing

### Test Script

**File**: `scripts/demos/test_phase5_agent.py`

**Tests**:
1. **Tool Selection**: Verify correct tools loaded for user type
2. **User Type Switching**: Test dynamic tool binding
3. **Job Seeker Flow**: Test conversation with job search tools
4. **Company Flow**: Test conversation with candidate search tools

**Run Tests**:
```bash
python scripts/demos/test_phase5_agent.py
```

### Manual Testing

**Test Job Seeker Flow**:
```bash
python -m src.job_portal.cli.main start

# Conversation:
User: I'm a job seeker
Agent: Great! What kind of job are you looking for?

User: Python developer, remote, fintech
Agent: [🔧 Used tools: search_jobs]
      🔍 Found 5 matching job posting(s):
      
      1. 🏢 TechCorp
         💼 Job: Senior Python Developer
         📍 Location: Remote
         💰 Salary: $120,000 - $180,000
         🎯 Match: 92.5%
         ...

User: Tell me more about the first one
Agent: [🔧 Used tools: get_company_details]
      ======================================================================
      🏢 TechCorp
      ======================================================================
      
      💼 Position: Senior Python Developer
      ...
```

**Test Company Flow**:
```bash
python -m src.job_portal.cli.main start

# Conversation:
User: We're hiring
Agent: Great! What kind of candidate are you looking for?

User: Senior Python developer with ML experience
Agent: [🔧 Used tools: search_candidates]
      🔍 Found 5 matching candidate(s):
      
      1. 👤 John Doe
         💼 Title: Senior Python Developer
         📊 Experience: 8 years
         🎯 Match: 94.2%
         ...
```

## Key Features

### 1. Intelligent Tool Usage
- Agent automatically detects when to use tools
- Extracts requirements from natural conversation
- No explicit commands needed from user

### 2. Context-Aware Responses
- Different behavior for job seekers vs companies
- Remembers previous searches
- Offers relevant follow-up actions

### 3. Natural Conversation
- Tool results presented conversationally
- No technical jargon exposed to user
- Smooth flow between chat and tool usage

### 4. Visual Feedback
- Loading indicators during processing
- Tool usage transparency (optional)
- Clear error messages

### 5. State Persistence
- Conversations saved across sessions
- Search results remembered
- Can resume previous conversations

## Rate Limiting

**Important**: Tools use Voyage AI embeddings with rate limits:
- **3 requests per minute (RPM)**
- **20 second delay** between API calls
- Handled automatically in tool implementations

**Impact on UX**:
- Search operations take ~20 seconds
- Loading indicator shows progress
- User sees "Thinking..." during processing

## Files Modified

### Core Agent
- ✅ `src/job_portal/agent/simple_agent.py` - Enhanced with tools
- ✅ `src/job_portal/agent/prompts.py` - Context-aware prompts

### State Management
- ✅ `src/job_portal/cli/session.py` - Extended state schema

### CLI
- ✅ `src/job_portal/cli/main.py` - Tool visualization and loading

### Documentation
- ✅ `docs/AGENTIC_CLI_PLAN.md` - Updated with completion status
- ✅ `docs/PHASE_5_COMPLETE.md` - This document

### Testing
- ✅ `scripts/demos/test_phase5_agent.py` - Phase 5 tests

## Usage Examples

### Example 1: Job Search
```python
from job_portal.agent.simple_agent import SimpleAgent

agent = SimpleAgent(user_type="job_seeker")

# Natural conversation triggers tool usage
response = agent.chat(
    "I'm looking for a remote Python developer position in fintech",
    thread_id="user123"
)
# Agent automatically calls search_jobs tool
# Returns formatted results conversationally
```

### Example 2: Candidate Search
```python
agent = SimpleAgent(user_type="company")

response = agent.chat(
    "We need a senior ML engineer with 5+ years experience",
    thread_id="company456"
)
# Agent automatically calls search_candidates tool
# Returns formatted candidate list
```

### Example 3: Follow-up Questions
```python
# After search results shown
response = agent.chat(
    "Tell me more about the first candidate",
    thread_id="company456"
)
# Agent calls get_candidate_details with ID from previous results
```

## Performance Considerations

### Tool Execution Time
- **Search operations**: ~20-25 seconds (due to rate limiting)
- **Detail retrieval**: ~1-2 seconds (MongoDB query)
- **Comparison**: ~1-2 seconds (MongoDB queries)

### Memory Usage
- State stored in `.sessions/` directory
- Each session ~5-10 KB
- Conversation history grows with usage

### API Costs
- **Voyage AI**: Free tier (200M tokens)
- **Ollama Cloud**: Pay per token
- **MongoDB Atlas**: Free tier (512 MB)

## Next Steps

Phase 5 is complete! Possible future enhancements:

### Phase 6 Ideas (Optional)
1. **Advanced Filtering**
   - Add filter tools for salary, location, skills
   - Multi-criteria search refinement

2. **Recommendations**
   - Proactive job/candidate suggestions
   - "You might also like..." feature

3. **Analytics**
   - Track search patterns
   - Popular skills/requirements
   - Match success rates

4. **Notifications**
   - Alert when new matches appear
   - Save searches for later

5. **Multi-modal**
   - Resume parsing (PDF/DOCX)
   - Job description analysis
   - Skill gap identification

## Troubleshooting

### Issue: Tools not being called
**Solution**: Check system prompt includes tool instructions
```python
from job_portal.agent.prompts import get_system_prompt_with_tools
prompt = get_system_prompt_with_tools("job_seeker")
print(prompt)  # Should show tool descriptions
```

### Issue: Rate limit errors
**Solution**: Tools have built-in 20s delays, but check:
```python
# In tools/job_seeker_tools.py
def _handle_rate_limit():
    # Ensures 20s between calls
```

### Issue: Tool results not formatted
**Solution**: Check tool output includes emojis and formatting:
```python
output = f"🔍 Found {len(results)} matching job posting(s):\n\n"
```

### Issue: State not persisting
**Solution**: Ensure session is saved after each interaction:
```python
session_manager.save_session(session)
```

## Conclusion

Phase 5 successfully transformed the basic chat agent into an intelligent assistant that:
- ✅ Uses tools proactively based on conversation
- ✅ Adapts behavior to user type (job seeker vs company)
- ✅ Maintains context across conversation turns
- ✅ Provides visual feedback during processing
- ✅ Presents results in a natural, conversational way

The agent is now production-ready for real-world job portal interactions!

---

**Status**: ✅ Phase 5 Complete  
**Next Phase**: Optional enhancements (see Next Steps)  
**Last Updated**: November 28, 2025
