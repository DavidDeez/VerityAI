from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any

class RegressionRuleBase(BaseModel):
    metric_name: str
    operator: str
    threshold: float

class RegressionRuleCreate(RegressionRuleBase):
    pass

class RegressionRule(RegressionRuleBase):
    id: int
    project_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class SecurityTestBase(BaseModel):
    name: str

class SecurityTestCreate(SecurityTestBase):
    pass

class SecurityTest(SecurityTestBase):
    id: int
    project_id: int
    status: str
    overall_score: Optional[float] = None
    results: Optional[Dict[str, Any]] = None
    created_at: datetime

    class Config:
        from_attributes = True
