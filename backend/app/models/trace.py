from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class Trace(Base):
    __tablename__ = "traces"

    id = Column(String, primary_key=True, index=True) # UUID string
    project_id = Column(Integer, ForeignKey("projects.id"), index=True, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    model = Column(String, index=True)
    provider = Column(String, index=True)
    
    input = Column(String)
    output = Column(String)
    
    latency = Column(Float)
    input_tokens = Column(Integer)
    output_tokens = Column(Integer)
    total_tokens = Column(Integer)
    estimated_cost = Column(Float)
    
    status = Column(String, index=True) # e.g. 'success', 'error'
    error = Column(String)
    
    meta_data = Column(JSON) # Storing arbitrary metadata

    project = relationship("Project", backref="traces")
    spans = relationship("Span", backref="trace")

class Span(Base):
    __tablename__ = "spans"

    id = Column(String, primary_key=True, index=True) # UUID string
    trace_id = Column(String, ForeignKey("traces.id"), index=True, nullable=False)
    parent_id = Column(String, ForeignKey("spans.id"), index=True, nullable=True)
    
    name = Column(String, index=True)
    span_type = Column(String) # e.g. 'llm', 'tool', 'retrieval'
    
    start_time = Column(DateTime(timezone=True))
    end_time = Column(DateTime(timezone=True))
    
    input = Column(String)
    output = Column(String)
    
    meta_data = Column(JSON)
