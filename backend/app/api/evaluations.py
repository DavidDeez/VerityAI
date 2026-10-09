from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app.api import deps
from app.core.database import get_db
from app.models.evaluation import EvaluationRun, Dataset
from app.models.project import Project
from app.schemas.evaluation import EvaluationRun as EvaluationRunSchema, EvaluationRunCreate
from app.services.evaluator import run_evaluation_task

router = APIRouter()

@router.post("/", response_model=EvaluationRunSchema)
def create_evaluation(
    *,
    db: Session = Depends(get_db),
    eval_in: EvaluationRunCreate,
    background_tasks: BackgroundTasks,
    project: Project = Depends(deps.get_project_by_api_key),
) -> Any:
    # Verify dataset exists
    if eval_in.dataset_id:
        dataset = db.query(Dataset).filter(Dataset.id == eval_in.dataset_id, Dataset.project_id == project.id).first()
        if not dataset:
            raise HTTPException(status_code=404, detail="Dataset not found")
            
    db_run = EvaluationRun(
        project_id=project.id,
        dataset_id=eval_in.dataset_id,
        name=eval_in.name,
        model_tested=eval_in.model_tested,
        metrics_config=eval_in.metrics_config,
        status="running"
    )
    db.add(db_run)
    db.commit()
    db.refresh(db_run)
    
    # Run evaluation in background task (could use Celery in prod)
    background_tasks.add_task(run_evaluation_task, db_run.id)
    
    return db_run

@router.get("/{run_id}", response_model=EvaluationRunSchema)
def read_evaluation(
    *,
    db: Session = Depends(get_db),
    run_id: int,
    project: Project = Depends(deps.get_project_by_api_key),
) -> Any:
    run = db.query(EvaluationRun).filter(EvaluationRun.id == run_id, EvaluationRun.project_id == project.id).first()
    if not run:
        raise HTTPException(status_code=404, detail="Evaluation not found")
    return run
