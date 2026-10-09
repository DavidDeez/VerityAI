import uuid
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List

class Span:
    def __init__(self, name: str, span_type: str = "generic"):
        self.id = str(uuid.uuid4())
        self.name = name
        self.span_type = span_type
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None
        self.input: Optional[str] = None
        self.output: Optional[str] = None
        self.meta_data: Dict[str, Any] = {}
        self.parent_id: Optional[str] = None

    def start(self):
        self.start_time = datetime.now(timezone.utc)
        return self

    def finish(self, output: Optional[str] = None):
        if output:
            self.output = output
        self.end_time = datetime.now(timezone.utc)
        return self

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "span_type": self.span_type,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "input": self.input,
            "output": self.output,
            "meta_data": self.meta_data,
            "parent_id": self.parent_id
        }

class Trace:
    def __init__(self, client, model: str, provider: str = "unknown", input: str = ""):
        self.client = client
        self.id = str(uuid.uuid4())
        self.model = model
        self.provider = provider
        self.input = input
        self.output: Optional[str] = None
        self.latency: Optional[float] = None
        self.input_tokens: Optional[int] = None
        self.output_tokens: Optional[int] = None
        self.total_tokens: Optional[int] = None
        self.estimated_cost: Optional[float] = None
        self.status: str = "started"
        self.error: Optional[str] = None
        self.meta_data: Dict[str, Any] = {}
        
        self.spans: List[Span] = []
        
        # Start timer
        self._start_time = datetime.now(timezone.utc)

    def log_output(self, output: str, input_tokens: int = 0, output_tokens: int = 0, cost: float = 0.0):
        self.output = output
        self.input_tokens = input_tokens
        self.output_tokens = output_tokens
        self.total_tokens = input_tokens + output_tokens
        self.estimated_cost = cost
        
    def add_span(self, span: Span):
        self.spans.append(span)

    def finish(self, status: str = "success", error: Optional[str] = None):
        self.status = status
        self.error = error
        
        end_time = datetime.now(timezone.utc)
        self.latency = (end_time - self._start_time).total_seconds()
        
        # Send trace to backend
        self.client._send_trace(self)
        
    def to_dict(self):
        return {
            "id": self.id,
            "model": self.model,
            "provider": self.provider,
            "input": self.input,
            "output": self.output,
            "latency": self.latency,
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
            "total_tokens": self.total_tokens,
            "estimated_cost": self.estimated_cost,
            "status": self.status,
            "error": self.error,
            "meta_data": self.meta_data,
            "spans": [s.to_dict() for s in self.spans]
        }
