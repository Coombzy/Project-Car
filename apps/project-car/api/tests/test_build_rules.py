from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]

REQUIRED_LINES = (
    "The suite is the sign-off.",
    "The writer does not sign off.",
    "A failing check cannot merge.",
    "The failing proof runs before the feature code.",
    "The red output is in the pass.",
    "in the same pull request.",
    "Do not add a review note.",
    "Do not auto-apply review-bot comments.",
    "One writer on shared files.",
    "Do not deploy Doc.",
    "Do not say the shop is open.",
)


def test_build_rules_name_the_sign_off() -> None:
    text = (ROOT / "Docs" / "build-rules.md").read_text()
    missing = [line for line in REQUIRED_LINES if line not in text]
    assert missing == []
