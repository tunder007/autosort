"""
billing.py — Stripe pay-as-you-go setup and usage.

What it does:
  Creates Stripe customer + Setup Checkout; returns monthly usage summary.

Input:
  GitHub session cookie

Output:
  checkout_url for add card; UsageResponse for GET /usage

Does not:
  Report per-job usage (billing_service on job complete).
"""

from __future__ import annotations

from typing import Annotated

import stripe
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.config import get_settings
from api.database import get_db
from api.dependencies import get_github_session
from api.models.identity import Identity
from api.schemas.billing import UsageResponse

router = APIRouter(prefix="/billing", tags=["billing"])
settings = get_settings()


@router.post("/setup")
def setup_billing(
    identity: Annotated[Identity, Depends(get_github_session)],
    db: Session = Depends(get_db),
) -> dict:
    if not settings.stripe_secret_key:
        identity.stripe_customer_id = identity.stripe_customer_id or f"dev_cus_{identity.id}"
        db.add(identity)
        db.commit()
        return {
            "checkout_url": f"{settings.web_url}/connect?billing=dev",
            "dev_mode": True,
        }

    stripe.api_key = settings.stripe_secret_key

    if not identity.stripe_customer_id:
        customer = stripe.Customer.create(
            metadata={"github_id": str(identity.github_id), "github_username": identity.github_username},
        )
        identity.stripe_customer_id = customer.id
        db.add(identity)
        db.commit()

    session = stripe.checkout.Session.create(
        mode="setup",
        customer=identity.stripe_customer_id,
        success_url=f"{settings.web_url}/connect?billing=success",
        cancel_url=f"{settings.web_url}/connect?billing=cancel",
    )
    return {"checkout_url": session.url, "dev_mode": False}


@router.get("/usage", response_model=UsageResponse)
def get_usage(
    identity: Annotated[Identity, Depends(get_github_session)],
) -> UsageResponse:
    return UsageResponse(
        files_billed_this_month=identity.files_billed_this_month,
        stripe_customer_id=identity.stripe_customer_id,
    )
