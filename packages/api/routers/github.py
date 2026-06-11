"""
github.py — GitHub OAuth (sole identity provider, no password accounts).

What it does:
  Starts OAuth flow, handles callback, creates/updates Identity, sets session cookie.

Input:
  OAuth code and state from GitHub redirect

Output:
  Redirect to web /connect; signed autosort_session cookie

Does not:
  Issue API keys (api_keys router) or validate Bearer tokens on job routes.
"""

from __future__ import annotations

import secrets
from typing import Annotated
from urllib.parse import urlencode

import httpx
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from itsdangerous import URLSafeSerializer
from sqlalchemy.orm import Session

from api.config import get_settings
from api.database import get_db
from api.dependencies import get_github_session
from api.models.identity import Identity

router = APIRouter(prefix="/auth", tags=["auth"])
settings = get_settings()
serializer = URLSafeSerializer(settings.session_secret, salt="autosort-session")
_oauth_states: dict[str, bool] = {}


@router.get("/github")
def github_login() -> RedirectResponse:
    if not settings.github_client_id:
        raise HTTPException(status_code=503, detail="GitHub OAuth not configured")

    state = secrets.token_urlsafe(16)
    _oauth_states[state] = True
    params = urlencode(
        {
            "client_id": settings.github_client_id,
            "redirect_uri": settings.github_callback_url,
            "scope": "read:user",
            "state": state,
        }
    )
    return RedirectResponse(f"https://github.com/login/oauth/authorize?{params}")


@router.get("/github/callback")
def github_callback(
    request: Request,
    code: str,
    state: str,
    db: Session = Depends(get_db),
) -> RedirectResponse:
    if state not in _oauth_states:
        raise HTTPException(status_code=400, detail="Invalid OAuth state")
    del _oauth_states[state]

    if not settings.github_client_secret:
        raise HTTPException(status_code=503, detail="GitHub OAuth not configured")

    with httpx.Client() as client:
        token_resp = client.post(
            "https://github.com/login/oauth/access_token",
            headers={"Accept": "application/json"},
            data={
                "client_id": settings.github_client_id,
                "client_secret": settings.github_client_secret,
                "code": code,
                "redirect_uri": settings.github_callback_url,
            },
        )
        token_resp.raise_for_status()
        access_token = token_resp.json().get("access_token")
        if not access_token:
            raise HTTPException(status_code=400, detail="GitHub token exchange failed")

        user_resp = client.get(
            "https://api.github.com/user",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        user_resp.raise_for_status()
        user = user_resp.json()

    github_id = int(user["id"])
    username = user.get("login", "unknown")

    identity = db.query(Identity).filter(Identity.github_id == github_id).first()
    if not identity:
        identity = Identity(github_id=github_id, github_username=username)
        db.add(identity)
        db.commit()
        db.refresh(identity)
    else:
        identity.github_username = username
        db.add(identity)
        db.commit()

    session_token = serializer.dumps({"identity_id": identity.id})
    response = RedirectResponse(f"{settings.web_url}/connect?connected=1")
    response.set_cookie(
        key="autosort_session",
        value=session_token,
        httponly=True,
        samesite="lax",
        max_age=60 * 60 * 24 * 30,
    )
    return response


@router.get("/session")
def get_session(identity: Annotated[Identity, Depends(get_github_session)]) -> dict:
    return {
        "github_id": identity.github_id,
        "github_username": identity.github_username,
        "stripe_customer_id": identity.stripe_customer_id,
        "has_payment_method": bool(identity.stripe_customer_id),
    }
