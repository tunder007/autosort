"""
job.py — sort job records for local and cloud modes.

What it does:
  Persists job lifecycle, file counts, and results for audit history.

Input:
  Created by jobs router; updated by CLI complete or cloud worker

Output:
  Job rows queryable via /history and GET /jobs/{id}

Does not:
  Execute the sort algorithm (worker/cli call core instead).
"""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.database import Base


class Job(Base):
    """One sort operation — local or cloud."""

    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(primary_key=True)
    identity_id: Mapped[int] = mapped_column(ForeignKey("identities.id"))
    mode: Mapped[str] = mapped_column(String(20))
    status: Mapped[str] = mapped_column(String(20), default="pending")
    files_moved: Mapped[int] = mapped_column(Integer, default=0)
    folder_path: Mapped[str | None] = mapped_column(String(1024), nullable=True)
    result_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    output_path: Mapped[str | None] = mapped_column(String(1024), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    identity: Mapped["Identity"] = relationship(back_populates="jobs")


from api.models.identity import Identity  # noqa: E402
