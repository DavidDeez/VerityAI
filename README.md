# VerityAI

> Open-source AI observability, evaluation, and reliability infrastructure for AI systems.

VerityAI helps AI engineers measure the reliability, safety, performance, and cost of LLM, RAG, and agentic systems. It serves as a comprehensive dashboard and evaluation engine.

## Features
* **Observability**: Track LLM interactions, latency, cost, and tool calls.
* **Evaluations**: Run rigorous evaluations on your AI applications.
* **Benchmarking**: Compare models and prompts on custom datasets.
* **Security Testing**: Detect prompt injections, data leaks, and instruction overrides.
* **Regression Testing**: Fail CI/CD when a new model or prompt regressions on key metrics.
* **Local AI Mode**: Pluggable provider support including Ollama and Fireworks.

## Architecture Diagram
```mermaid
flowchart TD
    subgraph Client Application
        SDK[Python SDK (@observe)]
    end

    subgraph Platform Backend
        API[FastAPI Backend]
        Worker[Background Tasks (Evaluator & Security)]
        Providers[LLM Providers: OpenAI, Ollama, Fireworks]
    end

    subgraph Data Layer
        PG[(PostgreSQL)]
    end

    subgraph Frontend
        Web[Next.js Dashboard & Trace Explorer]
    end

    SDK -->|Traces| API
    Web -->|Queries| API
    API -->|Write/Read| PG
    API -->|Run Tests| Worker
    Worker -->|Write Results| PG
    Worker -->|Query| Providers
```

## Quick Start (Demo Mode)

The easiest way to start the platform is using Docker Compose.

```bash
git clone https://github.com/DavidDeez/VerityAI.git
cd VerityAI
docker-compose up -d --build
```

- **Frontend Dashboard**: `http://localhost:3000`
- **Backend API Docs**: `http://localhost:8000/api/v1/openapi.json`

## SDK Usage

```python
from verityai import VerityAI

client = VerityAI(api_key="your_api_key")

@client.observe(model="gpt-4", provider="openai")
def agent_task(query):
    return "Agent response..."
```

## Documentation
- [Benchmark Report](BENCHMARK_REPORT.md)
- GitHub Actions CI/CD is configured in `.github/workflows/ci.yml`
