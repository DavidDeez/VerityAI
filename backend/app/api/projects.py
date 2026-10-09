from typing import Any, List
import secrets
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.core.database import get_db
from app.models.project import Project, ApiKey
from app.models.user import User
from app.schemas.project import Project as ProjectSchema, ProjectCreate, ApiKey as ApiKeySchema

router = APIRouter()

@router.get("/", response_model=List[ProjectSchema])
def read_projects(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    projects = db.query(Project).filter(Project.owner_id == current_user.id).offset(skip).limit(limit).all()
    return projects

@router.post("/", response_model=ProjectSchema)
def create_project(
    *,
    db: Session = Depends(get_db),
    project_in: ProjectCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    project = Project(name=project_in.name, owner_id=current_user.id)
    db.add(project)
    db.commit()
    db.refresh(project)
    return project

@router.post("/{project_id}/keys", response_model=ApiKeySchema)
def create_api_key(
    *,
    db: Session = Depends(get_db),
    project_id: int,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    project = db.query(Project).filter(Project.id == project_id, Project.owner_id == current_user.id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Generate a random API key (in a real app, hash this before saving and return the raw key ONCE)
    # For demo purposes we just store a token.
    raw_key = secrets.token_urlsafe(32)
    key_hash = raw_key # Simple mock
    
    api_key = ApiKey(key_hash=key_hash, project_id=project.id)
    db.add(api_key)
    db.commit()
    db.refresh(api_key)
    
    # Returning the key_hash directly just for the test/demo
    return api_key
