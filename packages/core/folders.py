"""
folders.py — README step 2: create type folders.

What it does:
  Creates one `<type>_folder` directory for each type in the sort matrix.

Input:
  folder_path: Path — parent folder
  matrix: SortMatrix — output from scanner

Output:
  list[Path] — paths of created (or existing) type folders

Does not:
  Scan files or move them.
"""

from __future__ import annotations

from pathlib import Path

from core.types import SortMatrix


def folder_name_for_type(file_type: str) -> str:
    """Return destination folder name for a file type."""
    return f"{file_type}_folder"


def create_type_folders(folder_path: Path, matrix: SortMatrix) -> list[Path]:
    """Create one subfolder per file type in the matrix."""
    parent = folder_path.resolve()
    created: list[Path] = []

    for group in matrix:
        target = parent / folder_name_for_type(group.type)
        target.mkdir(exist_ok=True)
        created.append(target)

    return created
