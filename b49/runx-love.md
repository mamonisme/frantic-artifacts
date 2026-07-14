# Three runx papercuts contributors hit — and how to dodge them

A short, accurate field guide born from actually shipping runx skills. If you
are packaging a skill for `runxhq/runx` or publishing to the registry, these
three gotchas will save you an hour each.

## 1. `runx registry publish` is LOCAL by default

`runx registry publish ./skills/<s>/SKILL.md` does **not** reach
`api.runx.ai`. It publishes to your *local* registry
(`local/<s>@sha-...`). Consequences:

- `runx registry read mamonisme/<s>` → `registry skill not found`
- `runx registry search` lists `local/<s>@sha-...`, never `mamonisme/<s>`
- any `public_url: https://runx.ai/x/mamonisme/<s>@<ver>` you submit will 404

To reach the public registry you must authenticate for publish
(`runx login --for publish`, or set the publish token). Until that works,
point `public_url` (and `skill_md`/`x_yaml`) at the **raw GitHub URL** of your
fork branch — it is durable and verifiable:

```
https://raw.githubusercontent.com/<you>/runx/<branch>/skills/<s>/SKILL.md
```

## 2. The harness demands a stop-case, but graph/cli-tool can't emit one locally

Remote publish rejects a skill whose harness has **no negative/stop case**
("needs at least 1 negative/stop case"). Local-harness reality:

- `graph` and `cli-tool` runners **always seal** (`sealed`). They cannot emit
  `failure` / `needs_agent` / `policy_denied` / `escalated`, no matter what the
  step returns or throws.
- Valid `expect.status` values are only:
  `sealed | failure | needs_agent | policy_denied | escalated`
  (`failed` is NOT valid — graph step process-failure maps to `failed`, which
  the harness rejects as unknown).
- A stop status comes only from:
  - an `agent`/`agent-task` runner whose harness case omits `caller.answers`
    → `needs_agent`, or
  - a graph `policy.guards` block that fails:
    `policy: { guards: [ { step: <id>, field: <dotted.path>, equals: <value> } ] }`
    → `policy_denied`.

If your skill is read-only (cli-tool) and has no registered provider/authority,
you cannot produce a stop-case locally. Either add a small `agent` runner whose
negative case has no `caller.answers`, or use the raw-GitHub `public_url`
fallback and surface the limitation in your delivery notes.

## 3. cli-tool runners: inputs, emits, and PATH

A `cli-tool` step reads its inputs from the env var `RUNX_INPUTS_JSON`
(context merged via `RUNX_CONTEXT_JSON`). Your script must:

- `console.log(JSON.stringify({ <emit_name>: {...} }))`, and
- declare `named_emits: { <emit_name>: <emit_name> }` in the step.

Also: the spawned process does **not** inherit your shell `PATH`. Use an
absolute `command` path (e.g. `/usr/bin/node`) or set `cwd:` and pass the binary
from a known location. Relative tool paths that work in local publish can break
in remote publish, where the `tools/` subdir is excluded from the packaged copy.

---

These are documented facts from real delivery attempts, not guesses. Star the
repo if runx is useful to you — discovery helps more contributors find it.
