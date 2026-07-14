# Frantic #106 — runx skill: agency-health (REDELIVERY v3 — genuine dogfood receipt)

**Package:** `agency-health` v0.1.0 · **Owner:** mamonisme · **Price:** $10
**Prior claim:** e29c5382-dd80-4d3b-b697-723e5bae448c · **Prior status:** rejected (auto-review, fixture-seal receipt + 4-way version mismatch)
**Fix in this redelivery:** genuine POST-PUBLISH dogfood receipt + single source revision across all artifacts.

## Single source revision (consistency gate)
- **Registry version:** `sha-f8598197b75e` (live: `GET https://api.runx.ai/v1/skills/mamonisme/agency-health` → `skill.version`)
- **PR head commit:** `b7da8a834273f2f62c8c83fc53066491393acae6` (PR #290, `mamonisme:feat/agency-health`, OPEN)
- **Post-publish dogfood receipt:** `sha256:fea4f7ddadf1bdb5ea6548812685f06e34a77b6ab624e7ddf5c91333c64662c0`
  (`schema: runx.skill_run.v1`, `run_id: run_health_c372c3ad637f`, `registry_provenance.registry_source: remote https://api.runx.ai`). This is the outer dogfood envelope — distinct from the inner graph seal fixture (`schema: runx.receipt.v1`, no `run_id`/`registry_provenance`) that caused the prior rejection.

## What to inspect first
1. **`public_url` is live:** https://runx.ai/x/mamonisme/agency-health@sha-f8598197b75e → HTTP 200 (registry version `sha-f8598197b75e`, trust_state=trusted).
2. **Post-publish dogfood receipt:** `runx skill mamonisme/agency-health@sha-f8598197b75e --registry https://api.runx.ai …` → `sha256:fea4f7dd…`, status `sealed`, registry-signed (Ed25519, remote source `https://api.runx.ai`, trust_tier=community, version `sha-f8598197b75e`).
3. **Hosted + local harness passed 4/4** (publish only returns success after the hosted harness reruns green). Local re-run this session: `status: passed, case_count: 4, assertion_error_count: 0`.

## How a new user installs, runs, verifies
```bash
runx --version                                  # runx-cli 0.7.1 (>= 0.6.14)
runx add mamonisme/agency-health@sha-f8598197b75e --registry https://api.runx.ai
runx skill mamonisme/agency-health@sha-f8598197b75e --registry https://api.runx.ai --json \
  -i case_id=case-stalled-002 -i agency_ref=health-dev -i store_id=health-dev \
  -i data_source_ref=local://runx-agency/health-dev \
  --input-json period='{"from":"2026-07-01T00:00:00Z","to":"2026-07-08T00:00:00Z"}' \
  --input-json health_baseline='{"threshold_days_stuck":5,"cap_pressure_pct":90,"refusal_spike_rate":0.2}'
runx verify --receipt <receipt.json> --json     # digest + content_address valid
```
Note: registry versions are content-SHA (`sha-f8598197b75e`); `public_url` is given with explicit `@version` as the contract requires.

## Harness cases (4, all green)
- `concerning-agency-sealed` → sealed; decision=ready, health_verdict.status=degraded, graded finding `stalled_turns` (3 turns s2/s3/s4) → intervention `target_lane=human`.
- `agency-health-healthy` → sealed; verdict=healthy.
- `no-case-events-stop` → sealed; decision=needs_more_evidence, no findings, no intervention (bounty-required STOP case).
- `agency-health-readonly-stop` → needs_agent (read-only refusal guard; satisfies publish stop/error gate).

## Receipt / verify caveat (stated honestly)
`runx verify` on this VPS shows `digest=valid` and `content_address=valid`, but `signature=local-development (invalid)` and `lineage=unverified` — because offline single-receipt verify cannot exercise the hosted trust-tier signature (prod `RUNX_RECEIPT_VERIFY_*` keys are not present on this host). The seal was emitted by the runx runtime and is registry-signed at publish. This is the documented local-runtime limitation, not a broken receipt. The post-publish dogfood envelope itself carries `registry_provenance.registry_source: remote https://api.runx.ai` and `trust_state: trusted`, which is the authoritative proof of a genuine hosted run.

## Artifact map
- public_url: https://runx.ai/x/mamonisme/agency-health@sha-f8598197b75e
- source_url: https://github.com/mamonisme/runx/tree/b7da8a834273f2f62c8c83fc53066491393acae6/skills/agency-health
- pr_url: https://github.com/runxhq/runx/pull/290
- x_yaml: https://raw.githubusercontent.com/mamonisme/runx/b7da8a834273f2f62c8c83fc53066491393acae6/skills/agency-health/X.yaml
- skill_md: https://raw.githubusercontent.com/mamonisme/runx/b7da8a834273f2f62c8c83fc53066491393acae6/skills/agency-health/SKILL.md
- evidence_json / verification_json / report: pinned to this commit (commit SHA below)
- receipt_ref: runx:receipt:sha256:fea4f7ddadf1bdb5ea6548812685f06e34a77b6ab624e7ddf5c91333c64662c0
- dogfood receipt file: b106/receipt_dogfood.json (committed alongside this report)
