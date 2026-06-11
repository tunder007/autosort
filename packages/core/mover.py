"""
mover.py — README step 3: move files into type folders.

What it does:
  Moves each file in the matrix into its corresponding `<type>_folder`.

Input:
  folder_path: Path — parent folder
  matrix: SortMatrix — file groups by type
  dry_run: bool — if True, simulate without moving

Output:
  SortResult — count of files moved and types found

Does not:
  Scan the folder or create directories (folders must exist).
"""

from __future__ import annotations

import shutil
from pathlib import Path

from core.folders import folder_name_for_type
from core.types import SortMatrix, SortResult


def move_files(folder_path: Path, matrix: SortMatrix, dry_run: bool = False) -> SortResult:
    """Move each file into its type folder."""
    parent = folder_path.resolve()
    moved = 0
    types_found = [group.type for group in matrix]
    moves: list[dict[str, str]] = []

    for group in matrix:
        dest_dir = parent / folder_name_for_type(group.type)
        for source in group.paths:
            target = dest_dir / source.name
            moves.append({"from": str(source), "to": str(target)})
            if not dry_run:
                if target.exists():
                    raise FileExistsError(f"Target already exists: {target}")
                shutil.move(str(source), str(target))
            moved += 1

    return SortResult(
        files_moved=moved,
        types_found=types_found,
        dry_run=dry_run,
        folder_path=str(parent),
        details={"moves": moves},
    )
