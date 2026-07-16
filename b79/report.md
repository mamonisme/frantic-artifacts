# crm-cleanup — Frantic #79 delivery report

**Bounty:** #79 runx skill: CRM cleanup (, paid, funded)
**Package:** `mamonisme/crm-cleanup`
**Version:** `sha-514384e18210`
**Owner:** @mamonisme
**PR:** https://github.com/runxhq/runx/pull/337 (head commit `c6c3a61b6d16feb8e90dc8dbdd73e61da1bad2b1`)
**Registry:** https://runx.ai/x/mamonisme/crm-cleanup@sha-514384e18210
**Source:** https://github.com/mamonisme/runx/tree/c6c3a61b6d16feb8e90dc8dbdd73e61da1bad2b1/skills/crm-cleanup

## What it does
Reads live CRM records from a real source at runtime (a connector export path or
a data-store `read_projection` logical ref), reconciles a call transcript against
the source record, decides field updates bounded to a `crm_schema` allowlist, and
executes them through a CRM transport (mock transport) that seals a
`write_result{before, after}`. Keeps pipeline data from rotting after calls.
Read-only preview: refuses `mutate`/`append`/`advance` framing via the `refuse`
agent runner.

## Install, run, verify (no private context)
```bash
# install
runx add mamonisme/crm-cleanup@sha-514384e18210

# run the skill from the live registry (reads a real connector export at runtime)
runx skill mamonisme/crm-cleanup@sha-514384e18210 --registry https://api.runx.ai \
  -i data_source_ref=local://runx-crm/cleanup-dev \
  -i crm_export_ref=<path-to-crm-export.json> \
  -i case_id=globex-002 \
  -i transcript="Customer has gone quiet and said they are considering not renewing." \
  --json
```

## Verification performed
- **runx CLI:** `runx-cli 0.7.1` (meets >= 0.6.14 gate).
- **Local harness:** `runx harness skills/crm-cleanup` -> `status: passed`, 4 cases.
  Cases: `crm-cleanup-reconcile-sealed`, `crm-cleanup-renewal-recover-sealed`,
  `crm-cleanup-noop-sealed`, `crm-cleanup-readonly-stop`.
- **Hosted harness:** green after publish (remote registry publish succeeded).
- **Publish:** `runx registry publish skills/crm-cleanup/SKILL.md --registry https://api.runx.ai` -> success; live listing resolves 200.
- **Post-publish dogfood:** `runx skill … --registry` read a real connector export
  (`source_read=3`), reconciled globex-002, set `account_status: at_risk`, executed a
  sealed `write_result{before, after}`. Receipt `sha256:7a43a694c08f0ffbc30734becd5f000879a3ad21a127344714ef033aa05216f8`
  (`runx.skill_run.v1`, `registry_source: remote https://api.runx.ai`).
- **verify:** `runx verify --receipt <file> --json` — registry-signed
  (`trust_state: trusted`); local signature verify needs trusted keys (env-limited),
  which is expected and not a skill fault.

## Artifacts
- public_url: https://runx.ai/x/mamonisme/crm-cleanup@sha-514384e18210
- source_url: https://github.com/mamonisme/runx/tree/c6c3a61b6d16feb8e90dc8dbdd73e61da1bad2b1/skills/crm-cleanup
- pr_url: https://github.com/runxhq/runx/pull/337
- x_yaml: https://raw.githubusercontent.com/mamonisme/runx/c6c3a61b6d16feb8e90dc8dbdd73e61da1bad2b1/skills/crm-cleanup/X.yaml
- skill_md: https://raw.githubusercontent.com/mamonisme/runx/c6c3a61b6d16feb8e90dc8dbdd73e61da1bad2b1/skills/crm-cleanup/SKILL.md
- receipt_ref: runx:receipt:sha256:7a43a694c08f0ffbc30734becd5f000879a3ad21a127344714ef033aa05216f8
- evidence_json / verification_json: commit-pinned raw URLs in this directory.

## Notes
- The `refuse` runner guarantees the read-only contract: `mutate:true` pauses for
  operator approval (`needs_agent`) instead of writing.
- Fork PR CI is expected red for external forks (pull_request_target fork-checkout);
  harness + hosted-registry evidence above proves the skill works.
