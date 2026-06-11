"""
config.py — environment configuration.

What it does:
  Loads settings from environment variables for DB, OAuth, Stripe, and storage.

Input:
  OS environment (see docs/ENVIRONMENT.md)

Output:
  Settings dataclass singleton via get_settings()

Does not:
  Read .env files directly (use docker, shell, or a process manager).
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    database_url: str
    github_client_id: str
    github_client_secret: str
    github_callback_url: str
    session_secret: str
    stripe_secret_key: str
    stripe_webhook_secret: str
    stripe_meter_event_name: str
    stripe_price_id: str
    price_per_file_cents: float
    web_url: str
    api_url: str
    storage_path: Path


def get_settings() -> Settings:
    """Build Settings from environment variables with sensible dev defaults."""
    return Settings(
        database_url=os.getenv(
            "DATABASE_URL",
            "sqlite:///./autosort.db",
        ),
        github_client_id=os.getenv("GITHUB_CLIENT_ID", ""),
        github_client_secret=os.getenv("GITHUB_CLIENT_SECRET", ""),
        github_callback_url=os.getenv(
            "GITHUB_CALLBACK_URL",
            "http://localhost:8000/auth/github/callback",
        ),
        session_secret=os.getenv("SESSION_SECRET", "dev-secret-change-me"),
        stripe_secret_key=os.getenv("STRIPE_SECRET_KEY", ""),
        stripe_webhook_secret=os.getenv("STRIPE_WEBHOOK_SECRET", ""),
        stripe_meter_event_name=os.getenv("STRIPE_METER_EVENT_NAME", "autosort_files"),
        stripe_price_id=os.getenv("STRIPE_PRICE_ID", ""),
        price_per_file_cents=float(os.getenv("PRICE_PER_FILE_CENTS", "0.1")),
        web_url=os.getenv("WEB_URL", "http://localhost:3000"),
        api_url=os.getenv("API_URL", "http://localhost:8000"),
        storage_path=Path(os.getenv("STORAGE_PATH", "./packages/api/storage")),
    )
