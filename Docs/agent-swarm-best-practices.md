# AI Agent and Swarm Best Practices

Applies to Cortana, Master Chief, Madcat, local models (Doc, Lightning, Porsche), Grok Build, and any future agents.

These practices come from recent research and production systems (Anthropic, OpenAI, AWS Strands, MAST failure study, token-efficiency papers, observability and security guides). They are filtered to what is useful for this fleet.

## 1. When to use multiple agents

Multi-agent systems can improve results on parallelizable or research-style tasks (reported gains up to ~90% in some Anthropic research setups) but often **lose** 39–70% on sequential reasoning and use ~15× the tokens of a normal chat.

**Use multiple agents when**
- The work can be cleanly split into independent pieces.
- You need different specializations or perspectives.
- Context isolation protects the lead agent from overflow.

**Prefer a single agent when**
- The steps are sequential and dependent.
- The task is small or deterministic.
- Token cost or debuggability matters more than coverage.

Default: start with one agent. Split only when you can name the specific constraint it removes.

## 2. Preferred coordination patterns

| Pattern | When to use | Notes |
|---------|-------------|-------|
| Supervisor + workers | Clear task boundaries, parallelizable work | Best default for this fleet. Lead assigns, workers return condensed results. |
| Sequential pipeline | Steps depend on previous output | Cheap and predictable. |
| Evaluator / critic loop | Quality matters and there is a clear rubric | Generator + critic. Cap iterations. |
| Pure swarm (peer-to-peer, no lead) | Rarely | High token cost, hard to debug, error amplification risk. Avoid for coding and compliance work. |

Hierarchical or supervisor patterns are safer than pure swarms for coding and business logic.

## 3. Context and token discipline

Context is scarce. Treat it as a budget.

- Give each agent only the context it needs (isolated or forked, not shared live windows).
- Workers return **summaries and decisions**, not raw transcripts or full file dumps.
- Prefer diffs and short prompts over pasting whole files.
- Externalize state (files, docs, metrics) instead of re-sending history every turn.
- Use prompt/prefix caching where available.
- Cap iterations and retries. Unbounded loops burn tokens fast.

Reported savings from structured handoffs + compression + selective forwarding: 60–85% in production systems.

## 4. Clear roles and handoffs

- Each agent has one primary responsibility (matches the coding structure guideline).
- Handoffs are structured: task, constraints, acceptance criteria, relevant facts. Not free-form chat.
- Lead agent verifies results without redoing the work.
- Define when an agent should stop and escalate to a human.

Vague briefs cause duplicated work and gaps (MAST failure study).

## 5. Proof and verification

- Mechanical checks (tests, type checks, invariant proofs) are preferred over agent self-assessment.
- RED then GREEN for code changes.
- Evaluator/critic loops only when the rubric is clear and iterations are capped.
- Audit trail: who did what, on which branch, at what token cost.

## 6. Local models vs cloud agents

- Use local models for mechanical work (diffs, small file edits, test generation) where context is limited and speed is acceptable.
- Use cloud agents (Cortana, etc.) for planning, review, and synthesis that needs larger context.
- Feed local models only the relevant files or diffs. Never the whole repo.
- Track metrics separately for local vs cloud (as already planned in the agent-scripts repo).

## 7. Observability and metrics

You need enough signal to answer “what happened, what did it cost, and was it correct?”

Minimum for this fleet:
- One trace / run ID per task.
- Tokens (in/out), latency, and success/failure per agent.
- Tool calls with arguments and results (not just the agent’s summary).
- Outcome check against real state (tests passed, PR opened, file exists) rather than only the transcript.
- Failures become regression cases or backlog rows.

Alert or flag when:
- Iteration or retry count exceeds a cap.
- Token use on a single task is unusually high.
- Repeated handoffs with no new progress.

This aligns with the metrics already planned in the agent-scripts repo. Keep local and cloud numbers separate.

## 8. Security and least privilege

- Give each agent only the tools and permissions it needs for the current task.
- Prefer read-only or scoped write (specific files or branches) over broad access.
- Do not let agents push to `main`, edit `.github/workflows`, or access secrets unless explicitly required and approved.
- Use sandboxing or worktrees where available so a bad change is contained.
- High-impact actions (merge, deploy, delete data, change permissions) require human approval.

Principle: least agency — only the autonomy needed for the task, for only as long as needed.

## 9. Human-in-the-loop

Three practical patterns:
- **Approval gate**: agent prepares, human must approve before irreversible action (merge, deploy, token spend above a threshold).
- **Review**: agent produces a PR or doc; human reviews before it is accepted.
- **Escalation**: agent stops and hands off with context when it is uncertain, missing information, or hits a policy boundary. Define the triggers explicitly (large diff, failing tests after one fix attempt, missing acceptance criteria) rather than relying on the agent to judge its own confidence.

For coding: agents open PRs. Humans (or Cortana after review) merge. Automated fix loops are capped at one pass; further issues escalate.

## 10. Failure modes to avoid

From research and this project:
- Stacked large PRs and god files (already seen in Project Car).
- Agents re-deriving the same information instead of reading a shared doc.
- No iteration or token caps.
- Pure peer swarms on sequential coding tasks.
- Missing proofs for invariants.
- Context rot from long shared conversations.
- Agents with broad permissions or no escalation path.

## 11. Practical rules for this fleet

1. Cortana (or the lead) writes or updates the brief / slice doc.
2. Local models or Grok Build implement the small RED/GREEN change.
3. Results come back as a short summary + proof output, not a long transcript.
4. Metrics (tokens, time, success) are recorded per agent.
5. If a task cannot be split cleanly, keep it on one agent.
6. High-impact actions require human approval.
7. Failures and high-cost runs are reviewed and turned into better briefs or tests.

These practices sit alongside the coding structure guidelines. Use both.
