"""
billing_service.py — pay-as-you-go usage reporting to Stripe.

What it does:
  Increments local usage counter and sends Stripe Meter Events (1 file = 1 unit).

Input:
  identity: Identity, file_count: int from completed job

Output:
  Updated identity.files_billed_this_month; optional Stripe meter event

Does not:
  Manage subscriptions or pricing pages.
"""

from __future__ import annotations

import logging

import stripe
from sqlalchemy.orm import Session

from api.config import get_settings
from api.models.identity import Identity

logger = logging.getLogger(__name__)
settings = get_settings()


def report_usage(db: Session, identity: Identity, file_count: int) -> None:
    """Record file_count units for identity locally and in Stripe when configured."""
    if file_count <= 0:
        return

    identity.files_billed_this_month += file_count
    db.add(identity)
    db.commit()

    if not settings.stripe_secret_key:
        logger.info("Stripe not configured — usage recorded locally only (%s files)", file_count)
        return

    stripe.api_key = settings.stripe_secret_key
    if not identity.stripe_customer_id:
        logger.warning("No stripe_customer_id for identity %s", identity.id)
        return

    try:
        stripe.billing.MeterEvent.create(
            event_name=settings.stripe_meter_event_name,
            payload={
                "stripe_customer_id": identity.stripe_customer_id,
                "value": str(file_count),
            },
        )
    except Exception as exc:
        logger.exception("Stripe meter event failed: %s", exc)
