from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.core.database import get_db
from app.models.trace import Trace, Span
from app.models.project import Project
from app.schemas.trace import Trace as TraceSchema, TraceCreate, SpanCreate
import uuid

router = APIRouter()

@router.post("/", response_model=TraceSchema)
def create_trace(
    *,
    db: Session = Depends(get_db),
    trace_in: TraceCreate,
    project: Project = Depends(deps.get_project_by_api_key),
) -> Any:
    # Create the trace
    db_trace = Trace(
        id=trace_in.id,
        project_id=project.id,
        model=trace_in.model,
        provider=trace_in.provider,
        input=trace_in.input,
        output=trace_in.output,
        latency=trace_in.latency,
        input_tokens=trace_in.input_tokens,
        output_tokens=trace_in.output_tokens,
        total_tokens=trace_in.total_tokens,
        estimated_cost=trace_in.estimated_cost,
        status=trace_in.status,
        error=trace_in.error,
        meta_data=trace_in.meta_data,
    )
    db.add(db_trace)
    
    # Create spans if provided
    for span_in in trace_in.spans:
        db_span = Span(
            id=span_in.id,
            trace_id=db_trace.id,
            parent_id=span_in.parent_id,
            name=span_in.name,
            span_type=span_in.span_type,
            start_time=span_in.start_time,
            end_time=span_in.end_time,
            input=span_in.input,
            output=span_in.output,
            meta_data=span_in.meta_data,
        )
        db.add(db_span)
        
    db.commit()
    db.refresh(db_trace)
    return db_trace

@router.get("/", response_model=List[TraceSchema])
def read_traces(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    project: Project = Depends(deps.get_project_by_api_key),
) -> Any:
    traces = db.query(Trace).filter(Trace.project_id == project.id).offset(skip).limit(limit).all()
    return traces

@router.get("/{trace_id}", response_model=TraceSchema)
def read_trace(
    *,
    db: Session = Depends(get_db),
    trace_id: str,
    project: Project = Depends(deps.get_project_by_api_key),
) -> Any:
    trace = db.query(Trace).filter(Trace.id == trace_id, Trace.project_id == project.id).first()
    if not trace:
        raise HTTPException(status_code=404, detail="Trace not found")
    return trace
