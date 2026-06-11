"""
jobs.py — create, complete, and download sort jobs.

What it does:
  Job lifecycle: create (local/cloud), get status, CLI complete, cloud download.

Input:
  Bearer API key; JSON bodies per endpoint

Output:
  JobResponse or zip FileResponse

Does not:
  Accept zip uploads (upload router) or list all jobs (history router).
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from api.database import get_db
from api.dependencies import require_billing_ready, verify_api_key
from api.models.identity import Identity
from api.models.job import Job
from api.schemas.job import JobComplete, JobCreate, JobResponse
from api.services.billing_service import report_usage

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.post("", response_model=JobResponse)
def create_job(
    body: JobCreate,
    auth: Annotated[tuple[Identity, object], Depends(verify_api_key)],
    db: Session = Depends(get_db),
) -> Job:
    identity, _api_key = auth
    require_billing_ready(identity)

    job = Job(identity_id=identity.id, mode=body.mode, status="pending")
    db.add(job)
    db.commit()
    db.refresh(job)
    return job


@router.get("/{job_id}", response_model=JobResponse)
def get_job(
    job_id: int,
    auth: Annotated[tuple[Identity, object], Depends(verify_api_key)],
    db: Session = Depends(get_db),
) -> Job:
    identity, _ = auth
    job = db.query(Job).filter(Job.id == job_id, Job.identity_id == identity.id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@router.post("/{job_id}/complete", response_model=JobResponse)
def complete_job(
    job_id: int,
    body: JobComplete,
    auth: Annotated[tuple[Identity, object], Depends(verify_api_key)],
    db: Session = Depends(get_db),
) -> Job:
    identity, _ = auth
    job = db.query(Job).filter(Job.id == job_id, Job.identity_id == identity.id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    if job.mode != "local":
        raise HTTPException(status_code=400, detail="Only local jobs can be completed via CLI")

    job.status = "done"
    job.files_moved = body.files_moved
    job.folder_path = body.folder_path
    job.result_json = json.dumps(
        {
            "types_found": body.types_found,
            "duration_ms": body.duration_ms,
        }
    )
    job.completed_at = datetime.now(timezone.utc)
    db.add(job)
    db.commit()
    db.refresh(job)

    report_usage(db, identity, body.files_moved)
    return job


@router.get("/{job_id}/download")
def download_job(
    job_id: int,
    auth: Annotated[tuple[Identity, object], Depends(verify_api_key)],
    db: Session = Depends(get_db),
) -> FileResponse:
    identity, _ = auth
    job = db.query(Job).filter(Job.id == job_id, Job.identity_id == identity.id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    if job.mode != "cloud" or job.status != "done" or not job.output_path:
        raise HTTPException(status_code=400, detail="Job output not ready")

    output = Path(job.output_path)
    if not output.is_file():
        raise HTTPException(status_code=404, detail="Output file missing")

    return FileResponse(
        path=output,
        filename=f"autosort_job_{job_id}.zip",
        media_type="application/zip",
    )
