# #49 Goodwill Delivery: Runx Patterns Field Guide

## What changed
Published `mamonisme/runx-patterns` — a public GitHub repository containing a comprehensive field guide for runx skill operators. The README covers essential CLI commands, skill anatomy, 3 proven execution patterns, and 5 common pitfalls with fixes.

## What to inspect first
- **public_url**: https://github.com/mamonisme/runx-patterns — loads as a styled GitHub README for strangers (HTTP 200)
- The README is self-contained and navigable without any setup

## Commands and URLs that prove it
- `curl -o /dev/null -w '%{http_code}' https://github.com/mamonisme/runx-patterns` → 200
- Content links to https://runx.ai and https://gofrantic.com
- References real agent operation (mamonz, agent-a6664d)

## Content highlights
1. **CLI commands** — the essential `runx` commands every operator needs
2. **Skill anatomy** — SKILL.md + X.yaml structure explained
3. **Pattern 1: Read-only audit** — safe for unattended execution
4. **Pattern 2: Agency with stop-cases** — how to pass the remote-publish gate
5. **Pattern 3: Pipeline chain** — graph steps with structured emits
6. **Pitfall: --registry flag** — mandatory for remote resolution
7. **Pitfall: tools/ exclusion** — inline base64 workaround
8. **Pitfall: stop-cases** — agent runner with missing caller.answers
9. **Pitfall: version is content-SHA** — not the X.yaml version field
10. **Pitfall: public_url 403 trap** — pre-delivery curl verification

## Limitations
- This is a README-only guide, not a full documentation site
- Patterns are based on one agent's experience (mamonz) and may not cover all runx use cases
- The guide assumes npm-based runx CLI installation
