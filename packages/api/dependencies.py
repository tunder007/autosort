"""
dependencies.py — API key verification and GitHub session for onboarding.

What it does:
  FastAPI dependencies: verify_api_key, get_github_session, require_billing_ready.

Input:
  Authorization header or autosort_session cookie

Output:
  Identity (+ ApiKey for API key auth)

Does not:
  Issue JWT login tokens or manage password accounts.
"""

from __future__ import annotations

import hashlib
from typing import Annotated

from fastapi import Cookie, Depends, Header, HTTPException, status
from itsdangerous import BadSignature, URLSafeSerializer
from sqlalchemy.orm import Session

from api.config import get_settings
from api.database import get_db
from api.models.api_key import ApiKey
from api.models.identity import Identity

settings = get_settings()
serializer = URLSafeSerializer(settings.session_secret, salt="autosort-session")


def hash_api_key(raw_key: str) -> str:
    """Return SHA-256 hex digest of a raw API key for storage lookup."""
    return hashlib.sha256(raw_key.encode()).hexdigest()


def verify_api_key(
    authorization: Annotated[str | None, Header()] = None,
    db: Session = Depends(get_db),
) -> tuple[Identity, ApiKey]:
    """Validate Bearer API key and return identity + key record."""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing API key")

    raw_key = authorization.removeprefix("Bearer ").strip()
    if not raw_key.startswith("sk_"):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key format")

    key_hash = hash_api_key(raw_key)
    api_key = db.query(ApiKey).filter(ApiKey.key_hash == key_hash).first()
    if not api_key:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key")

    identity = db.query(Identity).filter(Identity.id == api_key.identity_id).first()
    if not identity:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Identity not found")

    return identity, api_key


def get_github_session(
    autosort_session: Annotated[str | None, Cookie()] = None,
    db: Session = Depends(get_db),
) -> Identity:
    """Load Identity from signed session cookie set after GitHub OAuth."""
    if not autosort_session:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Connect GitHub first")

    try:
        data = serializer.loads(autosort_session)
        identity_id = int(data["identity_id"])
    except (BadSignature, KeyError, ValueError) as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid session") from exc

    identity = db.query(Identity).filter(Identity.id == identity_id).first()
    if not identity:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Identity not found")
    return identity


def require_billing_ready(identity: Identity) -> None:
    """Raise 402 if identity has no Stripe customer (payment method not set up)."""
    if not identity.stripe_customer_id:
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail="Add a payment method at /connect before sorting",
        )
