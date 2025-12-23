"""
Session management for CLI conversations.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, asdict, field


@dataclass
class SessionState:
    """Manages the state of a CLI session."""
    
    session_id: str
    user_type: Optional[str] = None  # "job_seeker" or "company"
    conversation_history: List[Dict[str, str]] = field(default_factory=list)
    selected_items: List[str] = field(default_factory=list)
    search_results: List[Dict[str, Any]] = field(default_factory=list)
    comparison_mode: bool = False
    last_tool_call: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def add_message(self, role: str, content: str):
        """Add a message to conversation history."""
        self.conversation_history.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
        self.updated_at = datetime.now().isoformat()
    
    def set_user_type(self, user_type: str):
        """Set the user type (job_seeker or company)."""
        if user_type not in ["job_seeker", "company"]:
            raise ValueError("user_type must be 'job_seeker' or 'company'")
        self.user_type = user_type
        self.updated_at = datetime.now().isoformat()
    
    def add_selected_item(self, item_id: str):
        """Add an item to the selection list."""
        if item_id not in self.selected_items:
            self.selected_items.append(item_id)
            self.updated_at = datetime.now().isoformat()
    
    def clear_selected_items(self):
        """Clear all selected items."""
        self.selected_items.clear()
        self.updated_at = datetime.now().isoformat()
    
    def set_comparison_mode(self, enabled: bool):
        """Enable or disable comparison mode."""
        self.comparison_mode = enabled
        self.updated_at = datetime.now().isoformat()
    
    def record_tool_call(self, tool_name: str):
        """Record the last tool call made."""
        self.last_tool_call = tool_name
        self.updated_at = datetime.now().isoformat()
    
    def add_search_results(self, results: List[Dict[str, Any]]):
        """Store search results for later reference."""
        self.search_results = results
        self.updated_at = datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert session to dictionary."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SessionState":
        """Create session from dictionary."""
        return cls(**data)


class SessionManager:
    """Manages session persistence."""
    
    def __init__(self, sessions_dir: str = ".sessions"):
        self.sessions_dir = Path(sessions_dir)
        self.sessions_dir.mkdir(exist_ok=True)
    
    def save_session(self, session: SessionState):
        """Save session to file."""
        session_file = self.sessions_dir / f"{session.session_id}.json"
        with open(session_file, "w", encoding="utf-8") as f:
            json.dump(session.to_dict(), f, indent=2, ensure_ascii=False)
    
    def load_session(self, session_id: str) -> Optional[SessionState]:
        """Load session from file."""
        session_file = self.sessions_dir / f"{session_id}.json"
        if not session_file.exists():
            return None
        
        with open(session_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            return SessionState.from_dict(data)
    
    def list_sessions(self) -> List[str]:
        """List all available session IDs."""
        return [f.stem for f in self.sessions_dir.glob("*.json")]
    
    def delete_session(self, session_id: str):
        """Delete a session file."""
        session_file = self.sessions_dir / f"{session_id}.json"
        if session_file.exists():
            session_file.unlink()
