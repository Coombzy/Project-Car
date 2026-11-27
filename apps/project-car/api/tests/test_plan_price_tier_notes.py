"""0019 moves leftover demo prices. Placeholder notes pick up the Premium mark."""
from __future__ import annotations
import importlib.util
from pathlib import Path
from alembic.config import Config
from alembic.operations import Operations
from alembic.runtime.migration import MigrationContext
from alembic.script import ScriptDirectory
from sqlalchemy import create_engine, text
from app.services.plan_price import PREMIUM_PRICE_MARK, tier_notes

def test_plan_price_tier_notes() -> None:
    root = Path(__file__).resolve().parents[1]
    script = ScriptDirectory.from_config(Config(str(root / "alembic.ini")))
    assert script.get_revision("20261031_0019").down_revision == "20261031_0018"
    basic = tier_notes(premium=False, included_tokens=1000, base_tokens_per_hour=100)
    premium = tier_notes(premium=True, included_tokens=1500, base_tokens_per_hour=100)
    assert premium.startswith(PREMIUM_PRICE_MARK) and PREMIUM_PRICE_MARK not in basic
    spec = importlib.util.spec_from_file_location("stand_in", root / "alembic/versions/20261031_0019_plan_price_stand_in.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    engine = create_engine("sqlite://")
    placeholder = "Placeholder. Owner can edit."
    seed = [("basic", "150.00", placeholder), ("premium", "250.00", placeholder), ("basic", "180.00", placeholder), ("premium", "640.00", "Owner wrote this.")]
    with engine.begin() as conn:
        conn.execute(text("CREATE TABLE membership_tiers (name TEXT, price TEXT, notes TEXT)"))
        conn.execute(text("INSERT INTO membership_tiers (name, price, notes) VALUES (:n, :p, :o)"), [{"n": n, "p": p, "o": o} for n, p, o in seed])
        with Operations.context(MigrationContext.configure(conn)):
            module.upgrade()
        found = conn.execute(text("SELECT name, price, notes FROM membership_tiers ORDER BY rowid")).all()
    assert list(found) == [("basic", "500.00", basic), ("premium", "750.00", premium), ("basic", "180.00", basic), ("premium", "640.00", "Owner wrote this.")]
