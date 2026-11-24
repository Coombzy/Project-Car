# ADR 0002: SQLAlchemy models and Alembic migrations

**Status:** accepted

**Decision:** Persistence is SQLAlchemy ORM models in `app/models.py` with schema changes applied through Alembic under `apps/project-car/api/alembic/`. `settings.database_url` selects the database; pytest uses SQLite via `app/db.py` when the URL is sqlite.

**Why:** One domain model and versioned migrations keep shop data consistent across dev, CI, and Postgres deploys.

**Source:** `app/models.py`; `app/config.py` (`database_url`); `app/db.py`; `apps/project-car/api/alembic/`; `apps/project-car/api/alembic.ini`.

**Consequences:** New tables/columns need an Alembic revision. Do not bypass the ORM for shop domain writes agents are implementing.