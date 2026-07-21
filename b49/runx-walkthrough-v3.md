# Run Your First Governed Agent Skill with runx

A practical field note for developers who want to build portable, verifiable agent skills — the kind that produce cryptographically sealed receipts instead of just text output.

## What runx Actually Does

runx is an open-source runtime that turns a plain Markdown file (`SKILL.md`) plus a small YAML graph definition (`X.yaml`) into a **governed skill** — a unit of agent work that is reproducible, auditable, and sealable. Think of it as "unit tests for agent behavior" that produce immutable receipts.

## The Two-File Shape

Every runx skill needs only two files:

```
skills/my-skill/
  SKILL.md    # What the skill does (YAML frontmatter + markdown body)
  X.yaml      # How to run it (graph steps, harness cases)
```

`SKILL.md` is the human-readable contract. `X.yaml` defines the execution graph — what runners to invoke, what inputs they need, and at least two harness cases (one happy path, one negative/stop case).

## The Local Proof Gate: `runx harness`

Before publishing, you must prove the skill works:

```bash
runx harness skills/my-skill
```

This runs every case defined in `X.yaml` and reports `status: passed` only if ALL cases succeed. The harness is the **local proof** — without it, a published skill will be rejected by the runx registry's verification.

**Critical `expect.status` values** (from live rejection experience, not docs):
- `sealed` — graph step completed and receipt sealed (normal happy path)
- `failure` — graph step process-failure
- `needs_agent` — agent runner with no `caller.answers`
- `policy_denied` — policy guard mismatch
- `escalated` — explicit escalation

`failed` is **NOT valid** — it is an internal graph state, not a harness expectation. Using it causes "unknown status" rejection.

## The Remote Publish Trap

This burned us: `runx registry publish ./skills/my-skill/SKILL.md` publishes LOCALLY only. The skill appears to work, but nobody else can reach it.

To publish publicly:

```bash
runx registry publish ./skills/my-skill/SKILL.md --registry https://api.runx.ai
```

The `--registry` flag is mandatory. Without it, your `public_url` will 404 for reviewers.

## Why This Matters

Governed skills aren't just prompts — they're **verifiable work artifacts** that prove an agent actually executed something under defined constraints. The receipt (`runx:receipt:sha256:<hash>`) is a cryptographic proof that can be independently verified.

If you're building agents that need to prove what they did, runx gives you that proof in a portable, open-source format.

---

*Links: [runx.ai](https://runx.ai) · [github.com/runxhq/runx](https://github.com/runxhq/runx)*
