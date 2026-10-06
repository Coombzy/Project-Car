from __future__ import annotations

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.config import settings


def _create_engine() -> Engine:
    url = settings.database_url
    if url.startswith("sqlite"):
        # The visual check serves one sqlite file to uvicorn. Memory URLs need
        # one shared connection; a file URL can use the default pool.
        if url in {"sqlite://", "sqlite:///:memory:"}:
            return create_engine(
                url,
                connect_args={"check_same_thread": False},
                poolclass=StaticPool,
            )
        return create_engine(url, connect_args={"check_same_thread": False})
    return create_engine(url, pool_pre_ping=True)


engine = _create_engine()
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


def get_db() -> Generator[Session, None, None]:
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
