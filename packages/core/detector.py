"""
detector.py — deterministic file type detection.

What it does:
  Detects file type from extension and magic bytes (first bytes of file). No AI.

Input:
  path: Path — path to a single file

Output:
  str — short type label (e.g. pdf, word, png, unknown)

Does not:
  Walk folders, move files, or call external classification APIs.
"""

from __future__ import annotations

from pathlib import Path

EXTENSION_MAP: dict[str, str] = {
    ".pdf": "pdf",
    ".doc": "word",
    ".docx": "word",
    ".png": "png",
    ".jpg": "image",
    ".jpeg": "image",
    ".gif": "image",
    ".webp": "image",
    ".txt": "text",
    ".md": "text",
    ".csv": "spreadsheet",
    ".xls": "spreadsheet",
    ".xlsx": "spreadsheet",
    ".zip": "archive",
    ".rar": "archive",
    ".mp3": "audio",
    ".wav": "audio",
    ".mp4": "video",
    ".mov": "video",
    ".avi": "video",
}

MAGIC_MAP: list[tuple[bytes, str]] = [
    (b"%PDF", "pdf"),
    (b"\x89PNG\r\n\x1a\n", "png"),
    (b"\xff\xd8\xff", "image"),
    (b"GIF87a", "image"),
    (b"GIF89a", "image"),
    (b"PK\x03\x04", "archive"),
    (b"RIFF", "audio"),
]


def _read_header(path: Path, n: int = 16) -> bytes:
    with path.open("rb") as handle:
        return handle.read(n)


def detect_type(path: Path) -> str:
    """Return file type label for a single file."""
    if not path.is_file():
        return "unknown"

    header = _read_header(path)
    for magic, file_type in MAGIC_MAP:
        if header.startswith(magic):
            if file_type == "archive" and path.suffix.lower() in {".docx", ".xlsx"}:
                return EXTENSION_MAP.get(path.suffix.lower(), "archive")
            return file_type

    return EXTENSION_MAP.get(path.suffix.lower(), "unknown")
