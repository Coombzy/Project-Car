# R172 visual recapture: text proof for PR #503

Review aid for [PR #503](https://github.com/Coombzy/Project-Car/pull/503). The png diff only says "Binary files differ". The green render and the pixel table are different checks.

## Green render on the reviewed head

- Png bytes were recaptured in `61ed23a6` and are the same at reviewed head `b7f51070d6ea0736939303d78b9ce52427553f36`. A later commit that only edits this file does not change them. Check: `git diff b7f51070 HEAD -- apps/project-car/web/visual/screenshots` is empty.
- Official CI on `b7f51070` was 3/3 green. `shop-web layout-shift / screenshots`: run [46035617670](https://github.com/Coombzy/Project-Car/actions/runs/46035617670), job 140630260712, success, completed 2026-11-27 10:45:04 America/Edmonton (16:45:04 UTC).
- That job runs `apply-baselines.sh`, then `npm run visual`. This PR edits `visual/screenshots/**`, so the script does not copy main's stored baselines over the checkout. It leaves the PR pngs in place and compares the fresh render to them. That is the intended CI path for a baseline recapture. Rendering against main's old goldens would fail by design, because the recapture exists to replace them.
- A pass means the fresh render matches those png bytes. It is not a pixel proof against main. The evidence against main is the table below. `git diff` of a png is only `Binary files differ` and does not contain the crop notes, so the diff text cannot support that column.
- `r62-error.png` is committed and no test compares it.

## Pixel diff against main

The table compares each changed png to the golden on main before this PR. 12 at 390, 14 at 768, 23 at 1440 (49). Owner `schedule.png` and `schedule-week.png` at 390, 768, and 1440 are byte-identical to main and are correctly left out of the 49. #500 (`6f787f60`) already recaptured all six with the Mountain Time eyebrow, and its 1440 shots already have the Refunds nav. Pixel cap 1% and layout-shift cap 0.1 are unchanged.

Paths are under `apps/project-car/web/visual/screenshots/`. No png changed size. "Exact" counts pixels where any RGB channel differs. "Visible" counts pixels where a channel differs by more than 3. The last column is a crop note, not text from the binary diff.

## Changed pngs

| PNG | Old = new size | Exact px (%) | Visible px | Crop note (not in the git diff) |
| --- | --- | --- | --- | --- |
| 390/fill.png | 390x844 | 590 (0.179%) | 564 | Eyebrow `AMERICA/REGINA` → `MOUNTAIN TIME`. |
| 390/home.png | 390x844 | 3715 (1.129%) | 3639 | Intro "Times are America/Regina" → "Times are Mountain Time" (reflows). Tokens at risk 3 → 1. |
| 390/login.png | 390x844 | 969 (0.294%) | 960 | Email field no longer prefilled with owner@projectcar.ca. `/member/login` link is now underlined. |
| 390/member-detail.png | 390x844 | 802 (0.244%) | 791 | Ada's token balance 156.25 → 375. |
| 390/member-home.png | 390x844 | 800 (0.243%) | 782 | Token balance 156.25 → 375. |
| 390/member-login.png | 390x844 | 1121 (0.341%) | 1095 | Email no longer prefilled with ada.reyes@example.com. `/login` link is now underlined. |
| 390/member-profile.png | 390x844 | 329160 (100%) | 100509 | Nav and link color gold → purple. Banner text beige → white. Background shifts slightly. Copy unchanged in the frame. |
| 390/member-schedule.png | 390x844 | 8210 (2.494%) | 7939 | Eyebrow `· AMERICA/REGINA` → `· MOUNTAIN TIME`. Tomorrow line "America/Regina" → "Mountain Time" (reflows). |
| 390/members.png | 390x844 | 599 (0.182%) | 586 | Token cells 156.25 → 375 and -12.50 → 150. |
| 390/not-found.png | 390x844 | 329160 (100%) | 32498 | Nav and "Dashboard" link gold → purple. Dismiss button border brighter. Background shifts slightly. Copy unchanged. |
| 390/signup.png | 390x844 | 36 (0.011%) | 36 | "Sign in" link gains an underline. |
| 390/tiers.png | 390x844 | 7922 (2.407%) | 7660 | Grant text "(America/Regina)" → "(Mountain Time)" (reflows). Band labels WEEKDAY DAY (BASE)/WEEKDAY EVENING → OFF-PEAK/NORMAL, with values 1/1.25 → 0.75/1. |
| 768/fill.png | 768x1024 | 590 (0.075%) | 565 | Eyebrow `AMERICA/REGINA` → `MOUNTAIN TIME`. |
| 768/home.png | 768x1024 | 2400 (0.305%) | 2339 | Intro "America/Regina" → "Mountain Time". Tokens at risk 3 → 1. |
| 768/jobs.png | 768x1024 | 40 (0.005%) | 0 | Nothing visible. 40 pixels drift by 3 or less. |
| 768/login.png | 768x1024 | 962 (0.122%) | 953 | Email no longer prefilled. `/member/login` link is now underlined. |
| 768/member-detail.png | 768x1024 | 9045 (1.150%) | 791 | Token balance 156.25 → 375. The rest is faint drift of 3 or less in the header. |
| 768/member-home.png | 768x1024 | 2639 (0.336%) | 782 | Token balance 156.25 → 375. The rest is faint drift. |
| 768/member-jobs.png | 768x1024 | 25 (0.003%) | 0 | Nothing visible. 25 pixels drift by 3 or less. |
| 768/member-login.png | 768x1024 | 1121 (0.143%) | 1095 | Email no longer prefilled. `/login` link is now underlined. |
| 768/member-profile.png | 768x1024 | 786432 (100%) | 121206 | Nav and link color gold → purple. Banner text beige → white. Token balance 156.25 → 375. |
| 768/member-schedule.png | 768x1024 | 31744 (4.036%) | 4417 | Eyebrow and tomorrow line America/Regina → Mountain Time. The rest is faint drift. |
| 768/members.png | 768x1024 | 4431 (0.563%) | 4246 | Tokens 156.25→375, -12.50→150, -187.50→-150, 437.50→550, 87.50→150 (0 unchanged). |
| 768/not-found.png | 768x1024 | 786432 (100%) | 39387 | Nav and "Dashboard" link gold → purple. Background shifts slightly. Copy unchanged. |
| 768/signup.png | 768x1024 | 36 (0.005%) | 36 | "Sign in" link gains an underline. |
| 768/tiers.png | 768x1024 | 1107 (0.141%) | 1059 | Grant text "(America/Regina)" → "(Mountain Time)". |
| 1440/cameras.png | 1440x900 | 1706 (0.132%) | 1657 | Admin nav gains "Refunds" between Payments and Tiers. |
| 1440/chat.png | 1440x900 | 1706 (0.132%) | 1657 | Admin nav gains "Refunds". |
| 1440/chat-room.png | 1440x900 | 1706 (0.132%) | 1657 | Admin nav gains "Refunds". |
| 1440/drafts.png | 1440x900 | 1810 (0.140%) | 1762 | Admin nav gains "Refunds". |
| 1440/fill.png | 1440x900 | 2334 (0.180%) | 2262 | Admin nav gains "Refunds". Eyebrow `AMERICA/REGINA` → `MOUNTAIN TIME`. |
| 1440/hoists.png | 1440x900 | 1706 (0.132%) | 1657 | Admin nav gains "Refunds". |
| 1440/home.png | 1440x900 | 4118 (0.318%) | 4009 | Admin nav gains "Refunds". Intro America/Regina → Mountain Time. Tokens at risk 3 → 1. |
| 1440/jobs.png | 1440x900 | 1706 (0.132%) | 1657 | Admin nav gains "Refunds". |
| 1440/login.png | 1440x900 | 139842 (10.790%) | 77820 | Demo banner drops the "Password changeme" line, so the card is shorter. Email and password fields are empty. |
| 1440/member-detail.png | 1440x900 | 2508 (0.194%) | 2448 | Admin nav gains "Refunds". Token balance 156.25 → 375. |
| 1440/member-home.png | 1440x900 | 3332 (0.257%) | 791 | Token balance 156.25 → 375. The rest is faint drift. |
| 1440/member-login.png | 1440x900 | 136303 (10.517%) | 74178 | Banner drops "Password changeme". Email and password fields are empty. |
| 1440/member-profile.png | 1440x900 | 1296000 (100%) | 150160 | Nav and link color gold → purple. Banner text beige → white. Token balance 156.25 → 375. |
| 1440/member-schedule.png | 1440x900 | 42574 (3.285%) | 7611 | Eyebrow and tomorrow line America/Regina → Mountain Time. The rest is faint drift. |
| 1440/members.png | 1440x900 | 7859 (0.606%) | 7569 | Admin nav gains "Refunds". Same token column changes as 768. |
| 1440/not-found.png | 1440x900 | 1296000 (100%) | 69188 | Nav gold → purple, admin nav gains "Refunds", and the "Dashboard" link is purple. Copy otherwise unchanged. |
| 1440/parts.png | 1440x900 | 1706 (0.132%) | 1657 | Admin nav gains "Refunds". |
| 1440/payments.png | 1440x900 | 1706 (0.132%) | 1657 | Admin nav gains "Refunds". |
| 1440/requests.png | 1440x900 | 1857 (0.143%) | 1809 | Admin nav gains "Refunds". |
| 1440/signup.png | 1440x900 | 43 (0.003%) | 43 | "Sign in" link gains an underline. |
| 1440/tiers.png | 1440x900 | 7866 (0.607%) | 7536 | Admin nav gains "Refunds". Grant text → "(Mountain Time)". Bands now OFF-PEAK 0.75, NORMAL 1, EVENING 1.25, PEAK 1.50. |
| 1440/tools.png | 1440x900 | 1706 (0.132%) | 1657 | Admin nav gains "Refunds". |
| 1440/waitlist.png | 1440x900 | 1821 (0.141%) | 1791 | Admin nav gains "Refunds". |

## Trimmed log

This trimmed log is the earlier local run on `563d74af` (PR head `61ed23a6` merged with main `af09273e`). It is not the CI attestation. That attestation is run 46035617670 on `b7f51070`, above. The png bytes are the same. Full stdout and stderr were 123 lines. Removed: four uvicorn startup lines, repeated `NO_COLOR` warnings, and the 390 and 768 pass lines, which have the same 33 test titles as 1440.

```text
> project-car-web@0.1.0 visual
> node --experimental-strip-types ../../../scripts/ui-proof.ts
Running 102 tests using 1 worker
  [tests 1-33: [390] pages.spec.ts, the same 33 titles as 69-101 below, all ✓]
  -   34 [390] › visual/text-drift.spec.ts:44:5 › 1440 owner body matches the frozen clock
  [tests 35-67: [768] pages.spec.ts, the same 33 titles as 69-101 below, all ✓]
  -   68 [768] › visual/text-drift.spec.ts:44:5 › 1440 owner body matches the frozen clock
  ✓   69 [1440] › visual/pages.spec.ts:200:9 › public pages › login (1.6s)
  ✓   70 [1440] › visual/pages.spec.ts:200:9 › public pages › member-login (1.6s)
  ✓   71 [1440] › visual/pages.spec.ts:200:9 › public pages › signup (1.6s)
  ✓   72 [1440] › visual/pages.spec.ts:214:9 › owner pages › home (1.7s)
  ✓   73 [1440] › visual/pages.spec.ts:214:9 › owner pages › cameras (1.6s)
  ✓   74 [1440] › visual/pages.spec.ts:214:9 › owner pages › chat (1.6s)
  ✓   75 [1440] › visual/pages.spec.ts:214:9 › owner pages › drafts (1.6s)
  ✓   76 [1440] › visual/pages.spec.ts:214:9 › owner pages › requests (1.6s)
  ✓   77 [1440] › visual/pages.spec.ts:214:9 › owner pages › fill (1.6s)
  ✓   78 [1440] › visual/pages.spec.ts:214:9 › owner pages › hoists (1.6s)
  ✓   79 [1440] › visual/pages.spec.ts:214:9 › owner pages › jobs (1.6s)
  ✓   80 [1440] › visual/pages.spec.ts:214:9 › owner pages › members (1.6s)
  ✓   81 [1440] › visual/pages.spec.ts:214:9 › owner pages › not-found (1.6s)
  ✓   82 [1440] › visual/pages.spec.ts:214:9 › owner pages › parts (1.6s)
  ✓   83 [1440] › visual/pages.spec.ts:214:9 › owner pages › payments (1.6s)
  ✓   84 [1440] › visual/pages.spec.ts:214:9 › owner pages › schedule (2.0s)
  ✓   85 [1440] › visual/pages.spec.ts:214:9 › owner pages › schedule-week (2.0s)
  ✓   86 [1440] › visual/pages.spec.ts:214:9 › owner pages › tiers (1.6s)
  ✓   87 [1440] › visual/pages.spec.ts:214:9 › owner pages › tools (1.6s)
  ✓   88 [1440] › visual/pages.spec.ts:214:9 › owner pages › waitlist (1.6s)
  ✓   89 [1440] › visual/pages.spec.ts:219:7 › owner pages › member-detail (1.6s)
  ✓   90 [1440] › visual/pages.spec.ts:223:7 › owner pages › chat-room (1.6s)
  ✓   91 [1440] › visual/pages.spec.ts:227:7 › owner pages › 2-hour chip actions (423ms)
  ✓   92 [1440] › visual/pages.spec.ts:239:7 › owner pages › R173 owner jobs does not scroll sideways (4.2s)
  ✓   93 [1440] › visual/pages.spec.ts:275:9 › member pages › member-home (1.6s)
  ✓   94 [1440] › visual/pages.spec.ts:275:9 › member pages › member-cameras (1.6s)
  ✓   95 [1440] › visual/pages.spec.ts:275:9 › member pages › member-chat (1.6s)
  ✓   96 [1440] › visual/pages.spec.ts:275:9 › member pages › member-jobs (1.6s)
  ✓   97 [1440] › visual/pages.spec.ts:275:9 › member pages › member-parts (1.6s)
  ✓   98 [1440] › visual/pages.spec.ts:275:9 › member pages › member-profile (1.5s)
  ✓   99 [1440] › visual/pages.spec.ts:275:9 › member pages › member-schedule (1.9s)
  ✓  100 [1440] › visual/pages.spec.ts:280:7 › member pages › member-chat-room (1.6s)
  ✓  101 [1440] › visual/pages.spec.ts:284:7 › member pages › member-not-found (1.5s)
  ✓  102 [1440] › visual/text-drift.spec.ts:44:5 › 1440 owner body matches the frozen clock (475ms)
::notice title=🎭 Playwright Run Summary::  2 skipped%0A  100 passed (2.8m)
  2 skipped
  100 passed (2.8m)
```
