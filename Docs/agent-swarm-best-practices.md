# AI Agent and Swarm Best Practices

Applies to Cortana, Master Chief, Madcat, local models (Doc, Lightning, Porsche), Grok Build, and any future agents.

These practices come from recent research and production systems (Anthropic, OpenAI, AWS Strands, MAST failure study, token-efficiency papers). They are filtered to what is useful for this fleet.

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

## 7. Failure modes to avoid

From research and this project:
- Stacked large PRs and god files (already seen in Project Car).
- Agents re-deriving the same information instead of reading a shared doc.
- No iteration or token caps.
- Pure peer swarms on sequential coding tasks.
- Missing proofs for invariants.
- Context rot from long shared conversations.

## 8. Practical rules for this fleet

1. Cortana (or the lead) writes or updates the brief / slice doc.
2. Local models or Grok Build implement the small RED/GREEN change.
3. Results come back as a short summary + proof output, not a long transcript.
4. Metrics (tokens, time, success) are recorded per agent.
5. If a task cannot be split cleanly, keep it on one agent.

These practices sit alongside the coding structure guidelines. Use both.
