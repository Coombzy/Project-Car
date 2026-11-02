<!-- Fill every field. Scripts read these lines: keep the "Field:" labels exactly. -->
Row: <!-- the row id from your brief; exactly one row per PR -->
Difficulty: <!-- [D# · S# C# R# T#], each 1–9: S size, C context, R risk, T test clarity; D = highest -->
Agent: <!-- your Cursor cloud-agent id (bc-…), "grok-build", or "local" -->

## What changed
<!-- 1–3 lines: baseline -> target. What must not get worse. -->

## Files
<!-- one path per line; explain any file the brief didn't name -->

## Tests run
<!-- e.g. scripts/pr-ready.sh -> READY; the related tests you ran -->

## Proof
<!-- paste the scripts/prove.sh green output: -->
RED commit: <!-- sha (test only, fails on main) -->
GREEN commit: <!-- sha -->
<!-- UI changes: before/after screenshots at 390 and 1440 px, hosted links (not committed) -->

## Merge conditions
<!-- One machine-checkable line each. Kinds: ci-green | red-green | file-exists <path> |
     file-contains <path> <text> | file-absent <path> | body-contains <text> -->
IF: ci-green
IF: red-green
