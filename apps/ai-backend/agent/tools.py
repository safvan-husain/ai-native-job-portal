from typing import List
import logging
from langchain_core.tools import tool
from models import Candidate

logger = logging.getLogger(__name__)

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
        # Log the filter being used
        filter_query = {"keywords": {"$all": keywords}}
        logger.info(f"[DB_FILTER] filter_candidates - Filter: {filter_query}")
        logger.info(f"[DB_FILTER] filter_candidates - Keywords count: {len(keywords)}, Keywords: {keywords}")
        
        print(f"DEBUG: Tool filter_candidates called with keywords: {keywords}")
        # We use $all to ensure the candidate has all the specified keywords
        candidates = await Candidate.find(filter_query).to_list()
        
        logger.info(f"[DB_FILTER] filter_candidates - Results: {len(candidates)} candidates found")
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
