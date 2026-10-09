from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, JSON, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class RegressionRule(Base):
    __tablename__ = "regression_rules"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), index=True, nullable=False)
    metric_name = Column(String, nullable=False) # e.g. 'accuracy', 'latency', 'hallucination'
    operator = Column(String, nullable=False) # '>=', '<='
    threshold = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class SecurityTest(Base):
    __tablename__ = "security_tests"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), index=True, nullable=False)
    name = Column(String, nullable=False)
    status = Column(String, default="running")
    overall_score = Column(Float, nullable=True)
    results = Column(JSON, nullable=True) # breakdown by category: prompt injection, data leakage
    created_at = Column(DateTime(timezone=True), server_default=func.now())
