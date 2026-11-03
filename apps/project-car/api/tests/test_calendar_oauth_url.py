"""Tests for google_authorize_url in calendar_oauth."""

from urllib.parse import parse_qs, urlparse

from app.config import Settings
from app.services.calendar_oauth import GOOGLE_AUTH, GOOGLE_SCOPES, google_authorize_url


def test_authorize_url_none_without_client_or_redirect():
    assert google_authorize_url(Settings(google_oauth_client_id="", google_oauth_redirect_uri="https://example.test/cb"), state="s") is None
    assert google_authorize_url(Settings(google_oauth_client_id="cid", google_oauth_redirect_uri=""), state="s") is None


def test_authorize_url_has_expected_query_params():
    url = google_authorize_url(Settings(google_oauth_client_id="cid", google_oauth_redirect_uri="https://example.test/cb"), state="mystate")
    assert url.startswith(GOOGLE_AUTH)
    qs = parse_qs(urlparse(url).query)
    assert qs["client_id"] == ["cid"]
    assert qs["redirect_uri"] == ["https://example.test/cb"]
    assert qs["response_type"] == ["code"]
    assert qs["scope"] == [GOOGLE_SCOPES]
    assert qs["state"] == ["mystate"]
