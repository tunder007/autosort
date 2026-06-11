"""
worker.py — processes cloud sort jobs (MVP: synchronous).

What it does:
  Extracts uploaded zip, runs core pipeline, builds output zip, reports billing.

Input:
  Job record, Identity, path to upload.zip

Output:
  Updated Job with status done and output_path set

Does not:
  Handle local CLI jobs (those complete via POST /jobs/{id}/complete).
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from sqlalchemy.orm import Session

from api.models.identity import Identity
from api.models.job import Job
from api.services.billing_service import report_usage
from api.services.sort_service import run_cloud_sort
from api.services.storage import extract_upload, zip_output


def process_cloud_job(db: Session, job: Job, identity: Identity, upload_path: Path) -> Job:
    """Run full cloud sort pipeline for one job."""
    work = extract_upload(job.id, upload_path)
    result = run_cloud_sort(work, dry_run=False)
    output_zip = zip_output(job.id, work)

    job.status = "done"
    job.files_moved = result.files_moved
    job.folder_path = str(work)
    job.output_path = str(output_zip)
    job.result_json = json.dumps(
        {
            "types_found": result.types_found,
            "details": result.details,
        }
    )
    job.completed_at = datetime.now(timezone.utc)
    db.add(job)
    db.commit()

    report_usage(db, identity, result.files_moved)
    return job
