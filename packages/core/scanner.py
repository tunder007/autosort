"""
scanner.py — README step 1: scan folder and build sort matrix.

What it does:
  Walks a folder and groups absolute file paths by detected type.

Input:
  folder_path: Path — the large folder (top-level files only)

Output:
  SortMatrix — ordered list of FileGroup; type order = first appearance in folder

Does not:
  Create folders, move files, or recurse into subfolders.
"""

from __future__ import annotations

from pathlib import Path

from core.detector import detect_type
from core.types import FileGroup, SortMatrix


def scan_folder(folder_path: Path) -> SortMatrix:
    """Scan top-level files only and group by detected type."""
    folder = folder_path.resolve()
    if not folder.is_dir():
        raise NotADirectoryError(f"Not a directory: {folder}")

    type_order: list[str] = []
    groups: dict[str, list[Path]] = {}

    for entry in sorted(folder.iterdir(), key=lambda p: p.name.lower()):
        if not entry.is_file():
            continue

        file_type = detect_type(entry)
        if file_type not in groups:
            type_order.append(file_type)
            groups[file_type] = []
        groups[file_type].append(entry.resolve())

    return [FileGroup(type=t, paths=groups[t]) for t in type_order]
