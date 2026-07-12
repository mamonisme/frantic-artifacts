# Bounty #109 — runx skill: purchase approval

## Deliverable
`purchase-approval` skill: decides a purchase request before any spend is committed.

- Reads procurement policy + budget balance (read-only).
- Decides **approve_in_full / scope_down / deny** against policy caps, vendor lists, and remaining budget.
- On approval emits typed `approval_decision` + bounded `AttenuationRequest` ceiling (amount, currency, counterparty, scopes).
- Forward counterpart to settle-invoice; distinct from expense-policy-check (post-hoc).
- Strictly a decision gate: never spends, sends, or mutates.

## Verification
- `runx harness skills/purchase-approval` → **passed 3/3** (approve / scope_down / deny)
- `runx registry publish` → success (owner mamonisme, v0.1.0)
- Receipts: `sha256:36cda173...`, `sha256:77a19682...`, `sha256:b0c32915...`

## Artifacts
- SKILL.md + X.yaml: `https://github.com/mamonisme/runx/tree/feat/purchase-approval/skills/purchase-approval`
- PR: https://github.com/runxhq/runx/pull/301
- Public: https://runx.ai/x/mamonisme/purchase-approval@0.1.0

## Note on CI
PR CI (`scafld verify`) fails only due to GitHub fork-PR checkout policy under `pull_request_target` (pwn-request protection). Repo policy, not a skill defect — harness passes locally, publish succeeded.
