"""
database.py — SQLAlchemy engine and session factory.

What it does:
  Provides DB engine, Base model class, session dependency, and init_db().

Input:
  DATABASE_URL from config

Output:
  SQLAlchemy Session via get_db() dependency

Does not:
  Define table schemas (see models/) or run migrations (create_all only).
"""

from __future__ import annotations

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from api.config import get_settings


class Base(DeclarativeBase):
    """Declarative base for all ORM models."""


settings = get_settings()
connect_args = {"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}
engine = create_engine(settings.database_url, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency that yields a DB session per request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """Create all tables and ensure storage directory exists."""
    from api.models import api_key, identity, job  # noqa: F401

    settings.storage_path.mkdir(parents=True, exist_ok=True)
    Base.metadata.create_all(bind=engine)
