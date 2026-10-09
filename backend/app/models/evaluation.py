from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, JSON, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class Dataset(Base):
    __tablename__ = "datasets"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), index=True, nullable=False)
    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    project = relationship("Project", backref="datasets")
    cases = relationship("DatasetCase", backref="dataset", cascade="all, delete-orphan")

class DatasetCase(Base):
    __tablename__ = "dataset_cases"

    id = Column(Integer, primary_key=True, index=True)
    dataset_id = Column(Integer, ForeignKey("datasets.id"), index=True, nullable=False)
    input_data = Column(Text, nullable=False)
    expected_output = Column(Text, nullable=True)
    context = Column(JSON, nullable=True) # E.g., for RAG tests
    meta_data = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class EvaluationRun(Base):
    __tablename__ = "evaluation_runs"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), index=True, nullable=False)
    dataset_id = Column(Integer, ForeignKey("datasets.id"), index=True, nullable=True)
    name = Column(String, nullable=False)
    status = Column(String, default="running") # running, completed, failed
    model_tested = Column(String, nullable=True)
    metrics_config = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    
    project = relationship("Project", backref="evaluation_runs")
    dataset = relationship("Dataset")
    results = relationship("EvaluationResult", backref="run", cascade="all, delete-orphan")

class EvaluationResult(Base):
    __tablename__ = "evaluation_results"

    id = Column(Integer, primary_key=True, index=True)
    run_id = Column(Integer, ForeignKey("evaluation_runs.id"), index=True, nullable=False)
    case_id = Column(Integer, ForeignKey("dataset_cases.id"), index=True, nullable=True)
    trace_id = Column(String, ForeignKey("traces.id"), index=True, nullable=True)
    
    output = Column(Text, nullable=True)
    scores = Column(JSON, nullable=False) # e.g. {"accuracy": 0.9, "hallucination": 0.1}
    failure_reason = Column(String, nullable=True) # e.g., 'HALLUCINATION', 'TIMEOUT'
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    case = relationship("DatasetCase")
    trace = relationship("Trace")
