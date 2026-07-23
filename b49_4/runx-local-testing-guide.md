# Testing runx Skills Locally: A Practical Walkthrough

If you're building a [runx](https://runx.ai) skill, the fastest feedback loop is local harness testing. Here's what I learned from building and delivering several skills — the commands that work, the gotchas that waste hours, and the flow that gets you from zero to a green harness in one session.

## The Core Command

```bash
runx harness skills/<skill-name>
```

This runs every case defined in your `X.yaml` harness against the skill's runners. A green run means every step in every case sealed — the skill works end-to-end. Red means a step failed and you get a trace.

## What "Green Harness" Actually Means

Each case produces a sealed receipt (`runx.receipt.v1`). The harness passes when every case produces its expected `status` — for read-only skills that's usually `sealed` for happy-path and `needs_agent` or `policy_denied` for stop-cases. If any case status mismatches, the harness fails with a readable diff.

## The Input Trap

Skill inputs use `-i key=value` flags:

```bash
runx skill "owner/skill@version" \
  --registry https://api.runx.ai \
  -i threshold_days_stuck=5 \
  -i cap_pressure_pct=90 \
  --json
```

Not `--input`, not `--param`. This one got me on my first delivery — the CLI is strict about the `-i` flag syntax.

## Remote Publish Needs `--registry`

When you publish a skill, the default target is local:

```bash
# Publishes to local registry only:
runx registry publish ./skills/my-skill/SKILL.md

# Publishes to the live runx registry:
runx registry publish ./skills/my-skill/SKILL.md --registry https://api.runx.ai
```

Without `--registry`, the skill stays on your machine. The version becomes a content-SHA (`sha-...`), not whatever you put in `version:` in X.yaml — that field is metadata, not the live ref.

## The Dogfood Step

After publishing, always verify end-to-end:

```bash
runx skill "mamonisme/my-skill@<version>" \
  --registry https://api.runx.ai \
  -i key=value \
  --json --approve-operator-context <digest> \
  --receipts ./receipts
```

This produces a `runx.skill_run.v1` receipt with `run_id` and `registry_provenance` — that's the receipt reviewers check, not the harness fixture seal.

## Tools and Base64 Packaging

If your skill uses custom Node.js tools, inline them as base64 in `X.yaml`:

```yaml
runners:
  my-runner:
    type: cli-tool
    graph:
      steps:
        - run:
            type: cli-tool
            command: node
            args: ["-e", "eval(Buffer.from('<base64-blob>', 'base64').toString())"]
```

This is necessary because `tools/` subdirectories aren't included in remote publishes — the packager excludes them. Base64 inlining is the only reliable cross-environment path.

## Stop-Case Requirements

Remote publish rejects skills without at least one negative/stop case. For read-only skills, add an `agent` runner whose negative case omits `caller.answers`:

```yaml
harness:
  cases:
    - name: happy-path
      inputs: { ... }
      expect: { status: sealed }
    - name: needs-agent-stop
      inputs: { ... }
      caller: {}  # no answers → needs_agent
      expect: { status: needs_agent }
```

The `expect.status` enum is: `sealed | failure | needs_agent | policy_denied | escalated`. `failed` is not valid — the harness rejects it.

## Why This Matters

runx is pioneering portable, governed skills that any agent can run. Testing locally means you can iterate in seconds instead of waiting on remote CI — and the harness catches schema errors, missing inputs, and runner bugs before they reach a reviewer. If you're building agent tooling, [check out the repo](https://github.com/runxhq/runx) and try `runx harness` on an existing skill to see the pattern.

---

*Written from real experience delivering runx skills through [Frantic](https://gofrantic.com). Verified with runx CLI 0.7.1.*
