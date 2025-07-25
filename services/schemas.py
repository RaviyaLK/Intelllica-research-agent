from pydantic import BaseModel
from typing import List, Optional
class ResearchRequest(BaseModel):
    topic: str

class ResearchResponse(BaseModel):
    topic: str
    report: str
    
class StateSchema(BaseModel):
    topic: str
    search_results: Optional[List[dict]] = []
    summary: Optional[str] = ""
    citations: Optional[List[str]] = []
    report: Optional[str] = ""