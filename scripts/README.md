# scripts

- `next-row.sh` prints the first open row under Now in `Docs/queue.md`. An empty Now prints nothing. It does not merge, deploy, or wake a bot.
- `check-result.sh` prints the pull request to merge, or one later line, for a success or failure. It does not merge or wake a bot.
- `prove.sh` runs the shop proof suite from the repo root: `pytest -q` in `apps/project-car/api`, then `npm run lint` and `npm test` in `apps/project-car/web`. `scripts/prove.sh red` exits 0 when that suite fails and records the sha in `.agent-proof/proof.json`. `scripts/prove.sh green` exits 0 only when the suite passes and that file has a red with a nonzero exit on a different sha. It then prints `RED commit` and `GREEN commit` lines for the pull request body. `PROVE_CMD` replaces the suite.
- `pr-ready.sh` is a local preflight. It prints `READY` or `NOT_READY|reason` against `origin/main` (or a base you pass). It checks the branch, `.github/workflows`, deleted tests, new skip or xfail markers, secret files, diff size, a clean tree, and the proof suite. `--no-tests` skips the suite. `git fetch origin main` may fail quietly.
- `selftest-agent-scripts.sh` checks `prove.sh` and `pr-ready.sh` in a throwaway git repo. It uses `PROVE_CMD`, not the real suite.
