"""
pipeline.py — orchestrates scanner → folders → mover.

What it does:
  Runs README steps 1–3 in a single call.

Input:
  folder_path: Path, dry_run: bool

Output:
  SortResult

Does not:
  HTTP, database access, authentication, or billing.
"""

from __future__ import annotations

from pathlib import Path

from core.folders import create_type_folders
from core.mover import move_files
from core.scanner import scan_folder
from core.types import SortResult


def sort_folder(folder_path: Path, dry_run: bool = False) -> SortResult:
    """Scan, create type folders, and move files."""
    folder = Path(folder_path)
    matrix = scan_folder(folder)
    if not matrix:
        return SortResult(
            files_moved=0,
            types_found=[],
            dry_run=dry_run,
            folder_path=str(folder.resolve()),
            details={"message": "No files to sort"},
        )

    create_type_folders(folder, matrix)
    return move_files(folder, matrix, dry_run=dry_run)
