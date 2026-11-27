import unittest
from types import SimpleNamespace

from app.auth import Principal
from app.models import CalendarProvider
from app.services.calendar_oauth import connection_status


class FakeSession:
    def __init__(self, row=None):
        self._row = row

    def scalars(self, _stmt):
        return self

    def first(self):
        return self._row


class TestConnectionStatus(unittest.TestCase):
    def setUp(self) -> None:
        self.owner = Principal(role="owner", email="owner@example.com")

    def test_missing_row_is_disconnected(self) -> None:
        self.assertEqual(
            connection_status(FakeSession(), self.owner, CalendarProvider.GOOGLE),
            "disconnected",
        )

    def test_returns_the_row_status(self) -> None:
        for status in ("connected", "pending"):
            row = SimpleNamespace(status=status)
            self.assertEqual(
                connection_status(FakeSession(row), self.owner, CalendarProvider.GOOGLE),
                status,
            )


if __name__ == "__main__":
    unittest.main()
