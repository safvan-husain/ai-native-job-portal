"""
Rich UI components for the CLI.
"""

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.markdown import Markdown
from rich import box
from typing import Optional


console = Console()


def print_welcome():
    """Display welcome screen."""
    welcome_text = """
# 🚀 Job Portal AI Assistant

Welcome to the intelligent job portal CLI! I'm here to help you:

**For Job Seekers:**
- Find matching companies and job opportunities
- Get detailed company information
- Compare multiple companies side-by-side

**For Companies:**
- Find qualified candidates
- Review candidate profiles
- Compare candidates for your positions
    """
    
    panel = Panel(
        Markdown(welcome_text),
        title="[bold cyan]Welcome[/bold cyan]",
        border_style="cyan",
        box=box.ROUNDED
    )
    console.print(panel)
    console.print()


def print_user_type_selection():
    """Display user type selection prompt."""
    console.print("[bold yellow]Please select your user type:[/bold yellow]")
    console.print("  [cyan]1.[/cyan] Job Seeker - Looking for opportunities")
    console.print("  [cyan]2.[/cyan] Company - Looking for candidates")
    console.print()


def get_user_type_choice() -> str:
    """Get user type choice from user."""
    while True:
        choice = Prompt.ask(
            "[bold]Your choice[/bold]",
            choices=["1", "2"],
            default="1"
        )
        
        if choice == "1":
            console.print("[green]✓[/green] You selected: [bold]Job Seeker[/bold]")
            return "job_seeker"
        else:
            console.print("[green]✓[/green] You selected: [bold]Company[/bold]")
            return "company"


def print_user_message(message: str):
    """Display user message."""
    console.print(f"[bold blue]You:[/bold blue] {message}")


def print_assistant_message(message: str):
    """Display assistant message."""
    console.print(f"[bold green]Assistant:[/bold green] {message}")


def print_system_message(message: str):
    """Display system message."""
    console.print(f"[dim italic]{message}[/dim italic]")


def print_error(message: str):
    """Display error message."""
    console.print(f"[bold red]Error:[/bold red] {message}")


def print_info(message: str):
    """Display info message."""
    console.print(f"[bold cyan]ℹ[/bold cyan] {message}")


def print_success(message: str):
    """Display success message."""
    console.print(f"[bold green]✓[/bold green] {message}")


def print_divider():
    """Print a visual divider."""
    console.print("─" * console.width, style="dim")


def print_help():
    """Display help information."""
    help_text = """
# Available Commands

- **help** - Show this help message
- **clear** - Clear the screen
- **exit** / **quit** / **bye** - Exit the application
- **new** - Start a new conversation
- **history** - Show conversation history

Just type your questions naturally and I'll help you!
    """
    
    panel = Panel(
        Markdown(help_text),
        title="[bold cyan]Help[/bold cyan]",
        border_style="cyan",
        box=box.ROUNDED
    )
    console.print(panel)


def clear_screen():
    """Clear the console screen."""
    console.clear()


def confirm_action(message: str) -> bool:
    """Ask for user confirmation."""
    return Confirm.ask(message)


def get_input(prompt: str = "You") -> str:
    """Get input from user with custom prompt."""
    return Prompt.ask(f"[bold blue]{prompt}[/bold blue]")
