import unittest

from app.auth import Principal
from app.config import Settings
from app.services.calendar_oauth import calendar_payload

HINT = "Download the ICS for a to-do due date. Apple Calendar has no public OAuth in this slice."
NEXT = (
    "Two-way Google Calendar sync needs GOOGLE_OAUTH_CLIENT_ID, "
    "GOOGLE_OAUTH_CLIENT_SECRET, and a registered redirect on ops. "
    "Apple stays ICS import until a CalDAV path is locked."
)


class FakeSession:
    def scalars(self, _stmt):
        return self

    def first(self):
        return None


class TestCalendarPayload(unittest.TestCase):
    def test_apple_is_ics_only_and_google_ready_follows_settings(self) -> None:
        owner = Principal(role="owner", email="owner@example.com")
        empty = calendar_payload(
            FakeSession(),
            owner,
            Settings(google_oauth_client_id="", google_oauth_redirect_uri=""),
        )
        self.assertEqual(empty["google"]["label"], "Connect Google Calendar")
        self.assertFalse(empty["google"]["ready"])
        self.assertFalse(empty["google"]["connected"])
        self.assertEqual(empty["google"]["status"], "disconnected")
        self.assertFalse(empty["apple"]["connected"])
        self.assertEqual(empty["apple"]["status"], "ics_only")
        self.assertTrue(empty["apple"]["ready"])
        self.assertEqual(empty["apple"]["label"], "Add to Apple Calendar")
        self.assertEqual(empty["apple"]["hint"], HINT)
        self.assertEqual(empty["next"], NEXT)

        ready = calendar_payload(
            FakeSession(),
            owner,
            Settings(
                google_oauth_client_id="cid",
                google_oauth_redirect_uri="https://example.test/cb",
            ),
        )
        self.assertTrue(ready["google"]["ready"])
