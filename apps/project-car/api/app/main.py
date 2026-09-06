from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import __version__
from app.config import get_settings
from app.errors import register_error_handlers
from app.routers import auth, bookings, chat, dashboard, fill, hoists, member, member_chat, members, tiers, waitlist


def create_app() -> FastAPI:
    application = FastAPI(
        title="Project Car Shop API",
        version=__version__,
        description=(
            "Shop OS API. Owner dashboard plus Member self-serve (balance, "
            "book / cancel, schedule quote) and Chat v1 (human / polling). "
            "Auth is a v1 session stub (Owner cookie/bearer; Member cookie), "
            "not OIDC. Demo data only — the shop is not open and there is no "
            "live payment processor."
        ),
    )
    register_error_handlers(application)

    origins = get_settings().cors_origin_list
    if origins:
        application.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["GET", "POST", "PATCH", "OPTIONS", "HEAD"],
            allow_headers=["Accept", "Content-Type", "Authorization"],
        )

    application.include_router(auth.router)
    application.include_router(member.router)
    application.include_router(waitlist.router)
    application.include_router(dashboard.router)
    application.include_router(tiers.router)
    application.include_router(members.router)
    application.include_router(hoists.router)
    application.include_router(bookings.router)
    application.include_router(fill.router)
    application.include_router(chat.router)
    application.include_router(member_chat.router)
    return application


app = create_app()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "project-car-api"}
