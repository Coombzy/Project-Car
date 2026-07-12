---
name: sqlalchemy-domain-modeling
description: Use when building a full set of SQLAlchemy ORM models (greenfield or new module). Covers Enum ordering, multi-FK relationships, nullable discipline, indexes, and post-generation verification. Triggers on requests for "SQLAlchemy models", "ORM schema", "domain models", or when fixing broken FK chains / circular enum imports.
trigger: When creating a new set of ORM models; when asked about SQLAlchemy 2.0 migrations; when fixing broken multi-FK relationships or circular enum imports.
---

# SQLAlchemy 2.0 Domain Modeling Skill

Produce production-grade SQLAlchemy 2.0 model sets using declarative\_base, Mapped/mapped\_column — not the legacy functional `declarative_base()`. Designed for greenfield domain models: IoT access-control → tools/hoist → token economy → incident detection → billing pipelines.

## Pre-flight checklist

1. **Read existing models first** if this module sits in an app with other tables — check naming conventions, Base class used, and enum patterns to maintain consistency.
2. **Plan FK chains** on paper: list every relationship, flag any entity with >1 FK to the same target table (these are the danger zones for circular references).

## Step-by-step pattern

### Phase 1: Imports & base setup

```python
from sqlalchemy import String, Integer, ..., ForeignKey, Index, Numeric, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
# Import only what you USE. Do NOT bulk-import Session or column_property "just in case".
```

Always inherit a custom `Base(DeclarativeBase)` that lives in this file. Never import/reuse a Base from another module unless explicitly told (leads to double-metadata issues in tests and Alembic).

### Phase 2: Enums (in dependency order!)

Define all Python enum classes **before** any model that references them. This is the #1 source of ImportError bugs — if Model B's column type references an Enum class defined after it, you get "NameError" at import time even before any query runs.

```python
class Status(str, Enum):  # inherit from str so native_enum=False text storage works
    ACTIVE = "active"
    INACTIVE = "inactive"
```

**CRITICAL:** `str` inheritance is mandatory when using `native\_enum=False`. Without it the dialect sees a Python enum (not a str) and can fail in SQLite/Firebird.

### Phase 3: Columns — nullable discipline

| Field type | Nullable? | When to null |
|---|---|---|
| PK | Never | N/A |
| FK to existing entity | `True` (SET NULL if ondelete) | Optional cross-links, soft-delete markers |
| String/Text | **False** unless genuinely optional | Names can be null during migrations |
| Integer/BigInteger | **False** with a sensible default (0) | Counters always have defaults |
| Numeric (money) | **False** when required; True as `default=0` | Prices, balances nullable during migration |
| DateTime | Use `server\_default=func.now()` for created | Onupdate timestamps use `onupdate=func.now()` |
| Boolean | Use `default=True/False`, never uninitialised | |

Pattern: prefer `nullable=False` + default. Nullable columns are a migration hazard — every query touching them needs `.optional()` or `isnot(None)` guards. Only leave null when the concept genuinely has "no value" (e.g., optional phone number).

### Phase 4: Relationships (CRITICAL)

#### Single-FK relationship (safe, standard):
```python
parent_obj = relationship("Parent", back_populates="children")
```

#### Multi-FK to same target → NEVER try to join all FKs into one relationship. This is the #1 bug class in SQLAlchemy modeling.

**WRONG ❌** (throws SQLAlchemy compilation error):
```python
booker = relationship("Member",
    primaryjoin="or_(member_id == foreign(Member.id), reported_by_member_id == ...)",
)
```

**RIGHT ✅** (split each FK into its own named relationship):
```python
subject: Mapped[Optional["Member"]] = relationship("Member", foreign_keys=[member_id], lazy="selectin")
reporter: Mapped["Member"] = relationship("Member", foreign_keys=[reported_by_member_id], back_populates="incidents_reported")
reviewer: Mapped[Optional["Member"]] = relationship("Member", foreign_keys=[reviewed_by_member_id])
```

Each FK column gets its own relationship with explicitly named `foreign_keys`. Back-populates flow the "natural" direction (one-to-many side names the back\_populates, many-to-one side gets the primary). Use string table names in `back_populates` to avoid circular import issues.

### Phase 5: Indexes

Always add:
- Unique on natural keys (`email`, `part_number`)
- Composite on high-query pairs (`(member_id, status)`, `(reader_location, timestamp)`)
- Single-column on enum/status columns that filter in >1 query

```python
__table_args__: dict = (
    Index("ix_table_col1", "column"),
    Index("ix_table_multi", "col1", "status"),
)
```

### Phase 6: Docstrings and __repr__/__str__

Every model class needs a docstring (2-3 lines on purpose, 1-2 on key FKs). Every model gets `__repr__` showing PK + meaningful field, and `__str__` for human display. Essential for debugging — Alembic migrations, ORM queries, and admin interfaces all call these:

```python
def __repr__(self) -> str:
    return f"<{self.__class__.__name__}(id={self.id!r})>"

def __str__(self) -> str:
    return self.name  # or human-readable composite
```

### Phase 7: Export and sanity-check block

At the bottom, list all classes in `ALL_MODELS` for Alembic autogenerate. Include an `if __name__ == "__main__"` block that iterates ALL\_MODELS and prints table names + column counts — this is your first-line import sanity check (catches missing class references immediately).

## Anti-patterns to avoid

1. **Multi-FK as one relationship** — see Phase 4 above. Fatal error, not just a warning.
2. **Circular Enum imports** — define all enums before any model that uses them, or use `native_enum=False` with string enum values.
3. **Bulk-importing unused ORM classes** — importing `Session`, `column_property` "just in case" pollutes your namespace and masks missing imports during refactoring. Import exactly what you use.
4. **Leaving nullable columns without defaults or null checks** — every nullable column is a query bug waiting to happen. Use `default` + `nullable=False` unless the value is genuinely optional per business logic.

## Post-generation checklist (ALWAYS run)

- [ ] All enums defined before their first use in a model
- [ ] Every multi-FK entity has separate named relationships, each with explicit `foreign_keys=[column]`
- [ ] No bulk imports of unused ORM constructs (`Session`, `column_property`)
- [ ] All models have `__repr__` and `__str__`
- [ ] `nullable=False` fields set sensible defaults
- [ ] Unique indexes on natural keys (email, SKU, etc.)
- [ ] ALL\_MODELS list is complete and in declaration order
- [ ] Run: `python models.py` — must print all tables without ImportError
