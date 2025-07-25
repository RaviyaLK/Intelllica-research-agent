from fastapi import APIRouter, HTTPException
from services.schemas import ResearchRequest, ResearchResponse
from services.agent_engine import run_research_pipeline
import os
from fastapi.responses import FileResponse
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
@router.get("/download-report")
def download_report(file_path: str):
    if os.path.exists(file_path):
        return FileResponse(path=file_path, filename=os.path.basename(file_path), media_type='application/pdf')
    return {"error": "File not found"}