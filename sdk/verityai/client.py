import httpx
from .trace import Trace
from typing import Optional, Any
from functools import wraps

class VerityAI:
    def __init__(self, api_key: str, base_url: str = "http://localhost:8000/api/v1"):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.client = httpx.Client(headers={"Authorization": f"Bearer {self.api_key}"})

    def trace(self, model: str = "unknown", provider: str = "unknown", input: str = "") -> Trace:
        """Create a new trace."""
        return Trace(client=self, model=model, provider=provider, input=input)

    def _send_trace(self, trace: Trace):
        """Internal method to send trace data to the backend."""
        response = self.client.post(f"{self.base_url}/traces/", json=trace.to_dict())
        response.raise_for_status()

    def observe(self, model: str = "unknown", provider: str = "unknown", **kwargs):
        """Decorator to automatically trace a function execution."""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **func_kwargs):
                # Combine args/kwargs for input recording (simplified)
                input_str = f"args: {args}, kwargs: {func_kwargs}"
                t = self.trace(model=model, provider=provider, input=input_str)
                t.meta_data.update(kwargs)
                
                try:
                    result = func(*args, **func_kwargs)
                    t.log_output(output=str(result))
                    t.finish(status="success")
                    return result
                except Exception as e:
                    t.finish(status="error", error=str(e))
                    raise
            return wrapper
        return decorator
