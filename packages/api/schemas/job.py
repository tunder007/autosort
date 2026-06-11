"""
schemas/job.py — Pydantic request/response models for job endpoints.

What it does:
  Validates JSON bodies and shapes API responses for jobs and history.

Input:
  HTTP JSON from clients

Output:
  Typed models for FastAPI response_model

Does not:
  Persist data or run business logic.
"""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class JobCreate(BaseModel):
    mode: str = Field(pattern="^(local|cloud)$")


class JobComplete(BaseModel):
    files_moved: int
    types_found: list[str] = []
    folder_path: str | None = None
    duration_ms: int | None = None


class JobResponse(BaseModel):
    id: int
    mode: str
    status: str
    files_moved: int
    folder_path: str | None
    created_at: datetime
    completed_at: datetime | None = None

    model_config = {"from_attributes": True}


class HistoryItem(BaseModel):
    id: int
    mode: str
    status: str
    files_moved: int
    folder_path: str | None
    created_at: datetime
    completed_at: datetime | None = None

    model_config = {"from_attributes": True}
