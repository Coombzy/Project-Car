# Multi-FK Modeling Patterns (Bug Traps)

## The "or-join" anti-pattern

Never use a single `relationship()` with an `or_` primaryjoin comparing two FK columns:

```python
# WRONG — SQLAlchemy cannot compile this; relationship to Member is ambiguous
booker = relationship("Member",
    primaryjoin="or_(member_id == foreign(Member.id), reported_by_member_id == foreign(Member.id))",
)
```

**Why it fails:** `primaryjoin` resolves a single FK column via the `foreign_keys` param. When you compare two different columns against the same target, SQLAlchemy cannot determine which FK owns the relationship. It throws `ArgumentError: Ambiguous foreign key columns for relationship`.

## Correct pattern: split by FK column

Each FK gets its own named relationship with explicit `foreign_keys`:

```python
# Entity C has member_id FK and reported_by_member_id FK both pointing to Member

member = relationship("Member", foreign_keys=[member_id], back_populates="incidents_as_subject")
reporter = relationship("Member", foreign_keys=[reported_by_member_id], back_populates="incident_reports")
reviewer = relationship("Member", foreign_keys=[reviewed_by_member_id])  # optional FK
```

## Naming convention for the one-to-many (back-populates) side

The target model should name relationships by their **semantic role**:

```python
# On Member class:
incidents_as_subject: Mapped[list["Incident"]] = relationship(
    "Incident", foreign_keys="[Incident.member_id]", back_populates="member"
)
incident_reports: Mapped[list["Incident"]] = relationship(
    "Incident", foreign_keys="[Incident.reported_by_member_id]", back_populates="reporter"
)
```

`incidents_as_subject` = incidents where this member **is the subject** (caused them).
`incident_reports` = incidents that this member **filed as a report**.

## Self-referential FK chains

When Entity A has FK→B and B also has FK→A, use `back_populates` with string names on both sides. Never use `primaryjoin` for simple bidirectional relationships — SQLAlchemy resolves the back-populate automatically:

```python
# Parent
children = relationship("Child", back_populates="parent")

# Child
parent = relationship("Parent", back_populates="children")  # no primaryjoin needed
```
