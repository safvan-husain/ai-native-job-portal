from typing import List
from langchain_core.tools import tool
from models import Candidate

@tool
async def filter_candidates(keywords: List[str]) -> str:
    """
    Filter candidates from the database that match ALL of the provided keywords.
    
    Args:
        keywords: A list of exact keywords to filter by (e.g., ["Python", "Machine Learning"]).
        
    Returns:
        A formatted string listing the matching candidates or a message if none found.
    """
    try:
        print(f"DEBUG: Tool filter_candidates called with keywords: {keywords}")
        # We use $all to ensure the candidate has all the specified keywords
        candidates = await Candidate.find({"keywords": {"$all": keywords}}).to_list()
        print(f"DEBUG: Found {len(candidates)} candidates.")
        
        if not candidates:
            return f"No candidates found matching all keywords: {', '.join(keywords)}"
        
        output = f"Found {len(candidates)} candidate(s) matching {', '.join(keywords)}:\n\n"
        for i, c in enumerate(candidates, 1):
            output += f"{i}. 👤 {c.name}\n"
            output += f"   🛠️  Skills: {', '.join(c.keywords)}\n"
            output += f"   📝 {c.description}\n\n"
            
        return output
    except Exception as e:
        return f"Error filtering candidates: {str(e)}"
