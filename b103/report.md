# Bounty #103 — Prove a substantial scafld bug with a failing test

## The bug
`ContractDigest` is documented as a **stable digest of the task contract** that
excludes volatile projection fields. It previously included `PlanningLog`, whose
entries carry per-event timestamps. As a result, two byte-identical contracts
differing **only** in a planning-log timestamp produced **different digests**.

In `reviewgate.staleReviewAuthority` this causes a valid, unchanged review to be
falsely flagged `review_stale_after_spec`, forcing spurious re-reviews and
blocking `scafld complete`.

## The fix
Removed `PlanningLog` from the digest struct.
- Fix commit: `1941ca5` on `mamonisme/scafld`
- PR: https://github.com/nilstate/scafld/pull/10

## Proof (failing test → fix → passing)
Regression tests added (both passing after the fix):
- `TestContractDigestStableAcrossPlanningLogTimestamp` — digest stays stable
  across a planning-log timestamp change.
- `TestContractDigestChangesWhenContractChanges` — digest still changes for a
  real contract edit (objective text), so the staleness signal stays live.

Runx harness over the fix branch seals a receipt proving the reproduction + fix:
`runx:receipt:sha256:51c745d5d50b7057ed8d2cb3c3519f8165a848260d7779a57dd88d3554b109e8`

## How to verify
```bash
git clone https://github.com/mamonisme/scafld
cd scafld
git checkout fix/contract-digest-planninglog-volatility
go test ./internal/core/spec/ -run TestContractDigest -v
```
