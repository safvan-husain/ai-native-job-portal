# CLI Usage Guide

## Quick Start

### Start the CLI
```bash
python -m src.job_portal.cli.main start
```

### Available Commands

#### Main Commands
- `start` - Start a new interactive session
- `list-sessions` - Show all saved sessions
- `delete-session <id>` - Delete a specific session

#### In-Session Commands
- `help` - Show help information
- `clear` - Clear the screen
- `exit` / `quit` / `bye` - Exit the application
- `new` - Start a new conversation (clears history)
- `history` - Show conversation history

## Examples

### Starting a New Session
```bash
python -m src.job_portal.cli.main start
```

You'll be prompted to:
1. Select user type (Job Seeker or Company)
2. Start chatting

### Resuming a Session
```bash
python -m src.job_portal.cli.main start --session <session-id>
```

### Forcing a New Session
```bash
python -m src.job_portal.cli.main start --new
```

### List All Sessions
```bash
python -m src.job_portal.cli.main list-sessions
```

### Delete a Session
```bash
python -m src.job_portal.cli.main delete-session <session-id>
```

## Session Management

Sessions are automatically saved to `.sessions/` directory as JSON files.

Each session contains:
- Session ID
- User type (job_seeker or company)
- Conversation history
- Selected items (for comparison)
- Search results
- Timestamps

## Current Status (Phase 1 Complete)

✅ **Working Features:**
- Beautiful CLI interface with Rich
- User type selection
- Conversation loop (echo mode)
- Session persistence
- Command handling
- Conversation history

⏳ **Coming in Phase 2:**
- Ollama LLM integration
- Intelligent responses
- Conversation memory
- Streaming responses

## Testing

Run the test suite:
```bash
python scripts/demos/test_cli.py
```

## Troubleshooting

### Import Errors
Make sure you're running from the project root:
```bash
cd /path/to/rag-learning-project
python -m src.job_portal.cli.main start
```

### Session Not Found
If a session ID doesn't exist, the CLI will automatically create a new session.

### Clear All Sessions
```bash
rm -rf .sessions/
```

## Next Steps

Once Phase 2 is complete, you'll be able to:
- Have intelligent conversations with Ollama
- Get contextual responses
- Use conversation memory across sessions
