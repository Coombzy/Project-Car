"""Guard: every Settings field with a placeholder default must be checked by
assert_runtime_secrets. #332 shipped member_demo_password = "changeme" unguarded."""

import ast
from pathlib import Path

import pytest

from app.config import Settings, _DEMO_SECRETS, assert_runtime_secrets

CONFIG = Path(__file__).resolve().parents[1] / "app" / "config.py"


def _const(node):
    if isinstance(node, ast.Constant):
        return node.value
    if isinstance(node, (ast.Tuple, ast.List)):
        vals = [_const(e) for e in node.elts]
        return tuple(vals) if isinstance(node, ast.Tuple) else vals


def _strings(value):
    return {value} if isinstance(value, str) else {
        i for e in (value if isinstance(value, (tuple, list)) else ()) for i in _strings(e)}


def _assignments(stmts):
    for stmt in stmts:
        if isinstance(stmt, (ast.Assign, ast.AnnAssign)) and stmt.value is not None:
            value = _const(stmt.value)
            targets = stmt.targets if isinstance(stmt, ast.Assign) else [stmt.target]
            for target in targets:
                if isinstance(target, ast.Name) and value is not None:
                    yield target.id, value


def placeholder_fields(source: str) -> set[str]:
    """Settings fields whose default is in _DEMO_SECRETS or starts with CHANGE_ME."""
    tree = ast.parse(source)
    demo = _strings(dict(_assignments(tree.body)).get("_DEMO_SECRETS", ()))
    return {name for cls in ast.walk(tree)
            if isinstance(cls, ast.ClassDef) and cls.name == "Settings"
            for name, value in _assignments(cls.body)
            if isinstance(value, str) and (value in demo or value.startswith("CHANGE_ME"))}


def guarded_names(source: str) -> set[str]:
    """Field names the assert_runtime_secrets loop iterates over."""
    tree = ast.parse(source)
    consts = dict(_assignments(tree.body))
    names = set()
    for fn in ast.walk(tree):
        if isinstance(fn, ast.FunctionDef) and fn.name == "assert_runtime_secrets":
            for loop in ast.walk(fn):
                if isinstance(loop, ast.For):
                    it = loop.iter
                    if isinstance(it, ast.Name):
                        it = ast.Constant(value=consts.get(it.id))
                    names |= _strings(_const(it))
    return names


def assert_placeholders_guarded(source: str, label: str) -> None:
    missing = placeholder_fields(source) - guarded_names(source)
    if missing:
        raise AssertionError(f"{label}: placeholder fields missing from guard loop: {sorted(missing)}")


# Mutant: a guard loop that skips extra_password, whose default is a placeholder.
MUTANT = '''
_DEMO_SECRETS = ("dev-owner-secret", "dev-ai-secret", "dev-session-secret-change-me", "changeme")
class Settings:
    shop_dev_mode = False
    owner_api_secret = "dev-owner-secret"
    extra_password = "changeme"
def assert_runtime_secrets(settings):
    if settings.shop_dev_mode:
        return
    for name, length in (("owner_api_secret", 32),):
        value = getattr(settings, name)
        if len(value) < length or value in _DEMO_SECRETS or value.startswith("CHANGE_ME"):
            raise RuntimeError(name)
'''


def test_mutant_missing_placeholder_is_caught():
    assert placeholder_fields(MUTANT) == {"owner_api_secret", "extra_password"}
    assert guarded_names(MUTANT) == {"owner_api_secret"}
    with pytest.raises(AssertionError, match="extra_password"):
        assert_placeholders_guarded(MUTANT, "mutant fixture")


def test_current_settings_placeholder_defaults_are_guarded():
    found = placeholder_fields(CONFIG.read_text())
    assert "member_demo_password" in found, "#332 field must stay visible to this guard"
    assert found == {n for n, f in Settings.model_fields.items() if isinstance(f.default, str)
                     and (f.default in _DEMO_SECRETS or f.default.startswith("CHANGE_ME"))}
    assert_placeholders_guarded(CONFIG.read_text(), str(CONFIG))
    with pytest.raises(RuntimeError):
        assert_runtime_secrets(Settings(shop_dev_mode=False, member_demo_password="changeme"))


# Other required secrets stay strong so only shop_proxy_secret can trip the guard.
_STRONG = {
    "owner_api_secret": "y" * 32,
    "ai_api_secret": "y" * 32,
    "session_secret": "y" * 32,
    "owner_password": "y" * 12,
    "member_demo_password": "y" * 12,
}


def test_aud010_shop_proxy_secret_placeholder_refused_outside_dev():
    """Empty SHOP_PROXY_SECRET starts. A placeholder or dummy secret does not, unless dev mode."""
    for secret in (*_DEMO_SECRETS, "CHANGE_ME", "CHANGE_ME_shop_proxy"):
        with pytest.raises(RuntimeError) as exc:
            assert_runtime_secrets(Settings(shop_dev_mode=False, shop_proxy_secret=secret, **_STRONG))
        message = str(exc.value)
        assert "shop_proxy_secret" in message
        assert "SHOP_PROXY_SECRET" in message
        assert secret not in message
    assert_runtime_secrets(Settings(shop_dev_mode=False, shop_proxy_secret="", **_STRONG))
    assert_runtime_secrets(Settings(shop_dev_mode=False, shop_proxy_secret="y" * 32, **_STRONG))
    assert_runtime_secrets(Settings(shop_dev_mode=True, shop_proxy_secret="changeme"))
