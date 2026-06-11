"""
history.py — README step 4: job audit log (sort history).

What it does:
  Returns recent sort jobs for the identity linked to the API key.

Input:
  Authorization: Bearer sk_...

Output:
  List of HistoryItem (mode, status, files_moved, timestamps)

Does not:
  Integrate with Git; this is an application audit log only.
"""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.database import get_db
from api.dependencies import verify_api_key
from api.models.identity import Identity
from api.models.job import Job
from api.schemas.job import HistoryItem

router = APIRouter(prefix="/history", tags=["history"])


@router.get("", response_model=list[HistoryItem])
def list_history(
    auth: Annotated[tuple[Identity, object], Depends(verify_api_key)],
    db: Session = Depends(get_db),
) -> list[Job]:
    identity, _ = auth
    return (
        db.query(Job)
        .filter(Job.identity_id == identity.id)
        .order_by(Job.created_at.desc())
        .limit(100)
        .all()
    )
