"""
main.py — FastAPI application entry point.

What it does:
  Mounts routers, CORS, DB init; exposes OpenAPI at /docs and /redoc.

Input:
  HTTP requests from CLI, web UI, and API clients

Output:
  REST responses, OpenAPI schema

Does not:
  Run the sort algorithm directly (delegates to services/worker).
"""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.config import get_settings
from api.database import init_db
from api.routers import api_keys, billing, github, history, jobs, upload

settings = get_settings()

app = FastAPI(
    title="Autosort API",
    description="Sort files by type — pay-as-you-go SaaS",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.web_url, "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(github.router)
app.include_router(api_keys.router)
app.include_router(billing.router)
app.include_router(jobs.router)
app.include_router(upload.router)
app.include_router(history.router)


@app.on_event("startup")
def on_startup() -> None:
    """Create database tables and storage directory on startup."""
    init_db()


@app.get("/health")
def health() -> dict:
    """Liveness check for deployments."""
    return {"status": "ok"}
