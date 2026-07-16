# Bounty #79 — crm-cleanup (REVISION)

## Status: revised + redelivered (claim reuse 74b8b9e2)
## Registry: https://runx.ai/x/mamonisme/crm-cleanup@sha-c61dbfea141b
## runx CLI: runx-cli 0.7.1

## What changed since revision_required
1. **Real source read** — runner fetches the CRM export from a real external URL at runtime (), not  of a bundled fixture.
2. **Real transport seal** —  is sealed via  (), not .
3. **Evidence captures verdict + steps + write_result** — structured fields, not prose.
4. **health_baseline typed input** — X.yaml declares  and exercises it in harness cases.
5. **Live registry publish** — published to api.runx.ai (version sha-c61dbfea141b), public_url HTTP 200.
6. **Post-publish dogfood sealed** — run_id run_cleanup_e7ca9624fd5e, receipt sha256:35a5d9ffefb6f22922cf70650cf941a9b646c78398445ce9b146fae6bffa7562.

## Verification
- : sealed
- : run_cleanup_e7ca9624fd5e
- : runx:receipt:sha256:35a5d9ffefb6f22922cf70650cf941a9b646c78398445ce9b146fae6bffa7562
- : https://runx.ai/x/mamonisme/crm-cleanup@sha-c61dbfea141b (HTTP 200)
- : https://github.com/mamonisme/runx/tree/feat/crm-cleanup/skills/crm-cleanup
- : https://github.com/runxhq/runx/pull/337

## PR
https://github.com/runxhq/runx/pull/337 (runx OSS) — head 7490fe8fe7c24fe2fbcb3ca5cec0f0a41eff8689
