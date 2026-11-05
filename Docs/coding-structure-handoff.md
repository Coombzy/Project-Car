# Handoff for Cortana: coding structure guidelines

## What was done
Created a coding structure best-practices guideline based on the issues found while reviewing Project Car (god files, large PRs, incomplete invariants).

## Document
- `Docs/coding-structure-guidelines.md` on branch `docs/coding-structure-guidelines`

## Scope
Applies to all apps (Project Car, pBay, Liquid Estate, and future apps).

## Key rules
- Keep source files under ~15–20 KB.
- Split by domain (models, schemas, services).
- Use re-exports so existing imports keep working.
- Small proof-driven PRs.
- Explicit tests for invariants (balances, unique constraints, no orphaned rows).
- Do not stack large feature branches.

## What to do next
- Review the guideline.
- Use it as the default for new work and for any split of large files.
- Point the local models and Grok Build at it when they are about to create or enlarge a file.
- Apply the same patterns to pBay and Liquid Estate.
