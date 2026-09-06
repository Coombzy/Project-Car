from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import __version__
from app.config import settings
from app.errors import register_error_handlers
from app.routers import auth, waitlist


def create_app() -> FastAPI:
    application = FastAPI(
        title="Project Car Shop API",
        version=__version__,
        description=(
            "Shop OS API. Slice 1: corrected domain model and public waitlist. "
            "Owner auth is a v1 session stub (email/password or bearer secret), not OIDC."
        ),
    )
    register_error_handlers(application)

    origins = settings.cors_origin_list
    if origins:
        application.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    application.include_router(auth.router)
    application.include_router(waitlist.router)
    return application


app = create_app()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "project-car-api"}
