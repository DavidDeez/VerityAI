from fastapi import APIRouter

from app.api import auth, projects, traces, datasets, evaluations, metrics, benchmarks

api_router = APIRouter()
api_router.include_router(auth.router, tags=["login"])
api_router.include_router(projects.router, prefix="/projects", tags=["projects"])
api_router.include_router(traces.router, prefix="/traces", tags=["traces"])
api_router.include_router(datasets.router, prefix="/datasets", tags=["datasets"])
api_router.include_router(evaluations.router, prefix="/evaluations", tags=["evaluations"])
api_router.include_router(metrics.router, prefix="/metrics", tags=["metrics"])
api_router.include_router(benchmarks.router, prefix="/benchmarks", tags=["benchmarks"])
