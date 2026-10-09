from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app.api import deps
from app.core.database import get_db
from app.models.benchmark import RegressionRule, SecurityTest
from app.models.project import Project
from app.schemas.benchmark import RegressionRule as RegressionRuleSchema, RegressionRuleCreate, SecurityTest as SecurityTestSchema, SecurityTestCreate
from app.services.security import run_security_test

router = APIRouter()

@router.post("/regressions", response_model=RegressionRuleSchema)
def create_regression_rule(
    *,
    db: Session = Depends(get_db),
    rule_in: RegressionRuleCreate,
    project: Project = Depends(deps.get_project_by_api_key),
) -> Any:
    rule = RegressionRule(
        project_id=project.id,
        metric_name=rule_in.metric_name,
        operator=rule_in.operator,
        threshold=rule_in.threshold,
    )
    db.add(rule)
    db.commit()
    db.refresh(rule)
    return rule

@router.get("/regressions", response_model=List[RegressionRuleSchema])
def read_regression_rules(
    db: Session = Depends(get_db),
    project: Project = Depends(deps.get_project_by_api_key),
) -> Any:
    return db.query(RegressionRule).filter(RegressionRule.project_id == project.id).all()

@router.post("/security-tests", response_model=SecurityTestSchema)
def create_security_test(
    *,
    db: Session = Depends(get_db),
    test_in: SecurityTestCreate,
    background_tasks: BackgroundTasks,
    project: Project = Depends(deps.get_project_by_api_key),
) -> Any:
    test = SecurityTest(
        project_id=project.id,
        name=test_in.name,
        status="running"
    )
    db.add(test)
    db.commit()
    db.refresh(test)
    
    background_tasks.add_task(run_security_test, test.id)
    
    return test

@router.get("/security-tests/{test_id}", response_model=SecurityTestSchema)
def read_security_test(
    *,
    db: Session = Depends(get_db),
    test_id: int,
    project: Project = Depends(deps.get_project_by_api_key),
) -> Any:
    test = db.query(SecurityTest).filter(SecurityTest.id == test_id, SecurityTest.project_id == project.id).first()
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")
    return test
