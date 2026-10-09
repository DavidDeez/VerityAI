from pydantic import BaseModel
from datetime import datetime

class ProjectBase(BaseModel):
    name: str

class ProjectCreate(ProjectBase):
    pass

class Project(ProjectBase):
    id: int
    owner_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class ApiKeyBase(BaseModel):
    pass

class ApiKeyCreate(ApiKeyBase):
    project_id: int

class ApiKey(ApiKeyBase):
    id: int
    project_id: int
    created_at: datetime
    # We do not return the full key, only its hash or a masked version in a real system.
    # For now, keeping it simple.

    class Config:
        from_attributes = True
