"""
core package — sorting algorithm (scan, folders, move).

What it does:
  Re-exports the main pipeline entry point and shared types.

Does not:
  Provide CLI, HTTP API, or billing.
"""

from core.pipeline import sort_folder
from core.types import FileGroup, SortMatrix, SortResult

__all__ = ["FileGroup", "SortMatrix", "SortResult", "sort_folder"]
