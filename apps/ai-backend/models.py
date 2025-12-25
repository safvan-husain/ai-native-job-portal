from typing import List
from beanie import Document
from pydantic import Field

class Candidate(Document):
    name: str
    keywords: List[str] = Field(default_factory=list)
    description: str

    class Settings:
        name = "candidates"
