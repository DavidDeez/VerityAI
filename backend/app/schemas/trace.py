from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any, List

class SpanBase(BaseModel):
    name: str
    span_type: str
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    input: Optional[str] = None
    output: Optional[str] = None
    meta_data: Optional[Dict[str, Any]] = None
    parent_id: Optional[str] = None

class SpanCreate(SpanBase):
    id: str

class Span(SpanBase):
    id: str
    trace_id: str

    class Config:
        from_attributes = True

class TraceBase(BaseModel):
    model: Optional[str] = None
    provider: Optional[str] = None
    input: Optional[str] = None
    output: Optional[str] = None
    latency: Optional[float] = None
    input_tokens: Optional[int] = None
    output_tokens: Optional[int] = None
    total_tokens: Optional[int] = None
    estimated_cost: Optional[float] = None
    status: Optional[str] = None
    error: Optional[str] = None
    meta_data: Optional[Dict[str, Any]] = None

class TraceCreate(TraceBase):
    id: str
    spans: Optional[List[SpanCreate]] = []

class Trace(TraceBase):
    id: str
    project_id: int
    timestamp: datetime
    spans: List[Span] = []

    class Config:
        from_attributes = True
