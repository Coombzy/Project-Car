"""Blank CSRF state must not start the Google OAuth flow."""

from urllib.parse import parse_qs, urlparse

from app.config import Settings
from app.services.calendar_oauth import google_authorize_url

S = Settings(google_oauth_client_id="cid", google_oauth_redirect_uri="https://example.test/cb")


def test_authorize_url_none_for_blank_state():
    assert google_authorize_url(S, state="") is None
    assert google_authorize_url(S, state="   ") is None


def test_authorize_url_keeps_nonblank_state():
    url = google_authorize_url(S, state="abc")
    assert url is not None
    assert parse_qs(urlparse(url).query)["state"] == ["abc"]
