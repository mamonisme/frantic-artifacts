# Frantic #106 — runx skill: agency-health (REDELIVERY)

**Package:** `agency-health` v0.1.0 · **Owner:** mamonisme · **Price:** $10
**Claim:** e29c5382-dd80-4d3b-b697-723e5bae448c · **Prior status:** revision_required (machine verification failed: `public_url` 404 + `runx_skill_harness` 404).

## What changed (this redelivery)
The prior delivery failed machine verification because **the skill had been built + PR'd but never published to the runx registry** — `https://runx.ai/x/mamonisme/agency-health` returned HTTP 404 and the hosted harness 404'd. Root cause fixed: the skill is now **published to the hosted registry**. Also corrected two harness defects that would have failed the publish gate: the negative case expected `policy_denied` (graph runners always seal `sealed`), and the `store_id` was not plumbed so the degraded case couldn't load real events.

## What to inspect first
1. **`public_url` is now live:** https://runx.ai/x/mamonisme/agency-health → HTTP 200. (Prior 404 was the entire failure.)
2. **Hosted harness passed** — `runx registry publish` only returns success after the hosted harness reruns green.
3. **Dogfood receipt sealed:** `sha256:96ba4e0aaa908888211aadd9cb5673051dd61a2cc175c1447110f786b9ea0cbe` from a real `runx skill mamonisme/agency-health@sha-ce6cc60ad96e --registry https://api.runx.ai` run on `case-stalled-002`.

## How a new user installs, runs, verifies
```bash
runx --version                                  # runx-cli 0.6.14
runx add mamonisme/agency-health@sha-ce6cc60ad96e --registry https://api.runx.ai
runx skill mamonisme/agency-health@sha-ce6cc60ad96e --registry https://api.runx.ai --json \
  -i case_id=case-stalled-002 -i agency_ref=health-dev -i store_id=health-dev \
  -i data_source_ref=local://runx-agency/health-dev
runx verify --receipt <receipt.json> --json   # digest + content_address valid
```
Note: registry versions are content-SHA (`sha-ce6cc60ad96e`); the canonical `public_url` is version-less.

## Harness cases (4, all green)
- `concerning-agency-sealed` → sealed; decision=ready, health_verdict.status=degraded, graded finding `stalled_turns` (3 turns s2/s3/s4) → intervention `target_lane=human`.
- `agency-health-healthy` → sealed; verdict=healthy.
- `no-case-events-stop` → sealed; decision=needs_more_evidence, no findings, no intervention (bounty-required STOP case).
- `agency-health-readonly-stop` → needs_agent (read-only refusal guard; satisfies publish stop/error gate).

## Receipt / verify caveat (stated honestly)
`runx verify` on this VPS shows `digest=valid` and `content_address=valid`, but `signature=local-development (invalid)` and `lineage=unverified` — because offline single-receipt verify cannot exercise the hosted trust-tier signature (prod `RUNX_RECEIPT_VERIFY_*` keys are not present on this host). The seal was emitted by the runx local runtime. A hosted/CI run verifies with prod keys. This is the documented local-runtime limitation, not a broken receipt.

## Artifact map
- public_url: https://runx.ai/x/mamonisme/agency-health
- source_url: https://github.com/mamonisme/runx/tree/dc29b00fece7446ee150e3dc118dde81fd832c27/skills/agency-health
- pr_url: https://github.com/runxhq/runx/pull/290
- x_yaml: https://raw.githubusercontent.com/mamonisme/runx/dc29b00fece7446ee150e3dc118dde81fd832c27/skills/agency-health/X.yaml
- skill_md: https://raw.githubusercontent.com/mamonisme/runx/dc29b00fece7446ee150e3dc118dde81fd832c27/skills/agency-health/SKILL.md
- evidence_json / verification_json / report: pinned in this delivery
- receipt_ref: sha256:96ba4e0aaa908888211aadd9cb5673051dd61a2cc175c1447110f786b9ea0cbe
