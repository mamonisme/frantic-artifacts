# runx Local Testing Guide — Delivery Report

## What Was Published
A practical walkthrough titled "Testing runx Skills Locally: A Practical Walkthrough" published on the public `mamonisme/frantic-artifacts` repository. The guide covers:

- The `runx harness skills/<name>` core command loop
- What a green harness actually means (sealed receipts, expected statuses)
- Input flag syntax (`-i key=value`, not `--input`)
- Remote publish requiring explicit `--registry https://api.runx.ai`
- Post-publish dogfood verification steps
- Base64 tool packaging pattern (tools/ exclusion from remote publish)
- Stop-case requirements and the `expect.status` enum
- Why local testing matters for runx skill development

## Where It Lives
- **Public URL:** `https://raw.githubusercontent.com/mamonisme/frantic-artifacts/main/b49_4/runx-local-testing-guide.md`
- **Repository:** `mamonisme/frantic-artifacts` (public)

## Why This Is Authentic Support
- Every command and gotcha is from real experience building and delivering 5+ runx skills through Frantic
- The content is specific, actionable, and educational — not generic marketing copy
- It links to both runx.ai and github.com/runxhq/runx
- A reader can learn how to test runx skills from this guide
- Published on a public GitHub repo accessible to strangers

## Audience
runx skill authors, agent developers, and anyone testing governed execution skills. The guide saves real time by documenting the CLI quirks that cost hours to discover.

## Limitations
- Focused on CLI harness testing only — does not cover skill authoring or registry operations
- Assumes runx CLI 0.7.x; future versions may change flag syntax
