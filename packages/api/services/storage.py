"""
storage.py — temporary file storage for cloud job uploads and downloads.

What it does:
  Manages per-job directories: extract zip, zip sorted output, cleanup.

Input:
  job_id, paths to zip files and work directories

Output:
  Paths under STORAGE_PATH for input extraction and output.zip

Does not:
  Run sorting or authenticate requests.
"""

from __future__ import annotations

import shutil
import zipfile
from pathlib import Path

from api.config import get_settings

settings = get_settings()


def job_dir(job_id: int) -> Path:
    """Return and create storage directory for a job."""
    path = settings.storage_path / str(job_id)
    path.mkdir(parents=True, exist_ok=True)
    return path


def extract_upload(job_id: int, zip_path: Path) -> Path:
    """Extract upload.zip into job input directory."""
    work = job_dir(job_id) / "input"
    work.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, "r") as archive:
        archive.extractall(work)
    return work


def zip_output(job_id: int, source_dir: Path) -> Path:
    """Zip sorted files into job output.zip."""
    output = job_dir(job_id) / "output.zip"
    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as archive:
        for file in source_dir.rglob("*"):
            if file.is_file():
                archive.write(file, file.relative_to(source_dir).as_posix())
    return output


def cleanup_job(job_id: int) -> None:
    """Remove all files for a job (optional maintenance)."""
    path = settings.storage_path / str(job_id)
    if path.exists():
        shutil.rmtree(path, ignore_errors=True)
