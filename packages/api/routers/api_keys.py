"""
api_keys.py — generate and revoke API keys (requires GitHub session).

What it does:
  CRUD for API keys tied to OAuth identity during onboarding.

Input:
  GitHub session cookie; optional label on create

Output:
  Key list (prefix only) or new raw key once on POST

Does not:
  Accept API key auth for its own endpoints (session required).
"""

from __future__ import annotations

import secrets
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from api.database import get_db
from api.dependencies import get_github_session, hash_api_key
from api.models.api_key import ApiKey
from api.models.identity import Identity

router = APIRouter(prefix="/api-keys", tags=["api-keys"])


class ApiKeyCreate(BaseModel):
    label: str = "default"


class ApiKeyResponse(BaseModel):
    id: int
    label: str
    key_prefix: str

    model_config = {"from_attributes": True}


class ApiKeyCreated(ApiKeyResponse):
    key: str


@router.post("", response_model=ApiKeyCreated)
def create_api_key(
    body: ApiKeyCreate,
    identity: Annotated[Identity, Depends(get_github_session)],
    db: Session = Depends(get_db),
) -> dict:
    raw_key = f"sk_{secrets.token_urlsafe(32)}"
    api_key = ApiKey(
        identity_id=identity.id,
        key_hash=hash_api_key(raw_key),
        label=body.label,
        key_prefix=raw_key[:10],
    )
    db.add(api_key)
    db.commit()
    db.refresh(api_key)
    return {
        "id": api_key.id,
        "label": api_key.label,
        "key_prefix": api_key.key_prefix,
        "key": raw_key,
    }


@router.get("", response_model=list[ApiKeyResponse])
def list_api_keys(
    identity: Annotated[Identity, Depends(get_github_session)],
    db: Session = Depends(get_db),
) -> list[ApiKey]:
    return db.query(ApiKey).filter(ApiKey.identity_id == identity.id).all()


@router.delete("/{key_id}")
def revoke_api_key(
    key_id: int,
    identity: Annotated[Identity, Depends(get_github_session)],
    db: Session = Depends(get_db),
) -> dict:
    api_key = (
        db.query(ApiKey)
        .filter(ApiKey.id == key_id, ApiKey.identity_id == identity.id)
        .first()
    )
    if not api_key:
        raise HTTPException(status_code=404, detail="API key not found")
    db.delete(api_key)
    db.commit()
    return {"deleted": True}
