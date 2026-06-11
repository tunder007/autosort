"""
schemas/billing.py — Pydantic models for billing usage responses.

What it does:
  Shapes GET /billing/usage response.

Does not:
  Call Stripe or update usage counters.
"""

from pydantic import BaseModel


class UsageResponse(BaseModel):
    files_billed_this_month: int
    stripe_customer_id: str | None
