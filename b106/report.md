# Bounty #106 — runx skill: agency health

## Deliverable
`agency-health` skill: assembles a **read-only** health bundle for one running agency over a period.

- Reads domain-keyed turn state via data-store `read_events` (C2 contract) keyed on the agency case, folded in version order.
- Reads cross-run aggregates (seal rate, refusal spikes) from the ledger read runner (C7) by receipt **id-stub only** — never treats the ledger as domain state.
- Grades signals against declared norms; seals `health_verdict` (healthy/watch/degraded) plus typed intervention findings naming target lanes (policy-author / improve-skill / ops-desk / human).
- Strictly read-only: appends nothing, sends nothing, executes nothing, consumes no effect. Refuses any mutate framing (`run({mutate:true})` -> `refused: read_only_contract`).

## Verification
- `runx harness skills/agency-health` → **passed 2/2** (agency-health-healthy, agency-health-degraded-stall)
- `runx registry publish` → success (owner mamonisme, v0.1.0)
- Receipts: `sha256:61f68364a57630a65e539b3555633447f7221ee3a8d6332467b238adb2ab4688`, `sha256:17ed39e4cf226176c404fb914e805c8df280037848ae582f403306f16456376d`

## Artifacts
- SKILL.md + X.yaml: `https://github.com/mamonisme/runx/tree/feat/agency-health/skills/agency-health`
- PR: https://github.com/runxhq/runx/pull/290
- Public: https://runx.ai/x/mamonisme/agency-health@0.1.0

## Note on CI
PR CI (`scafld verify`) fails only because GitHub refuses fork-PR checkout under `pull_request_target` (pwn-request protection). This is a repo policy, not a skill defect — harness passes locally and publish succeeded.
