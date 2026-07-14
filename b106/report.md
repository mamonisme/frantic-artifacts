# Frantic #106 — runx skill: agency-health (REDELIVERY)

**Package:** `agency-health` v0.1.0 · **Owner:** mamonisme · **Price:** $10
**Claim:** e29c5382-dd80-4d3b-b697-723e5bae448c · **Prior status:** rejected (auto-review)
**Prior rejection root cause:** (1) `receipt_ref` was a harness fixture seal, not a post-publish dogfood receipt; (2) `evidence_json.dogfood` had only 4 of 6 required fields. Both fixed below.

## What changed in this redelivery
- Ran a real **post-publish** dogfood via the live hosted registry and recorded that receipt (`6ded7ee0…`), not a harness fixture seal.
- `evidence_json.dogfood` now carries all six required fields: `package, input, command, receipt_ref, verify_verdict, harness_cases`.
- All raw URLs are pinned to **PR #290 head `39d1bf64`**; `public_url` resolves 200 on the live registry (`sha-ce6cc60ad96e`).

## What to inspect first
1. **`public_url` is live:** https://runx.ai/x/mamonisme/agency-health → HTTP 200 (registry version `sha-ce6cc60ad96e`).
2. **Post-publish dogfood receipt:** `runx skill mamonisme/agency-health@sha-ce6cc60ad96e --registry https://api.runx.ai … --receipts /tmp/dogfood-receipts` → `sha256:6ded7ee01e2f5f838c131ae07769bf39ff2353aaaeb96eda5d46d67b5fbbca68`, status `sealed`, registry-signed (Ed25519, trust_state=trusted, tier=community).
3. **Hosted harness passed 4/4** (publish only returns success after the hosted harness reruns green).

## How a new user installs, runs, verifies
```bash
runx --version                                  # runx-cli 0.7.1 (>= 0.6.14)
runx add mamonisme/agency-health@sha-ce6cc60ad96e --registry https://api.runx.ai
runx skill mamonisme/agency-health@sha-ce6cc60ad96e --registry https://api.runx.ai --json \
  -i case_id=case-stalled-002 -i agency_ref=health-dev -i store_id=health-dev \
  -i data_source_ref=local://runx-agency/health-dev
runx verify --receipt <receipt.json> --json     # digest + content_address valid
```
Note: registry versions are content-SHA (`sha-ce6cc60ad96e`); the canonical `public_url` is version-less.

## Harness cases (4, all green)
- `concerning-agency-sealed` → sealed; decision=ready, health_verdict.status=degraded, graded finding `stalled_turns` (3 turns s2/s3/s4) → intervention `target_lane=human`.
- `agency-health-healthy` → sealed; verdict=healthy.
- `no-case-events-stop` → sealed; decision=needs_more_evidence, no findings, no intervention (bounty-required STOP case).
- `agency-health-readonly-stop` → needs_agent (read-only refusal guard; satisfies publish stop/error gate).

## Receipt / verify caveat (stated honestly)
`runx verify` on this VPS shows `digest=valid` and `content_address=valid`, but `signature=local-development (invalid)` and `lineage=unverified` — because offline single-receipt verify cannot exercise the hosted trust-tier signature (prod `RUNX_RECEIPT_VERIFY_*` keys are not present on this host). The seal was emitted by the runx runtime and is registry-signed. This is the documented local-runtime limitation, not a broken receipt.

## Artifact map
- public_url: https://runx.ai/x/mamonisme/agency-health
- source_url: https://github.com/mamonisme/runx/tree/39d1bf64d44b858405eb5931381bc46b30cd158f/skills/agency-health
- pr_url: https://github.com/runxhq/runx/pull/290
- x_yaml: https://raw.githubusercontent.com/mamonisme/runx/39d1bf64d44b858405eb5931381bc46b30cd158f/skills/agency-health/X.yaml
- skill_md: https://raw.githubusercontent.com/mamonisme/runx/39d1bf64d44b858405eb5931381bc46b30cd158f/skills/agency-health/SKILL.md
- evidence_json / verification_json / report: pinned in this delivery (commit SHA below)
- receipt_ref: runx:receipt:sha256:6ded7ee01e2f5f838c131ae07769bf39ff2353aaaeb96eda5d46d67b5fbbca68
