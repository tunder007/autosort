"""
upload.py — upload zip for cloud sort jobs.

What it does:
  Accepts .zip for a pending cloud job, runs worker, returns completed job.

Input:
  multipart file upload + job id + API key

Output:
  JobResponse with status done and output_path set

Does not:
  Handle local CLI jobs or GitHub onboarding.
"""

from __future__ import annotations

import shutil
from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from api.database import get_db
from api.dependencies import verify_api_key
from api.models.identity import Identity
from api.models.job import Job
from api.schemas.job import JobResponse
from api.services.storage import job_dir
from api.worker import process_cloud_job

router = APIRouter(prefix="/jobs", tags=["upload"])


@router.post("/{job_id}/upload", response_model=JobResponse)
async def upload_zip(
    job_id: int,
    auth: Annotated[tuple[Identity, object], Depends(verify_api_key)],
    db: Session = Depends(get_db),
    file: UploadFile = File(...),
) -> Job:
    identity, _ = auth
    job = db.query(Job).filter(Job.id == job_id, Job.identity_id == identity.id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    if job.mode != "cloud":
        raise HTTPException(status_code=400, detail="Only cloud jobs accept uploads")
    if job.status not in {"pending", "failed"}:
        raise HTTPException(status_code=400, detail="Job already processed")

    if not file.filename or not file.filename.lower().endswith(".zip"):
        raise HTTPException(status_code=400, detail="Upload must be a .zip file")

    upload_path = job_dir(job_id) / "upload.zip"
    with upload_path.open("wb") as handle:
        shutil.copyfileobj(file.file, handle)

    job.status = "processing"
    db.add(job)
    db.commit()

    try:
        return process_cloud_job(db, job, identity, upload_path)
    except Exception as exc:
        job.status = "failed"
        job.result_json = str(exc)
        db.add(job)
        db.commit()
        raise HTTPException(status_code=500, detail=f"Sort failed: {exc}") from exc
