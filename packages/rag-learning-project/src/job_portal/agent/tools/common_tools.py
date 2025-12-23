"""Common utility tools shared across job seekers and companies."""
from typing import List, Dict, Any
from langchain_core.tools import tool


@tool
def format_search_results(results: str, result_type: str = "job") -> str:
    """
    Format search results in a more readable way.
    
    This is a utility tool for formatting raw search results.
    
    Args:
        results: Raw search results as string
        result_type: Type of results ("job" or "candidate")
        
    Returns:
        Formatted results string
    """
    # This is a simple pass-through for now
    # Can be enhanced with more sophisticated formatting
    return results


def _format_score(score: float) -> str:
    """Format similarity score as percentage."""
    return f"{score * 100:.1f}%"


def _truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text to max length with ellipsis."""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."
