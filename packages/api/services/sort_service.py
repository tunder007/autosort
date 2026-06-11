"""
sort_service.py — runs core pipeline on a directory for cloud jobs.

What it does:
  Thin wrapper around core.pipeline.sort_folder for the API layer.

Input:
  work_dir: Path — directory containing files to sort (top-level)

Output:
  SortResult from core

Does not:
  Handle zip upload/extract (storage.py) or HTTP.
"""

from __future__ import annotations

from pathlib import Path

from core.pipeline import sort_folder
from core.types import SortResult


def run_cloud_sort(work_dir: Path, dry_run: bool = False) -> SortResult:
    """Sort files in work_dir using the core algorithm."""
    return sort_folder(work_dir, dry_run=dry_run)
