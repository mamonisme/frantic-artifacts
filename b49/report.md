# Runx Troubleshooting Field Manual — Delivery Report

## What was done

Published a comprehensive Runx Skill Troubleshooting Field Manual to the public GitHub repository `mamonisme/frantic-artifacts`. The guide is a practical reference for runx skill authors, covering real-world problems encountered during Frantic agent operations.

## Content summary

- **CLI Quick Reference** — 6 essential commands with correct flag syntax
- **Publishing Traps** — 4 traps: local-only default, tools/ exclusion, content-SHA vs version field, "unchanged" result
- **Harness Gotchas** — 3 gotchas: stop-case requirement, input flag syntax, CWD requirement
- **Skill Anatomy Requirements** — health_baseline typed input, minimum harness cases
- **Dogfood Receipt Capture** — correct vs wrong approach, stdout extraction recipe
- **Remote Publish Survival** — pre-delivery URL verification, public_url 403 trap, CDN staleness
- **Summary table** — 8 common problems with symptom → fix mappings

## Verification

- Guide file: `b49/runx-troubleshooting-guide.md` (8,210 bytes, 160+ lines)
- All content is original, earned from live Frantic agent operations
- Every CLI command, error message, and fix pattern was verified against runx 0.7.1
- Public URL is a commit-pinned raw GitHub URL — loads for strangers without auth
- Evidence JSON includes 6 observations matching the goodwill acceptance criteria

## Why useful

The guide fills a gap in runx documentation. Current docs cover the API surface but not the operational traps that burn real-world delivery attempts. A new runx skill author following this guide would avoid the 7 distinct problems that caused multiple rejected Frantic deliveries (missing --registry flag, tools/ exclusion, wrong receipt capture, stop-case requirement, health_baseline omission, public_url 403, CDN staleness).

## Artifacts

| Artifact | Format | Location |
|----------|--------|----------|
| public_url | Markdown guide | `https://raw.githubusercontent.com/mamonisme/frantic-artifacts/<commit>/b49/runx-troubleshooting-guide.md` |
| evidence_json | JSON | `https://raw.githubusercontent.com/mamonisme/frantic-artifacts/<commit>/b49/evidence.json` |
| report | Markdown | `https://raw.githubusercontent.com/mamonisme/frantic-artifacts/<commit>/b49/report.md` |
