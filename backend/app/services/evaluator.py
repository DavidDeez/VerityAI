import time
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.evaluation import EvaluationRun, EvaluationResult, DatasetCase
from datetime import datetime, timezone
import random

def calculate_exact_match(output: str, expected: str) -> float:
    if not output or not expected:
        return 0.0
    return 1.0 if output.strip().lower() == expected.strip().lower() else 0.0

def calculate_hallucination(output: str, context: list) -> float:
    # A mock metric for hallucination: random between 0 (perfect) and 1 (fully hallucinated)
    # In a real engine, we'd call an LLM judge here.
    return random.uniform(0.0, 0.2)

def run_evaluation_task(run_id: int):
    """
    Background task to process an evaluation run.
    """
    db: Session = SessionLocal()
    try:
        run = db.query(EvaluationRun).filter(EvaluationRun.id == run_id).first()
        if not run or not run.dataset_id:
            return
            
        cases = db.query(DatasetCase).filter(DatasetCase.dataset_id == run.dataset_id).all()
        
        # Simulate LLM interactions and evaluation
        for case in cases:
            # Simulate latency
            time.sleep(0.1)
            
            # Simulated model output
            mock_output = case.expected_output if case.expected_output else "Generated output..."
            
            # Calculate metrics
            scores = {}
            if "exact_match" in (run.metrics_config or {}).get("metrics", ["exact_match"]):
                scores["exact_match"] = calculate_exact_match(mock_output, case.expected_output)
            
            if "hallucination" in (run.metrics_config or {}).get("metrics", ["hallucination"]):
                scores["hallucination"] = calculate_hallucination(mock_output, case.context)
                
            scores["latency"] = random.uniform(0.5, 2.0)
            
            result = EvaluationResult(
                run_id=run.id,
                case_id=case.id,
                output=mock_output,
                scores=scores
            )
            db.add(result)
            
        run.status = "completed"
        run.completed_at = datetime.now(timezone.utc)
        db.commit()
    except Exception as e:
        if run:
            run.status = "failed"
            db.commit()
    finally:
        db.close()
