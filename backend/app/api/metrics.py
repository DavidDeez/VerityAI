from typing import Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.api import deps
from app.core.database import get_db
from app.models.trace import Trace
from app.models.project import Project

router = APIRouter()

@router.get("/")
def get_dashboard_metrics(
    db: Session = Depends(get_db),
    project: Project = Depends(deps.get_project_by_api_key),
) -> Any:
    """Get aggregated metrics for the dashboard."""
    
    total_requests = db.query(Trace).filter(Trace.project_id == project.id).count()
    
    success_requests = db.query(Trace).filter(Trace.project_id == project.id, Trace.status == 'success').count()
    success_rate = (success_requests / total_requests * 100) if total_requests > 0 else 0
    
    avg_latency = db.query(func.avg(Trace.latency)).filter(Trace.project_id == project.id).scalar() or 0
    
    total_tokens = db.query(func.sum(Trace.total_tokens)).filter(Trace.project_id == project.id).scalar() or 0
    total_cost = db.query(func.sum(Trace.estimated_cost)).filter(Trace.project_id == project.id).scalar() or 0

    return {
        "reliability_score": 92.5, # Mock composite score
        "total_requests": total_requests,
        "success_rate": round(success_rate, 2),
        "average_latency": round(avg_latency, 2),
        "total_tokens": total_tokens,
        "estimated_cost": round(total_cost, 4),
        "hallucination_rate": 3.2, # Mock
        "evaluation_pass_rate": 94.1 # Mock
    }
