# packages/cli

Local agent — runs the sorting algorithm on your disk.

## Usage

```bash
pip install -e .
autosort sort "C:\Downloads\LargeFolder" --dry-run
autosort sort "./folder" --api-key sk_your_key
```

| Flag | Purpose |
|------|---------|
| `--dry-run` | Preview moves without changing files |
| `--api-key` | Report job + usage to the API after sorting |
| `--api-url` | API base URL (default: `http://localhost:8000`) |

## What it does

1. Calls `core.pipeline.sort_folder` on the given folder
2. With `--api-key`: creates a local job, completes it, triggers billing/history

## What it does not

- Upload files to the cloud (use the web UI or API upload endpoint)
- Handle GitHub OAuth (use `/connect` in the browser first)
