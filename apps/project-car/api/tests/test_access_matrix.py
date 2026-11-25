"""Frozen public-vs-authenticated HTTP APIRoutes (PC-AUD-030)."""
from fastapi.routing import APIRoute
from app.deps import require_member, require_owner, require_principal
from app.main import app

_AUTH = (require_owner, require_member, require_principal)
# Unauthenticated (METHOD, path) on origin/main. Authenticated routes are not listed.
PUBLIC_ROUTES = frozenset({
    ("GET", "/calendar/apple/start"), ("GET", "/calendar/google/callback"),
    ("GET", "/health"), ("GET", "/signup-mode"),
    ("POST", "/auth/login"), ("POST", "/auth/logout"),
    ("POST", "/auth/member/login"), ("POST", "/auth/member/logout"),
    ("POST", "/signup"), ("POST", "/waitlist"),
})

def _authed(node, seen):
    if node is None or id(node) in seen:
        return False
    seen.add(id(node))
    hit = getattr(node, "call", None) in _AUTH or getattr(node, "dependency", None) in _AUTH
    return hit or any(_authed(sub, seen) for sub in (getattr(node, "dependencies", None) or ()))

def _routes():
    stack = list(app.routes)
    while stack:
        node = stack.pop()
        if isinstance(node, APIRoute) or isinstance(getattr(node, "original_route", None), APIRoute):
            yield node
        elif callable(expand := getattr(node, "effective_candidates", None)):
            stack.extend(expand())

def _split():
    public, authed, present = set(), set(), set()
    for route in _routes():
        pairs = {(m.upper(), route.path) for m in (route.methods or ())}
        present |= pairs
        deps = (getattr(route, "dependant", None), *(getattr(route, "dependencies", None) or ()))
        (authed if any(_authed(d, set()) for d in deps) else public).update(pairs)
    return public, authed, present

def test_unlisted_http_route_is_not_public():
    public, _, _ = _split()
    assert public <= PUBLIC_ROUTES, sorted(public - PUBLIC_ROUTES)

def test_frozen_public_routes_stay_open_and_present():
    public, authed, present = _split()
    missing, gained = PUBLIC_ROUTES - present, PUBLIC_ROUTES & authed
    assert not missing, sorted(missing)
    assert not gained, sorted(gained)
    assert PUBLIC_ROUTES <= public
