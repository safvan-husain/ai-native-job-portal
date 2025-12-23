# Phase 5 Usage Guide: Agent with Tools

Quick reference for using the enhanced conversational agent with intelligent tool support.

## Quick Start

### Start the CLI
```bash
python -m src.job_portal.cli.main start
```

### Resume a Session
```bash
python -m src.job_portal.cli.main start --session <session-id>
```

### List Sessions
```bash
python -m src.job_portal.cli.main list-sessions
```

## Job Seeker Examples

### Example 1: Basic Job Search
```
You: I'm a job seeker
Agent: Great! What kind of job are you looking for?

You: Python developer, remote work, fintech industry
Agent: [🔧 Used tools: search_jobs]
      🔍 Found 5 matching job posting(s):
      
      1. 🏢 TechCorp
         💼 Job: Senior Python Developer
         📍 Location: Remote
         💰 Salary: $120,000 - $180,000
         🎯 Match: 92.5%
         🆔 ID: 507f1f77bcf86cd799439011
      ...
```

### Example 2: Get Job Details
```
You: Tell me more about TechCorp
Agent: [🔧 Used tools: get_company_details]
      ======================================================================
      🏢 TechCorp
      ======================================================================
      
      💼 Position: Senior Python Developer
      🏭 Company Size: 500 employees
      🏢 Industry: Fintech
      📍 Location: Remote
      
      📝 Job Description:
      We're looking for an experienced Python developer...
```

### Example 3: Compare Jobs
```
You: Compare the first three jobs
Agent: [🔧 Used tools: compare_companies]
      ======================================================================
      📊 Comparing 3 Job Opportunities
      ======================================================================
      
      Option 1: 🏢 TechCorp
      ─────────────────────────────────────────────────────────────────────
      💼 Job Title: Senior Python Developer
      📍 Location: Remote | Fully Remote
      💰 Salary: $120,000 - $180,000
      ...
```

## Company Examples

### Example 1: Candidate Search
```
You: We're hiring
Agent: Great! What kind of candidate are you looking for?

You: Senior Python developer with ML experience, 5+ years
Agent: [🔧 Used tools: search_candidates]
      🔍 Found 5 matching candidate(s):
      
      1. 👤 John Doe
         💼 Title: Senior Python Developer
         📊 Experience: 8 years
         💰 Desired Salary: $150,000+
         🎯 Match: 94.2%
         🆔 ID: 507f1f77bcf86cd799439012
      ...
```

### Example 2: Candidate Details
```
You: Show me details for John Doe
Agent: [🔧 Used tools: get_candidate_details]
      ======================================================================
      👤 John Doe
      ======================================================================
      
      💼 Current Title: Senior Python Developer
      📊 Experience: 8 years
      🎓 Education: Master's in Computer Science
      
      📝 Profile Summary:
      Experienced Python developer specializing in ML...
```

### Example 3: Compare Candidates
```
You: Compare the top 3 candidates
Agent: [🔧 Used tools: compare_candidates]
      ======================================================================
      📊 Comparing 3 Candidates
      ======================================================================
      
      Candidate 1: 👤 John Doe
      ─────────────────────────────────────────────────────────────────────
      💼 Title: Senior Python Developer
      📊 Experience: 8 years
      🎓 Education: Master's in Computer Science
      ...
```

## Natural Language Patterns

The agent understands various ways of asking for the same thing:

### Job Search Patterns
- "I'm looking for a Python job"
- "Find me remote developer positions"
- "Show me fintech opportunities"
- "I want to work as a data scientist"
- "Search for ML engineer roles"

### Detail Request Patterns
- "Tell me more about [company name]"
- "Show details for the first result"
- "What's the job description for [company]?"
- "Give me more info on that position"

### Comparison Patterns
- "Compare the first three"
- "Show me a comparison of these jobs"
- "Which one is better?"
- "Compare [company1] and [company2]"

## Tool Behavior

### Automatic Tool Selection
The agent automatically decides when to use tools based on:
- User intent (searching, getting details, comparing)
- User type (job seeker vs company)
- Conversation context

### Tool Execution Time
- **Search**: ~20-25 seconds (Voyage AI rate limiting)
- **Details**: ~1-2 seconds (MongoDB query)
- **Compare**: ~1-2 seconds (MongoDB queries)

You'll see a loading indicator: `[bold cyan]Thinking...`

### Tool Feedback
After tool execution, you'll see:
```
[dim]🔧 Used tools: search_jobs[/dim]
```

This helps you understand what the agent did.

## Tips for Best Results

### 1. Be Specific
❌ "Find me a job"
✅ "Find me a remote Python developer job in fintech"

### 2. Use Natural Language
❌ "search_jobs(query='python')"
✅ "I'm looking for Python developer positions"

### 3. Follow Up Naturally
After search results:
- "Tell me more about the first one"
- "Compare the top three"
- "Show me details for TechCorp"

### 4. Provide Context
- "I have 5 years of Python experience"
- "I prefer remote work"
- "I'm interested in fintech"

The agent uses this context to refine searches.

## CLI Commands

### During Conversation
- `help` - Show available commands
- `history` - Show conversation history
- `clear` - Clear screen
- `exit` - Exit the CLI

### Session Management
```bash
# Start new session
python -m src.job_portal.cli.main start --new

# Resume session
python -m src.job_portal.cli.main start --session <id>

# List all sessions
python -m src.job_portal.cli.main list-sessions

# Delete session
python -m src.job_portal.cli.main delete-session <id>
```

## Troubleshooting

### Agent Not Using Tools
**Symptom**: Agent just chats, doesn't search
**Solution**: Be more explicit about what you want
```
Instead of: "I need help"
Try: "I'm looking for a Python developer job"
```

### Slow Responses
**Symptom**: Takes 20+ seconds to respond
**Reason**: Voyage AI rate limiting (3 RPM)
**Solution**: This is normal for search operations

### Tool Errors
**Symptom**: "Error searching for jobs"
**Check**:
1. MongoDB connection: `python scripts/maintenance/test_connection.py`
2. Voyage API key in `.env`
3. Internet connection

### No Results Found
**Symptom**: "No matching jobs found"
**Try**:
1. Broader search terms
2. Remove specific requirements
3. Check if sample data exists: `python scripts/maintenance/seed_sample_data.py`

## Advanced Usage

### Programmatic Usage
```python
from job_portal.agent.simple_agent import SimpleAgent

# Create agent
agent = SimpleAgent(user_type="job_seeker")

# Single response
response = agent.chat(
    "Find me Python developer jobs",
    thread_id="user123"
)
print(response)

# Streaming response
for chunk in agent.stream_chat(
    "Tell me more about the first result",
    thread_id="user123"
):
    print(chunk, end="")
```

### Custom Configuration
```python
agent = SimpleAgent(
    user_type="job_seeker",
    model="llama3.1:8b",  # Custom model
    base_url="https://ollama.com",
    api_key="your-key"
)
```

### Switch User Type
```python
agent = SimpleAgent(user_type="job_seeker")
# ... use as job seeker ...

agent.set_user_type("company")
# ... now use as company ...
```

## State Management

### What's Tracked
- User type (job seeker or company)
- Conversation history
- Search results
- Selected items
- Last tool used
- Comparison mode

### Session Persistence
Sessions are saved to `.sessions/` directory:
```
.sessions/
  ├── 2f7e5904-d107-433f-84cd-f4510489ff44.json
  ├── 9bee146c-8d29-4fd0-aafe-d7f08b7ed2c4.json
  └── cec2c7b6-3628-4f73-b053-2f00ea74c8bc.json
```

### Resume Previous Session
```bash
# List sessions to find ID
python -m src.job_portal.cli.main list-sessions

# Resume specific session
python -m src.job_portal.cli.main start --session <id>
```

## Rate Limits

### Voyage AI Limits
- **3 requests per minute (RPM)**
- **10,000 tokens per minute (TPM)**
- **200M free tokens** total

### Impact
- Search operations have 20s delay
- Multiple searches take time
- Loading indicator shows progress

### Best Practices
- Be patient during searches
- Don't spam search requests
- Use detail/compare tools (no rate limit)

## Examples by Use Case

### Use Case 1: Job Seeker Finding First Job
```
You: Hi, I just graduated with a CS degree
Agent: Congratulations! What kind of position are you looking for?

You: Entry-level Python developer, open to location
Agent: [searches] Found 5 entry-level Python positions...

You: Which one is best for beginners?
Agent: Based on the results, I'd recommend...

You: Show me details for that one
Agent: [shows details] Here's the full job description...
```

### Use Case 2: Company Hiring Senior Developer
```
You: We need to hire a senior developer
Agent: What specific skills and experience are you looking for?

You: Senior Python developer, 5+ years, ML experience, fintech background
Agent: [searches] Found 5 matching candidates...

You: Compare the top 3
Agent: [compares] Here's a side-by-side comparison...

You: Show me full profile for candidate 1
Agent: [shows details] Here's the complete profile...
```

### Use Case 3: Career Change
```
You: I'm a Java developer wanting to switch to Python
Agent: Great! What kind of Python roles interest you?

You: Backend development, preferably remote
Agent: [searches] Found 5 Python backend positions...

You: Which ones accept career changers?
Agent: Looking at the experience requirements...

You: Show me the most flexible one
Agent: [shows details] This position seems most open...
```

## Next Steps

After Phase 5, you can:
1. Use the CLI for real job/candidate matching
2. Integrate with your application
3. Customize prompts for your use case
4. Add more tools for specific needs
5. Deploy to production

## Support

### Documentation
- `docs/PHASE_5_COMPLETE.md` - Implementation details
- `docs/AGENTIC_CLI_PLAN.md` - Full project plan
- `docs/embeddings/` - Embedding system docs

### Testing
```bash
# Test agent functionality
python scripts/demos/test_phase5_agent.py

# Test full system
python -m src.job_portal.cli.main start
```

### Issues
Check:
1. Environment variables in `.env`
2. MongoDB connection
3. Voyage API key validity
4. Sample data exists

---

**Happy matching!** 🎯
