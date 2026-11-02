from __future__ import annotations

from fastapi import FastAPI

from app import __version__
from app.auth import assert_runtime_secrets, shop_dev_mode
from app.config import get_settings
from app.cors import ShopCorsMiddleware
from app.errors import register_error_handlers
from app.security_headers import SecurityHeadersMiddleware
from app.routers import (
    auth,
    bookings,
    calendar,
    chat,
    dashboard,
    fill,
    hoists,
    incidents,
    jobs,
    member,
    member_chat,
    members,
    parts_requests,
    signup,
    staff,
    tiers,
    todos,
    tool_crib,
    waitlist,
)


def create_app() -> FastAPI:
    settings = get_settings()
    assert_runtime_secrets(settings)
    dev = shop_dev_mode()
    application = FastAPI(
        title="Project Car Shop API",
        version=__version__,
        docs_url="/docs" if dev else None,
        redoc_url="/redoc" if dev else None,
        openapi_url="/openapi.json" if dev else None,
        description=(
            "Shop OS API. Owner dashboard plus Member self-serve (balance, "
            "book / cancel, schedule quote) and Chat v1 (human / polling). "
            "A job claim and a job done each store a row. "
            "A crib checkout and a crib return each store a row. "
            "Auth is a v1 session stub (Owner cookie/bearer; Member cookie), "
            "not OIDC. Demo data only — the shop is not open and there is no "
            "live payment processor."
        ),
    )
    register_error_handlers(application)
    application.add_middleware(ShopCorsMiddleware)
    application.add_middleware(SecurityHeadersMiddleware)

    application.include_router(auth.router)
    application.include_router(member.router)
    application.include_router(waitlist.router)
    application.include_router(signup.router)
    application.include_router(dashboard.router)
    application.include_router(tiers.router)
    application.include_router(members.router)
    application.include_router(hoists.router)
    application.include_router(incidents.router)
    application.include_router(bookings.router)
    application.include_router(staff.router)
    application.include_router(fill.router)
    application.include_router(jobs.router)
    application.include_router(chat.router)
    application.include_router(member_chat.router)
    application.include_router(todos.router)
    application.include_router(parts_requests.router)
    application.include_router(tool_crib.router)
    application.include_router(calendar.router)
    return application


app = create_app()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "project-car-api"}
