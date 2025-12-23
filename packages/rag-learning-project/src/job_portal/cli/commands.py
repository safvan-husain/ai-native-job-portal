"""
Command handlers for the CLI.
"""

from typing import Optional
from .ui import (
    print_help,
    clear_screen,
    print_info,
    print_system_message,
    console
)
from .session import SessionState


class CommandHandler:
    """Handles special commands in the CLI."""
    
    COMMANDS = {
        "help": "Show help information",
        "clear": "Clear the screen",
        "exit": "Exit the application",
        "quit": "Exit the application",
        "bye": "Exit the application",
        "new": "Start a new conversation",
        "history": "Show conversation history"
    }
    
    def __init__(self, session: SessionState):
        self.session = session
    
    def is_command(self, text: str) -> bool:
        """Check if text is a command."""
        return text.lower().strip() in self.COMMANDS
    
    def handle_command(self, text: str) -> Optional[str]:
        """
        Handle a command.
        
        Returns:
            - None if command was handled
            - "exit" if user wants to exit
            - The original text if not a command
        """
        command = text.lower().strip()
        
        if command not in self.COMMANDS:
            return text
        
        if command == "help":
            print_help()
            return None
        
        elif command == "clear":
            clear_screen()
            return None
        
        elif command in ["exit", "quit", "bye"]:
            print_system_message("Goodbye! 👋")
            return "exit"
        
        elif command == "new":
            print_info("Starting a new conversation...")
            self.session.conversation_history.clear()
            self.session.selected_items.clear()
            self.session.search_results.clear()
            print_system_message("Conversation cleared. How can I help you?")
            return None
        
        elif command == "history":
            self._show_history()
            return None
        
        return text
    
    def _show_history(self):
        """Display conversation history."""
        if not self.session.conversation_history:
            print_info("No conversation history yet.")
            return
        
        console.print("\n[bold cyan]Conversation History:[/bold cyan]")
        for i, msg in enumerate(self.session.conversation_history, 1):
            role = msg.get("role", "unknown")
            content = msg.get("content", "")
            timestamp = msg.get("timestamp", "")
            
            if role == "user":
                console.print(f"  [blue]{i}. You:[/blue] {content}")
            elif role == "assistant":
                console.print(f"  [green]{i}. Assistant:[/green] {content}")
            else:
                console.print(f"  [dim]{i}. {role}:[/dim] {content}")
        
        console.print()
