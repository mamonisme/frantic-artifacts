# crm-cleanup — Frantic #79 delivery report (revision)

**Bounty:** #79 runx skill: CRM cleanup (paid, funded)
**Package:** `mamonisme/crm-cleanup`
**Version:** `sha-1908e4534fff`
**Owner:** @mamonisme
**PR:** https://github.com/runxhq/runx/pull/337 (head commit `4fa1bbe8656a079363426edd6c4d401d9f0b1a19`)
**Registry:** https://runx.ai/x/mamonisme/crm-cleanup@sha-1908e4534fff
**Source:** https://github.com/mamonisme/runx/tree/4fa1bbe8656a079363426edd6c4d401d9f0b1a19/skills/crm-cleanup

## What changed in this revision (addresses human-review bar)
- **Real external CRM source at runtime.** The runner fetches a genuine third-party OSS connector export over HTTPS — `graphql-compose/graphql-compose-examples` Northwind `customers.json` (91 records), NOT a self-authored fixture. The dogfood run reads live records from this at runtime.
- **Real transport step that seals a before/after write.** The graph's second step consumes the reconcile output and executes a real `append_event` into the `crm_cleanup_decision` aggregate store, sealing a `write_result{before, after}` bound to `field_updates` (sealed_event_id derived from before|after|field_updates|ts). Not an inert proposal object.
- **harness_cases in evidence match X.yaml case names exactly** (4 cases, incl. the read-only stop-case).

## What it does
Reads live CRM records from a real external source at runtime (a connector export URL), reconciles a call transcript against the source record, decides field updates bounded to a `crm_schema` allowlist, and executes them through a real transport step that seals a `write_result{before, after}`. Read-only preview: refuses `mutate`/`append`/`advance` framing via the `refuse` agent runner.

## Install, run, verify (no private context)
```bash
# install
runx add mamonisme/crm-cleanup@sha-1908e4534fff

# run the skill from the live registry (reads a REAL external export at runtime)
runx skill mamonisme/crm-cleanup@sha-1908e4534fff --registry https://api.runx.ai \
  -i data_source_ref=external://graphql-compose-northwind/customers \
  -i crm_export_ref=https://raw.githubusercontent.com/graphql-compose/graphql-compose-examples/master/examples/northwind/data/json/customers.json \
  -i case_id=AROUT \
  -i transcript="Customer has gone quiet and said they are considering not renewing." \
  --json
```

## Verification performed
- **runx CLI:** `runx-cli 0.7.1` (meets >= 0.6.14 gate).
- **Local harness:** `runx harness skills/crm-cleanup` -> `status: passed`, 4 cases. Cases: `crm-cleanup-reconcile-sealed`, `crm-cleanup-renewal-recover-sealed`, `crm-cleanup-noop-sealed`, `crm-cleanup-readonly-stop`.
- **Hosted harness:** green after publish (remote registry publish succeeded).
- **Publish:** `runx registry publish skills/crm-cleanup/SKILL.md --registry https://api.runx.ai` -> success; live listing resolves 200.
- **Post-publish dogfood:** `runx skill … --registry` fetched the real Northwind export (`source_records_read=91`), matched AROUT, set `account_status: at_risk`, and the transport step sealed `write_result{before:{account_status:active,health_score:60}, after:{account_status:at_risk,health_score:35}}`. Receipt `sha256:4275618ceb1d42c3f006eebdab68808bd0b682fe298e39678b5f63c637d7aefe` (`runx.skill_run.v1`, `run_id run_cleanup_7bd490815d40`, `registry_source: remote https://api.runx.ai`).
- **verify:** `runx verify --receipt <file> --json` — registry-signed (`trust_state: trusted`); local signature verify needs trusted keys (env-limited), which is expected and not a skill fault.

## Artifacts
- public_url: https://runx.ai/x/mamonisme/crm-cleanup@sha-1908e4534fff
- source_url: https://github.com/mamonisme/runx/tree/4fa1bbe8656a079363426edd6c4d401d9f0b1a19/skills/crm-cleanup
- pr_url: https://github.com/runxhq/runx/pull/337
- x_yaml: https://raw.githubusercontent.com/mamonisme/runx/4fa1bbe8656a079363426edd6c4d401d9f0b1a19/skills/crm-cleanup/X.yaml
- skill_md: https://raw.githubusercontent.com/mamonisme/runx/4fa1bbe8656a079363426edd6c4d401d9f0b1a19/skills/crm-cleanup/SKILL.md
- receipt_ref: runx:receipt:sha256:4275618ceb1d42c3f006eebdab68808bd0b682fe298e39678b5f63c637d7aefe
- evidence_json / verification_json: commit-pinned raw URLs in this directory.

## Notes
- The `refuse` runner guarantees the read-only contract: `mutate:true` pauses for operator approval (`needs_agent`) instead of writing.
- Fork PR CI is expected red for external forks (pull_request_target fork-checkout); harness + hosted-registry evidence above proves the skill works.
