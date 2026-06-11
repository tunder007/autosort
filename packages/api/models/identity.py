"""
identity.py — GitHub-linked identity and Stripe customer (no password accounts).

What it does:
  ORM model for external identity: github_id, username, stripe_customer_id, usage counter.

Input:
  Rows inserted/updated by github and billing routers

Output:
  Identity records for API keys and jobs

Does not:
  Store passwords, emails, or custom login credentials.
"""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import BigInteger, DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.database import Base


class Identity(Base):
    """User identity from OAuth provider plus optional Stripe customer."""

    __tablename__ = "identities"

    id: Mapped[int] = mapped_column(primary_key=True)
    github_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)
    github_username: Mapped[str] = mapped_column(String(255))
    stripe_customer_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    files_billed_this_month: Mapped[int] = mapped_column(default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    api_keys: Mapped[list["ApiKey"]] = relationship(back_populates="identity")
    jobs: Mapped[list["Job"]] = relationship(back_populates="identity")


from api.models.api_key import ApiKey  # noqa: E402
from api.models.job import Job  # noqa: E402
