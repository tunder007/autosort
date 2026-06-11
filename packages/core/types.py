"""
types.py — shared data structures for the sorting pipeline.

What it does:
  Defines dataclasses used by scanner, folders, mover, and pipeline.

Input:
  None (type definitions only)

Output:
  FileGroup, SortMatrix, SortResult types for the pipeline

Does not:
  Detect file types, perform I/O, or call HTTP APIs.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

FileType = str


@dataclass
class FileGroup:
    """One row in the sort matrix: a file type and its absolute paths."""

    type: FileType
    paths: list[Path]


SortMatrix = list[FileGroup]


@dataclass
class SortResult:
    """Outcome of a sort_folder run."""

    files_moved: int
    types_found: list[str]
    dry_run: bool
    folder_path: str
    details: dict[str, Any] = field(default_factory=dict)
