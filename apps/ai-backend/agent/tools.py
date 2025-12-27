from typing import List, Literal
import logging
from langchain_core.tools import tool
from models import Candidate

logger = logging.getLogger(__name__)

@tool
async def filter_candidates(
    keywords: List[str], 
    match_mode: Literal["any", "all"] = "any"
) -> str:
    """
    Filter candidates from the database based on keywords.
    
    IMPORTANT: Use SPECIFIC keywords from the available list. For generic terms like 
    "web developer", use specific skills like ["React", "Node.js", "JavaScript"] instead.
    
    Args:
        keywords: A list of exact keywords to filter by (e.g., ["Python", "React", "Node.js"]).
                 MUST use keywords that exist in the database. Use specific skills, not generic roles.
        match_mode: 
            - "any" (default): Returns candidates matching ANY of the keywords (OR logic).
                              Use this for broader searches (e.g., find web developers = any of React, Node.js, JavaScript).
            - "all": Returns candidates matching ALL keywords (AND logic).
                     Use this when you need candidates with all specified skills.
        
    Returns:
        A formatted string listing the matching candidates or a message if none found.
    """
    try:
        # Build filter query based on match mode
        if match_mode == "all":
            # Match ALL keywords (AND logic)
            filter_query = {"keywords": {"$all": keywords}}
            match_description = "all"
        else:
            # Match ANY keyword (OR logic)
            filter_query = {"keywords": {"$in": keywords}}
            match_description = "any"
        
        logger.info(f"[DB_FILTER] filter_candidates - Match mode: {match_mode}")
        logger.info(f"[DB_FILTER] filter_candidates - Filter: {filter_query}")
        logger.info(f"[DB_FILTER] filter_candidates - Keywords count: {len(keywords)}, Keywords: {keywords}")
        
        print(f"DEBUG: Tool filter_candidates called with keywords: {keywords}, match_mode: {match_mode}")
        candidates = await Candidate.find(filter_query).to_list()
        
        logger.info(f"[DB_FILTER] filter_candidates - Results: {len(candidates)} candidates found")
        print(f"DEBUG: Found {len(candidates)} candidates.")
        
        if not candidates:
            return f"No candidates found matching {match_description} of the keywords: {', '.join(keywords)}"
        
        output = f"Found {len(candidates)} candidate(s) matching {match_description} of: {', '.join(keywords)}\n\n"
        for i, c in enumerate(candidates, 1):
            output += f"{i}. 👤 {c.name}\n"
            output += f"   🛠️  Skills: {', '.join(c.keywords)}\n"
            output += f"   📝 {c.description}\n\n"
            
        return output
    except Exception as e:
        logger.error(f"[DB_FILTER] filter_candidates - Error: {str(e)}")
        return f"Error filtering candidates: {str(e)}"
