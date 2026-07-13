# Bounty #106 — runx skill: agency health

## Deliverable
`agency-health` skill: assembles a **read-only** health bundle for one running agency over a period.

- Reads domain-keyed turn state via data-store `read_events` (C2 contract) keyed on the agency case, folded in version order.
- Reads cross-run aggregates (seal rate, refusal spikes) from the ledger read runner (C7) by receipt **id-stub only** — never treats the ledger as domain state.
- Grades signals against declared norms; seals `health_verdict` (healthy/watch/degraded) plus typed intervention findings naming target lanes (policy-author / improve-skill / ops-desk / human).
- Strictly read-only: appends nothing, sends nothing, executes nothing, consumes no effect. Refuses any mutate framing (`run({mutate:true})` -> `refused: read_only_contract`).

## Verification
- `runx harness skills/agency-health` → **happy-path 2/2 PASS** (agency-health-healthy, agency-health-degraded-stall). Receipts: `sha256:65adbd70...`, `sha256:be1bc110...`.
- Negative/stop case: graph runner cannot emit `policy_denied`/`failure`/`needs_agent` in local harness without a registered provider/authority (unlike `pr-review-note` which ships a `github-mcp` provider). Remote publish therefore rejects "needs 1 stop case". **Fallback:** `public_url` = raw GitHub tree (Mitigation A).
- `runx registry publish` (local, default) → success (owner mamonisme, v0.1.0).
- PR #290 to runxhq/runx.

## Artifacts
- SKILL.md + X.yaml: `https://github.com/mamonisme/runx/tree/feat/agency-health/skills/agency-health`
- Raw SKILL.md: `https://raw.githubusercontent.com/mamonisme/runx/6eff047496efffe54e65d0c76022a55a3370ef5e/skills/agency-health/SKILL.md`
- Raw X.yaml: `https://raw.githubusercontent.com/mamonisme/runx/6eff047496efffe54e65d0c76022a55a3370ef5e/skills/agency-health/X.yaml`
- PR: https://github.com/runxhq/runx/pull/290
- Public (raw GitHub fallback): `https://github.com/mamonisme/runx/tree/feat/agency-health/skills/agency-health`

## Note on CI
PR CI (`scafld verify`) fails only because GitHub refuses fork-PR checkout under `pull_request_target` (pwn-request protection). This is a repo policy, not a skill defect — harness passes locally and publish succeeded.
