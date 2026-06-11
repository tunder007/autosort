"""
main.py — CLI entry point for local sorting.

What it does:
  Runs sort_folder on disk; optionally reports job completion to the API.

Input:
  Command-line: folder path, --dry-run, --api-key, --api-url

Output:
  Sorted folder on disk; optional HTTP job record when --api-key is set

Does not:
  Implement OAuth, billing, or cloud zip upload (see packages/api).
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from core.pipeline import sort_folder


def _api_request(method: str, url: str, api_key: str, body: dict | None = None) -> dict:
    """Send an authenticated JSON request to the Autosort API."""
    data = json.dumps(body).encode() if body is not None else None
    request = Request(
        url,
        data=data,
        method=method,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
    )
    with urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode())


def _report_to_api(folder: Path, api_key: str, api_url: str, dry_run: bool) -> int:
    """Sort locally, then create and complete a job on the API for billing/history."""
    start = time.perf_counter()
    result = sort_folder(folder, dry_run=dry_run)
    duration_ms = int((time.perf_counter() - start) * 1000)

    if dry_run:
        print(f"[dry-run] Would move {result.files_moved} files")
        return 0

    job = _api_request("POST", f"{api_url.rstrip('/')}/jobs", api_key, {"mode": "local"})
    job_id = job["id"]
    _api_request(
        "POST",
        f"{api_url.rstrip('/')}/jobs/{job_id}/complete",
        api_key,
        {
            "files_moved": result.files_moved,
            "types_found": result.types_found,
            "folder_path": result.folder_path,
            "duration_ms": duration_ms,
        },
    )
    print(f"Sorted {result.files_moved} files. Job {job_id} recorded.")
    return 0


def main() -> int:
    """Parse CLI arguments and run sort or API-backed sort."""
    parser = argparse.ArgumentParser(prog="autosort", description="Sort files by type")
    sub = parser.add_subparsers(dest="command", required=True)

    sort_parser = sub.add_parser("sort", help="Sort files in a folder")
    sort_parser.add_argument("folder", type=Path, help="Folder to sort")
    sort_parser.add_argument("--dry-run", action="store_true", help="Preview without moving")
    sort_parser.add_argument("--api-key", help="API key for usage tracking")
    sort_parser.add_argument("--api-url", default="http://localhost:8000", help="API base URL")

    args = parser.parse_args()

    if args.command == "sort":
        folder = args.folder.resolve()
        if not folder.is_dir():
            print(f"Error: not a directory: {folder}", file=sys.stderr)
            return 1

        if args.api_key and not args.dry_run:
            try:
                return _report_to_api(folder, args.api_key, args.api_url, args.dry_run)
            except (HTTPError, URLError) as exc:
                print(f"API error: {exc}", file=sys.stderr)
                return 1

        result = sort_folder(folder, dry_run=args.dry_run)
        action = "Would move" if args.dry_run else "Moved"
        print(f"{action} {result.files_moved} files into {len(result.types_found)} type folders")
        for t in result.types_found:
            print(f"  - {t}_folder")
        return 0

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
