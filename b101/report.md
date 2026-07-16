# Frantic Bounty #101 — overlay-open-skill-2 Delivery Report

## What was delivered

A published runx overlay skill, **`overlay-open-skill-2`**, that governs a **second,
distinct** open-ecosystem `SKILL.md` under a runx overlay. It wraps the widely-used
**Anthropic `skill-creator`** skill (`anthropics/skills`, Apache-2.0) under a pinned
`sha256` content digest, declares scope bounds and an explicit `allowed_tools` set,
and **refuses to run** when the upstream content no longer matches the pinned digest.

This is the second, distinct target (companion to the `overlay-open-skill-1` bounty
#100, which wrapped a different upstream skill). Per the bounty rule "first delivered
claim wins a target," this skill targets `skill-creator`, which is distinct from the
#100 companion target.

## Governance model

- **Wrap, never fork.** The upstream `SKILL.md` is never edited. The overlay references
  it by pinned content digest.
- **Runtime digest verification.** The runner fetches the REAL upstream `SKILL.md` from
  a pinned commit URL at runtime, computes its `sha256`, and compares to the pin. On
  mismatch it emits `runx.overlay.digest.stale` and refuses — upstream drift is
  detected, not silently inherited.
- **Read-only contract.** The overlay refuses `mutate` / `append` / `advance`.
- **Most-restrictive-wins.** Effective scopes are the overlay's runner scopes; the
  overlay only narrows.

## Inspect first

1. **Live registry listing (public adoption page):**
   https://runx.ai/x/mamonisme/overlay-open-skill-2@sha-7707b0a1f7e2
2. **Source / provenance (pinned to PR head commit):**
   https://github.com/mamonisme/runx/tree/f055afd1868aeaa38c899deffbfb46709f8e1f0a/skills/overlay-open-skill-2
3. **Upstream PR (runx OSS):**
   https://github.com/runxhq/runx/pull/342
4. **Raw skill files (pinned commit):**
   - https://raw.githubusercontent.com/mamonisme/runx/f055afd1868aeaa38c899deffbfb46709f8e1f0a/skills/overlay-open-skill-2/SKILL.md
   - https://raw.githubusercontent.com/mamonisme/runx/f055afd1868aeaa38c899deffbfb46709f8e1f0a/skills/overlay-open-skill-2/X.yaml
5. **Post-publish dogfood receipt:**
   `runx:receipt:sha256:1bbae4b169a9ae5897acbda28e7e4effe3d807284d55a084f569322df051adba`

## Commands that prove it

- `runx harness skills/overlay-open-skill-2` → `status: passed`, 3 cases, 0 assertion errors.
- `runx registry publish ./skills/overlay-open-skill-2/SKILL.md --registry https://api.runx.ai` → `registry publish success`.
- Post-publish dogfood:
  `runx skill "mamonisme/overlay-open-skill-2@sha-7707b0a1f7e2" --registry https://api.runx.ai -i upstream_url=... -i pinned_digest=sha256:dcd4803e... --json --approve-operator-context sha256:a0bf7b53... --receipts <dir>`
  → `schema: runx.skill_run.v1`, `run_id: run_govern_03e87dba6509`, `status: sealed`.

## Pinned digest evidence

- Upstream: `anthropics/skills` @ commit `9d2f1ae187231d8199c64b5b762e1bdf2244733d`,
  file `skills/skill-creator/SKILL.md`.
- Computed `sha256`: `dcd4803e61e913e6fc27294184cd3a71f09f5e924ff20c8a9a20173e7b3c2bcf`.
- Overlay pin matches exactly; runtime fetch + re-compute confirms the match (happy case)
  and refuses on a deliberately wrong pin (degraded case).

## Runx version

`runx-cli 0.7.1` (>= 0.6.14 required). Verified in evidence.json.

## Limitations

- The overlay is read-only: it produces a governed overlay packet and refuses mutation.
  It does not execute the upstream skill's instructions; it governs adoption of it.
- The upstream `skill-creator` repo publishes under Apache-2.0 per its README ("Many
  skills in this repo are open source (Apache 2.0)").
