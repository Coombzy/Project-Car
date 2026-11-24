"""Guard against redeclaring a field on Settings (the Project-Car #333 miss)."""

import ast
from collections import Counter
from pathlib import Path

CONFIG = Path(__file__).resolve().parents[1] / "app" / "config.py"


def _field_names(node: ast.ClassDef) -> list[str]:
    """Names bound directly in the class body: AnnAssign and Assign targets."""
    names: list[str] = []
    for stmt in node.body:
        if isinstance(stmt, ast.AnnAssign) and isinstance(stmt.target, ast.Name):
            names.append(stmt.target.id)
        elif isinstance(stmt, ast.Assign):
            for target in stmt.targets:
                if isinstance(target, ast.Name):
                    names.append(target.id)
    return names


def duplicate_fields(source: str, class_name: str = "Settings") -> list[str]:
    """Field names declared more than once in the top-level body of class_name."""
    for node in ast.parse(source).body:
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            counts = Counter(_field_names(node))
            return sorted(name for name, count in counts.items() if count > 1)
    raise AssertionError(f"class {class_name} not found in source")


def test_mutant_redeclarations_are_caught():
    src = """
class Settings:
    shop_dev_mode: bool = False
    cookie_secure: bool | None = None
    shop_dev_mode: bool = False
"""
    assert duplicate_fields(src) == ["shop_dev_mode"]


def test_current_settings_field_names_are_unique():
    assert duplicate_fields(CONFIG.read_text()) == []
