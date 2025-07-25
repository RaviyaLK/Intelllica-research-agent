from fastapi import APIRouter, HTTPException
from services.schemas import ResearchRequest, ResearchResponse
from services.agent_engine import run_research_pipeline

router = APIRouter(prefix="/api/v1")

@router.get("/health")
async def health_check():
    return {"status": "ok"}

@router.post("/research", response_model=ResearchResponse)
async def research_topic(request: ResearchRequest):
    try:
        report = run_research_pipeline(request.topic)
        return ResearchResponse(topic=request.topic, report=report)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
