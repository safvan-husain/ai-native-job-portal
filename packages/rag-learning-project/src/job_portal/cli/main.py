"""
Main entry point for the Job Portal CLI.
"""

import uuid
import typer
from typing import Optional
from rich.live import Live
from rich.spinner import Spinner
from rich.panel import Panel
from rich.markdown import Markdown
from .ui import (
    print_welcome,
    print_user_type_selection,
    get_user_type_choice,
    print_user_message,
    print_assistant_message,
    print_system_message,
    print_error,
    print_divider,
    get_input,
    console
)
from .session import SessionState, SessionManager
from .commands import CommandHandler

# Import agent (with fallback for when dependencies aren't installed)
try:
    from ..agent import SimpleAgent
    AGENT_AVAILABLE = True
except ImportError as e:
    AGENT_AVAILABLE = False
    AGENT_IMPORT_ERROR = str(e)


app = typer.Typer(
    name="job-portal",
    help="Interactive AI assistant for job portal",
    add_completion=False
)


def run_conversation_loop(
    session: SessionState,
    session_manager: SessionManager,
    use_agent: bool = True
):
    """Run the main conversation loop."""
    command_handler = CommandHandler(session)
    
    # Initialize agent if available and requested
    agent = None
    if use_agent and AGENT_AVAILABLE:
        try:
            agent = SimpleAgent(user_type=session.user_type)
            print_system_message("🤖 AI Agent initialized successfully!")
        except Exception as e:
            print_error(f"Failed to initialize agent: {str(e)}")
            print_system_message("Falling back to echo mode...")
            agent = None
    elif use_agent and not AGENT_AVAILABLE:
        print_error(f"Agent not available: {AGENT_IMPORT_ERROR}")
        print_system_message("Please install dependencies: pip install -r requirements.txt")
        print_system_message("Falling back to echo mode...")
    
    # Show user type if already set
    if session.user_type:
        user_type_display = "Job Seeker" if session.user_type == "job_seeker" else "Company"
        print_system_message(f"Continuing as: {user_type_display}")
        print_divider()
    
    while True:
        try:
            # Get user input
            user_input = get_input()
            
            # Skip empty input
            if not user_input.strip():
                continue
            
            # Handle commands
            result = command_handler.handle_command(user_input)
            
            if result == "exit":
                # Save session before exit
                session_manager.save_session(session)
                break
            elif result is None:
                # Command was handled, continue loop
                continue
            
            # Add user message to history
            session.add_message("user", user_input)
            print_user_message(user_input)
            
            # Generate response
            if agent:
                # Use AI agent with tool support
                try:
                    # Show loading indicator
                    with console.status("[bold cyan]Thinking...", spinner="dots"):
                        # Get response from agent (may include tool calls)
                        config = {"configurable": {"thread_id": session.session_id}}
                        
                        # Track tool calls
                        tool_calls_made = []
                        final_response = None
                        
                        # Stream events from the graph
                        for event in agent.graph.stream(
                            {"messages": [{"role": "user", "content": user_input}]},
                            config=config,
                            stream_mode="values"
                        ):
                            messages = event.get("messages", [])
                            if messages:
                                last_message = messages[-1]
                                
                                # Check for tool calls
                                if hasattr(last_message, "tool_calls") and last_message.tool_calls:
                                    for tool_call in last_message.tool_calls:
                                        tool_name = tool_call.get("name", "unknown")
                                        tool_calls_made.append(tool_name)
                                        session.record_tool_call(tool_name)
                                
                                # Check for final AI response
                                if hasattr(last_message, "content") and last_message.content:
                                    if not hasattr(last_message, "tool_calls") or not last_message.tool_calls:
                                        final_response = last_message.content
                    
                    # Show tool calls if any were made
                    if tool_calls_made:
                        tool_list = ", ".join(set(tool_calls_made))
                        console.print(f"[dim]🔧 Used tools: {tool_list}[/dim]")
                    
                    # Display the response
                    if final_response:
                        response = final_response
                        print_assistant_message(response)
                    else:
                        response = "I'm processing your request..."
                        print_assistant_message(response)
                    
                except Exception as e:
                    print_error(f"Agent error: {str(e)}")
                    response = f"[Echo mode] You said: {user_input}"
                    print_assistant_message(response)
            else:
                # Fallback to echo mode
                response = f"[Echo mode] You said: {user_input}"
                print_assistant_message(response)
            
            # Add assistant message to history
            session.add_message("assistant", response)
            
            # Save session after each interaction
            session_manager.save_session(session)
            
            print_divider()
            
        except KeyboardInterrupt:
            console.print("\n")
            print_system_message("Use 'exit' to quit properly.")
            continue
        except EOFError:
            console.print("\n")
            break
        except Exception as e:
            print_error(f"An error occurred: {str(e)}")
            continue


@app.command()
def start(
    session_id: Optional[str] = typer.Option(
        None,
        "--session",
        "-s",
        help="Resume a previous session by ID"
    ),
    new: bool = typer.Option(
        False,
        "--new",
        "-n",
        help="Force start a new session"
    ),
    no_agent: bool = typer.Option(
        False,
        "--no-agent",
        help="Disable AI agent (use echo mode)"
    )
):
    """
    Start the Job Portal AI Assistant CLI.
    """
    session_manager = SessionManager()
    
    # Display welcome screen
    print_welcome()
    
    # Handle session
    if new or not session_id:
        # Create new session
        session_id = str(uuid.uuid4())
        session = SessionState(session_id=session_id)
        print_system_message(f"Session ID: {session_id}")
        
        # Get user type
        print_user_type_selection()
        user_type = get_user_type_choice()
        session.set_user_type(user_type)
        
        print_divider()
        print_system_message("Great! How can I help you today?")
        print_system_message("(Type 'help' for available commands)")
        print_divider()
    else:
        # Try to resume session
        session = session_manager.load_session(session_id)
        if session:
            print_system_message(f"Resuming session: {session_id}")
        else:
            print_error(f"Session '{session_id}' not found. Starting new session.")
            session_id = str(uuid.uuid4())
            session = SessionState(session_id=session_id)
            print_system_message(f"New session ID: {session_id}")
            
            # Get user type
            print_user_type_selection()
            user_type = get_user_type_choice()
            session.set_user_type(user_type)
        
        print_divider()
    
    # Save initial session
    session_manager.save_session(session)
    
    # Run conversation loop
    run_conversation_loop(session, session_manager, use_agent=not no_agent)


@app.command()
def list_sessions():
    """List all available sessions."""
    session_manager = SessionManager()
    sessions = session_manager.list_sessions()
    
    if not sessions:
        print_system_message("No saved sessions found.")
        return
    
    console.print("\n[bold cyan]Available Sessions:[/bold cyan]")
    for session_id in sessions:
        session = session_manager.load_session(session_id)
        if session:
            user_type = session.user_type or "Not set"
            msg_count = len(session.conversation_history)
            console.print(f"  • {session_id}")
            console.print(f"    Type: {user_type} | Messages: {msg_count}")
            console.print(f"    Created: {session.created_at}")
    console.print()


@app.command()
def delete_session(session_id: str):
    """Delete a session by ID."""
    session_manager = SessionManager()
    
    if session_id not in session_manager.list_sessions():
        print_error(f"Session '{session_id}' not found.")
        return
    
    session_manager.delete_session(session_id)
    print_system_message(f"Session '{session_id}' deleted.")


def main():
    """Main entry point."""
    app()


if __name__ == "__main__":
    main()
