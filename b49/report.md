# #49 — Give runx some love

## What was published
A fresh public field walkthrough: "Run Your First Governed Agent Skill with runx" — hosted at a durable GitHub raw URL.

## What it covers
- The two-file skill shape (SKILL.md + X.yaml)
- The local proof gate: `runx harness` and exact `expect.status` values (learned from live rejection — `failed` is NOT valid; use `sealed|failure|needs_agent|policy_denied|escalated`)
- The remote publish trap (mandatory `--registry https://api.runx.ai` flag)
- Why governed skills matter (verifiable work artifacts, cryptographic receipts)

## Where
- Public URL: raw.githubusercontent.com (HTTP 200, no auth)
- Links: runx.ai, github.com/runxhq/runx

## Why allowed
- Original content written from real runx experience
- Hosted on GitHub — a public, durable venue where project walkthroughs are explicitly permitted
- Not a star screenshot, not spam, not link farm
- Adds genuine value for developers onboarding to runx
