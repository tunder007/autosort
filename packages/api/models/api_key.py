"""
api_key.py — API keys linked to GitHub identity.

What it does:
  Stores hashed API keys for Bearer authentication on job/history endpoints.

Input:
  Created via POST /api-keys after GitHub session

Output:
  ApiKey rows; raw key shown only once at creation

Does not:
  Store plaintext keys or validate OAuth on every job request.
"""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.database import Base


class ApiKey(Base):
    """Long-lived API key for CLI and automation."""

    __tablename__ = "api_keys"

    id: Mapped[int] = mapped_column(primary_key=True)
    identity_id: Mapped[int] = mapped_column(ForeignKey("identities.id"))
    key_hash: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    label: Mapped[str] = mapped_column(String(100), default="default")
    key_prefix: Mapped[str] = mapped_column(String(12))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    identity: Mapped["Identity"] = relationship(back_populates="api_keys")


from api.models.identity import Identity  # noqa: E402
