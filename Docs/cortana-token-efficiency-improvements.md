# Cortana Token Efficiency Improvements

**Date:** 2026-11-04  
**Status:** Proposed for Master Chief + Cortana to implement  
**Goal:** Reduce Grok Bot token burn from Cortana (largest current consumer) while preserving her ability to drive the repos to done.

This document consolidates the efficiency recommendations from the multi-agent review. Master Chief should work with Cortana to update her rules / rulebook and operating procedures.

## Highest impact

1. **Force more work onto Grok Build CLI + local models.**
   - Any task involving reading more than a couple of files, running tests, generating large patches, or exploring the repos *must* go through Grok Build CLI or a local Qwen/Bonsai model (on the M4 Pro or M1 Max) first.
   - Cortana should only wake for high-level decisions, merge judgment, or when Build explicitly fails after retries.

2. **Shrink context.**
   - Never re-read an entire repo or large file unless the previous summary is older than 24 h or a major change landed.
   - Always prefer the latest short status file or diff.
   - Maintain a single living `STATUS.md` (or equivalent) per repo, updated in 5–10 lines after each meaningful change.

3. **Tighten the daily report.**
   - Change the ~7:12 PM report to a strict format: 3–5 bullets max (merged, in-flight, blockers, next).
   - No narrative or “what I tried” unless it is a real blocker that needs Ben.
   - Everything else stays internal or goes to Master Chief.

## Medium impact

- **Batch non-urgent questions and decisions** into one short daily batch instead of multiple small messages.
- **Local model first for exploration.** Use Bonsai 2 / Qwen3.8-27B (or the 35B-A3B distill) for first-pass code reading, summarization, and draft patches. Only the final review or hard architectural call goes to the Grok bot.
- **Parallel slices stay on Build.** Multiple parallel agents should be Grok Build or Cursor cloud agents, not additional Grok Bot turns.

## Hygiene

- Shorten any remaining long instructions in her rulebook (`/home/box/cortana/rulebook.md`). Replace multi-paragraph guidance with one-line rules.
- Explicitly ban status-style messages (“Working on X…”, “Almost done…”) even internally if they generate extra turns.
- Prefer structured, short outputs (delta / action items / changed files) over long narratives.

## Local model speed context (for planning)

On the available MacBooks (approximate, community + measured data):

- **M4 Pro 24 GB (Porsche):** Qwen3.8-27B class ~100–250 tok/s prefill (reading code), ~8–15 tok/s generation (higher with good MTP). Bonsai 2 ternary is a strong fit.
- **M1 Max 64 GB (Doc):** Significantly higher; MoE models (e.g. Qwen3.6-35B-A3B) can reach 50–80+ tok/s generation with MTP; prefill hundreds of tok/s.

Reading a medium file or focused repo slice is practical. Full-repo dumps should still be chunked.

## Next steps for Master Chief + Cortana

1. Review and adopt the rules above into Cortana’s standing instructions / rulebook.
2. Confirm a short STATUS.md update pattern per repo.
3. Adjust the daily report template.
4. Report back once the changes are live.

---

*Prepared from multi-agent review for Ben / Master Chief. Canonical location: `Docs/cortana-token-efficiency-improvements.md`.*
