from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any, List

class DatasetCaseBase(BaseModel):
    input_data: str
    expected_output: Optional[str] = None
    context: Optional[List[Any]] = None
    meta_data: Optional[Dict[str, Any]] = None

class DatasetCaseCreate(DatasetCaseBase):
    pass

class DatasetCase(DatasetCaseBase):
    id: int
    dataset_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class DatasetBase(BaseModel):
    name: str
    description: Optional[str] = None

class DatasetCreate(DatasetBase):
    cases: Optional[List[DatasetCaseCreate]] = []

class Dataset(DatasetBase):
    id: int
    project_id: int
    created_at: datetime
    cases: List[DatasetCase] = []

    class Config:
        from_attributes = True

class EvaluationResultBase(BaseModel):
    case_id: Optional[int] = None
    trace_id: Optional[str] = None
    output: Optional[str] = None
    scores: Dict[str, float]
    failure_reason: Optional[str] = None

class EvaluationResultCreate(EvaluationResultBase):
    pass

class EvaluationResult(EvaluationResultBase):
    id: int
    run_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class EvaluationRunBase(BaseModel):
    dataset_id: Optional[int] = None
    name: str
    model_tested: Optional[str] = None
    metrics_config: Optional[Dict[str, Any]] = None

class EvaluationRunCreate(EvaluationRunBase):
    pass

class EvaluationRun(EvaluationRunBase):
    id: int
    project_id: int
    status: str
    created_at: datetime
    completed_at: Optional[datetime] = None
    results: List[EvaluationResult] = []

    class Config:
        from_attributes = True
