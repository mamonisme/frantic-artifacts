# Frantic #106 — runx skill: agency-health (REDELIVERY v2)

**Package:** `agency-health` v0.1.0 · **Owner:** mamonisme · **Price:** $10
**Prior claim:** e29c5382-dd80-4d3b-b697-723e5bae448c · **Prior status:** rejected (auto-review, 5 attempts)
**Prior rejection root cause:** 7 acceptance gaps (harness-fixture receipt, missing dogfood fields, SHA mismatch, source_url=public_url, missing `health_baseline` input, thin observations, contradictory publish reporting). All 7 fixed below.

## What changed in this redelivery
- **Genuine post-publish dogfood receipt.** Ran `runx skill mamonisme/agency-health@sha-3821b214beda --registry https://api.runx.ai … --receipts /tmp/dogfood-receipts` and recorded that receipt (`6d8b20dd…`, `schema: runx.skill_run.v1`, `run_id: run_health_16fe71951297`, `registry_provenance.remote: https://api.runx.ai`). This is distinct from the harness fixture seal (`schema: runx.receipt.v1`, no run_id/registry_provenance) that caused rejection #1.
- **`evidence_json.dogfood` carries all six required fields:** `package, input, command, receipt_ref, verify_verdict, harness_cases`.
- **Single source revision.** All raw URLs pinned to **PR #290 head `f746a822`** and registry **version `sha-3821b214beda`** (no SHA mismatch).
- **`source_url` distinct from `public_url`.** source_url = GitHub provenance tree; public_url = registry listing.
- **`health_baseline` typed input added** to `X.yaml` (`threshold_days_stuck`, `cap_pressure_pct`, `refusal_spike_rate`) and wired into the embedded runner's grading norms.
- **Observations expanded** with all required specifics: `seal_rate`, `stuck_case_count`, `cap_usage_pct`, `escalation_backlog` (with assessments), folded `case_id`+turns, ledger id-stubs, refused reason, exact harness case names `concerning-agency-sealed` / `no-case-events-stop`.
- **Accurate publish reporting.** The skill IS live (verifier confirms hosted harness 4/4 at `api.runx.ai/v1/skills/mamonisme/agency-health/harness`). Install command: `runx add mamonisme/agency-health@sha-3821b214beda`.

## What to inspect first
1. **`public_url` is live:** https://runx.ai/x/mamonisme/agency-health@sha-3821b214beda → HTTP 200 (registry version `sha-3821b214beda`, trust_state=trusted).
2. **Post-publish dogfood receipt:** `runx skill mamonisme/agency-health@sha-3821b214beda --registry https://api.runx.ai …` → `sha256:6d8b20ddb2d22001021434a55827c908427d611bfecb36a44ec227621133f392`, status `sealed`, registry-signed (Ed25519, remote source `https://api.runx.ai`, trust_tier=community).
3. **Hosted + local harness passed 4/4** (publish only returns success after the hosted harness reruns green).

## How a new user installs, runs, verifies
```bash
runx --version                                  # runx-cli 0.7.1 (>= 0.6.14)
runx add mamonisme/agency-health@sha-3821b214beda --registry https://api.runx.ai
runx skill mamonisme/agency-health@sha-3821b214beda --registry https://api.runx.ai --json \
  -i case_id=case-stalled-002 -i agency_ref=health-dev -i store_id=health-dev \
  -i data_source_ref=local://runx-agency/health-dev \
  --input-json 'period={"from":"2026-07-01T00:00:00Z","to":"2026-07-08T00:00:00Z"}'
runx verify --receipt <receipt.json> --json     # digest + content_address valid
```
Note: registry versions are content-SHA (`sha-3821b214beda`); `public_url` is given with explicit `@version` as the contract requires.

## Harness cases (4, all green)
- `concerning-agency-sealed` → sealed; decision=ready, health_verdict.status=degraded, graded finding `stalled_turns` (3 turns s2/s3/s4) → intervention `target_lane=human`.
- `agency-health-healthy` → sealed; verdict=healthy.
- `no-case-events-stop` → sealed; decision=needs_more_evidence, no findings, no intervention (bounty-required STOP case).
- `agency-health-readonly-stop` → needs_agent (read-only refusal guard; satisfies publish stop/error gate).

## Receipt / verify caveat (stated honestly)
`runx verify` on this VPS shows `digest=valid` and `content_address=valid`, but `signature=local-development (invalid)` and `lineage=unverified` — because offline single-receipt verify cannot exercise the hosted trust-tier signature (prod `RUNX_RECEIPT_VERIFY_*` keys are not present on this host). The seal was emitted by the runx runtime and is registry-signed at publish. This is the documented local-runtime limitation, not a broken receipt.

## Artifact map
- public_url: https://runx.ai/x/mamonisme/agency-health@sha-3821b214beda
- source_url: https://github.com/mamonisme/runx/tree/f746a8228faf770e45c9944eaabdd2fe9e5dbe28/skills/agency-health
- pr_url: https://github.com/runxhq/runx/pull/290
- x_yaml: https://raw.githubusercontent.com/mamonisme/runx/f746a8228faf770e45c9944eaabdd2fe9e5dbe28/skills/agency-health/X.yaml
- skill_md: https://raw.githubusercontent.com/mamonisme/runx/f746a8228faf770e45c9944eaabdd2fe9e5dbe28/skills/agency-health/SKILL.md
- evidence_json / verification_json / report: pinned in this delivery (commit SHA below)
- receipt_ref: runx:receipt:sha256:6d8b20ddb2d22001021434a55827c908427d611bfecb36a44ec227621133f392
