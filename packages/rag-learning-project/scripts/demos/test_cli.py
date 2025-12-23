"""
Quick test script for the CLI (Phase 1 verification).

This script tests the CLI components without running the interactive loop.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.job_portal.cli.session import SessionState, SessionManager
from src.job_portal.cli.commands import CommandHandler
from src.job_portal.cli.ui import console, print_success, print_error, print_info


def test_session_management():
    """Test session creation and persistence."""
    print_info("Testing session management...")
    
    # Create session
    session = SessionState(session_id="test-session-123")
    session.set_user_type("job_seeker")
    session.add_message("user", "Hello")
    session.add_message("assistant", "Hi there!")
    
    # Save session
    manager = SessionManager(sessions_dir=".test_sessions")
    manager.save_session(session)
    
    # Load session
    loaded_session = manager.load_session("test-session-123")
    
    if loaded_session:
        assert loaded_session.session_id == "test-session-123"
        assert loaded_session.user_type == "job_seeker"
        assert len(loaded_session.conversation_history) == 2
        print_success("✓ Session management works!")
    else:
        print_error("✗ Failed to load session")
        return False
    
    # Cleanup
    manager.delete_session("test-session-123")
    Path(".test_sessions").rmdir()
    
    return True


def test_command_handler():
    """Test command handling."""
    print_info("Testing command handler...")
    
    session = SessionState(session_id="test-cmd")
    handler = CommandHandler(session)
    
    # Test command detection
    assert handler.is_command("help")
    assert handler.is_command("HELP")
    assert handler.is_command("exit")
    assert not handler.is_command("hello world")
    
    # Test command handling
    result = handler.handle_command("help")
    assert result is None  # Command was handled
    
    result = handler.handle_command("exit")
    assert result == "exit"
    
    result = handler.handle_command("hello")
    assert result == "hello"  # Not a command, return original
    
    print_success("✓ Command handler works!")
    return True


def test_session_state():
    """Test session state operations."""
    print_info("Testing session state...")
    
    session = SessionState(session_id="test-state")
    
    # Test user type
    session.set_user_type("company")
    assert session.user_type == "company"
    
    # Test messages
    session.add_message("user", "Test message")
    assert len(session.conversation_history) == 1
    assert session.conversation_history[0]["role"] == "user"
    
    # Test selected items
    session.add_selected_item("item-1")
    session.add_selected_item("item-2")
    assert len(session.selected_items) == 2
    
    session.clear_selected_items()
    assert len(session.selected_items) == 0
    
    # Test serialization
    data = session.to_dict()
    restored = SessionState.from_dict(data)
    assert restored.session_id == session.session_id
    assert restored.user_type == session.user_type
    
    print_success("✓ Session state works!")
    return True


def main():
    """Run all tests."""
    console.print("\n[bold cyan]Testing CLI Components (Phase 1)[/bold cyan]\n")
    
    tests = [
        ("Session State", test_session_state),
        ("Session Management", test_session_management),
        ("Command Handler", test_command_handler),
    ]
    
    passed = 0
    failed = 0
    
    for name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print_error(f"✗ {name} failed: {str(e)}")
            failed += 1
    
    console.print()
    if failed == 0:
        print_success(f"All {passed} tests passed! ✓")
        console.print("\n[bold green]Phase 1.1 and 1.2 are complete![/bold green]")
        console.print("\nYou can now run the CLI with:")
        console.print("  [cyan]python -m src.job_portal.cli.main start[/cyan]")
    else:
        print_error(f"{failed} test(s) failed, {passed} passed")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
