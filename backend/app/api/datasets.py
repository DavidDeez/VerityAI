from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.core.database import get_db
from app.models.evaluation import Dataset, DatasetCase
from app.models.project import Project
from app.schemas.evaluation import Dataset as DatasetSchema, DatasetCreate

router = APIRouter()

@router.post("/", response_model=DatasetSchema)
def create_dataset(
    *,
    db: Session = Depends(get_db),
    dataset_in: DatasetCreate,
    project: Project = Depends(deps.get_project_by_api_key),
) -> Any:
    db_dataset = Dataset(
        project_id=project.id,
        name=dataset_in.name,
        description=dataset_in.description,
    )
    db.add(db_dataset)
    db.flush()
    
    for case_in in dataset_in.cases:
        db_case = DatasetCase(
            dataset_id=db_dataset.id,
            input_data=case_in.input_data,
            expected_output=case_in.expected_output,
            context=case_in.context,
            meta_data=case_in.meta_data
        )
        db.add(db_case)
        
    db.commit()
    db.refresh(db_dataset)
    return db_dataset

@router.get("/", response_model=List[DatasetSchema])
def read_datasets(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    project: Project = Depends(deps.get_project_by_api_key),
) -> Any:
    datasets = db.query(Dataset).filter(Dataset.project_id == project.id).offset(skip).limit(limit).all()
    return datasets
