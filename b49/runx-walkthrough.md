# Getting started with runx skills — a field walkthrough

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
an `expect.status`. The ONLY valid negative/stop statuses are:

`sealed | failure | needs_agent | policy_denied | escalated`

(`failed` is NOT valid — a graph/cli-tool step that throws still *seals*, it does
not emit `failure`. A stop case only fires from an `agent` runner whose case
omits `caller.answers` → `needs_agent`, or a graph `policy.guards` block that
fails → `policy_denied`.)

Green output reports `status: passed` with `receipt_ids`. Capture those before
publishing.

## 3. `runx registry publish` is LOCAL by default

`runx registry publish ./skills/<s>/SKILL.md` does **not** reach `api.runx.ai`.
It publishes to your *local* registry (`local/<s>@sha-...`). Consequences:

- `runx registry read mamonisme/<s>` → `registry skill not found`
- `runx registry search` lists `local/<s>@sha-...`, never `mamonisme/<s>`
- any `public_url: https://runx.ai/x/mamonisme/<s>@<ver>` you submit will 404

To reach the public registry you must authenticate for publish
(`runx login --for publish`, or set the publish token). Until that works,
point `public_url` (and `skill_md`/`x_yaml`) at the **raw GitHub URL** of your
fork branch — it is durable and verifiable.

## 4. Why this matters

runx is new. Most of the sharp edges are undocumented publish/runtime traps, not
skill logic. A short, accurate field guide like this one saves a contributor an
hour each. That is the kind of authentic signal a young OSS project needs more
than a star.
