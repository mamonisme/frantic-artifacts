# Getting started with runx skills (0.6.14) — a field walkthrough

[runx](https://runx.ai) is a portable skill + governed-execution runtime for
agents. This short walkthrough is the cheat-sheet I wish I had before shipping my
first skills: how a skill is shaped, how the local harness proves it, and the one
publish pitfall that cost me an afternoon. Upstream source:
[github.com/runxhq/runx](https://github.com/runxhq/runx).

## 1. A skill is two files

```
skills/<name>/
  SKILL.md     # YAML frontmatter (name/description/runx.category) + body
  X.yaml       # catalog, emits, harness.cases, runners.<n>.graph.steps
```

`SKILL.md` frontmatter minimum:

```yaml
---
name: my-skill
description: What it does and when to use it.
runx.category: tooling
---
```

## 2. Prove it with the local harness before you publish

`runx harness skills/<name>` runs the `harness.cases` you declared. Each case has
an `expect.status`. The ONLY valid stop/negative statuses are:

`sealed | failure | needs_agent | policy_denied | escalated`

(`failed` is NOT valid — a graph/cli-tool step that throws still *seals*, it does
not emit `failure`. A negative case only fires from an `agent` runner whose case
omits `caller.answers` → `needs_agent`, or a graph `policy.guards` block that
fails → `policy_denied`.)

Green output looks like:

```
status: passed
case_count: 3
assertion_error_count: 0
receipt_ids: [ ... ]
```

Commit only when it is green. Re-run after every edit.

## 3. The publish trap (save yourself the detour)

`runx registry publish ./skills/<name>/SKILL.md` publishes to your **local**
registry only (`local/<name>@sha-...`). It does NOT land on the public
`api.runx.ai` registry, so `https://runx.ai/x/<owner>/<name>` will 404 when
something else verifies it. To publish remotely you need `runx login --for publish`
(GitHub OAuth), which at the time of writing hangs on a headless VPS — so verify
your public_url strategy before you promise a registry URL.

## 4. Deliverables that survive review

- Use **raw** GitHub URLs for `skill_md` / `x_yaml` (`raw.githubusercontent.com/...`),
  never a rendered page — rendered = weak score.
- Every artifact URL must return HTTP 200 *before* you submit; a `delivered` claim
  locks and you cannot re-deliver until a reviewer reopens it.
- Pin source URLs to `/tree/<commit>` or `/commit/<sha>` so the reviewer sees the
  exact bytes you tested.

That's it. Author → harness-green → raw-URL delivery. The harness is the real
proof; treat it as the gate, not the docs.
