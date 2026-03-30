---
name: skill-benchmark
description:
  "Benchmarks any Agent Skills skill across multiple AI models by running evals
  with and without the skill loaded. Produces with/without/delta pass-rate tables
  across any provider — OpenCode free models, OpenRouter, local models, or the
  current Claude session. Use when you want to quantify skill uplift, compare
  models, or validate that a skill works across providers. Use when asked to
  benchmark, measure, or compare a skill's performance."
user-invocable: true
license: MIT
compatibility:
  Designed for Claude Code or similar AI coding agents. Requires python3. Claude
  CLI and opencode CLI are optional depending on which executor types are used.
metadata:
  author: ibaou-dev
  version: "1.1.0"
  openclaw:
    emoji: "📊"
    homepage: https://github.com/ibaou-dev/skills
    requires:
      bins:
        - python3
    install: []
allowed-tools: Read Glob Grep Bash(python3:*) Bash(uv:*) Bash(git:*) Agent
---

**Persona:** You are a benchmark engineer. Measure skill uplift with rigor — no
cherry-picking, no skipped baselines, clear results.

## Step 1: Verify evals exist

```bash
cat skills/<skill-name>/evals/evals.json | python3 -c "import json,sys; d=json.load(sys.stdin); print(f'{len(d)} evals, {sum(len(e[\"assertions\"]) for e in d)} assertions')"
```

If missing, stop and ask the user to create evals first (see CLAUDE.md eval design
guidelines).

## Step 2: Check / create bench config

Look for `.bench/<skill-name>/bench.json` (gitignored, not tracked).

If missing, scaffold one:

```bash
python3 scripts/benchmark.py --skill skills/<skill-name> --init-config
# Then edit .bench/<skill-name>/bench.json to configure executors/judges
```

The config controls which models run and how skill loading works. See
[references/bench-config.sample.json](references/bench-config.sample.json) for a
full example with all executor/judge types.

**Executor types:**

| Type | How it runs | Skill "with" mode |
| --- | --- | --- |
| `opencode` | `opencode run` subprocess | symlink auto-managed |
| `openai_compat` | POST `/v1/chat/completions` (OpenRouter, OpenCode Zen, any OpenAI-compat API) | skill body injected into prompt |
| `local` | POST `/api/v1/chat` custom schema `{system_prompt, input}` | `system_prompt` field |
| `session` | `claude -p` subprocess | skill body injected into prompt |

**Judge types:** `none` (regex only) · `session` (current session model via `claude -p`) · `openai_compat` (any external LLM)

Hybrid: run a local/free model as executor + `session` as judge to get LLM-graded
assertions without a second paid API call.

## Step 3: Run benchmark

```bash
# Config-driven (recommended — runs all configured models in one shot)
python3 scripts/benchmark.py --config .bench/<skill-name>/bench.json

# Ad-hoc single run
python3 scripts/benchmark.py \
  --skill skills/<skill-name> \
  --executor opencode --model opencode/minimax-m2.5-free \
  --judge none --mode both

# Filter to specific evals
python3 scripts/benchmark.py --config ... --evals 1,3,9
```

Results append automatically to `.bench/<skill-name>/results.ndjson`.

## Step 4: Review results

```bash
# Merged table — latest run per label
python3 scripts/benchmark.py --skill skills/<skill-name> --report

# Per-assertion detail
python3 scripts/benchmark.py --config ... --detail
```

## Step 5: Record and iterate

1. Copy the `EVALUATIONS.md row:` line printed after each run into the skill's
   `EVALUATIONS.md` (per-skill file) and the repo-root `EVALUATIONS.md` summary.
2. Adjust the skill, bump `metadata.version` in SKILL.md, re-run to see delta change.
3. Compare runs via `--report` to track improvement across iterations.

→ See [references/bench-config.sample.json](references/bench-config.sample.json)
for config schema with all executor/judge types
→ See [references/runner-opencode.md](references/runner-opencode.md) for raw
OpenCode CLI reference
→ See [references/runner-claude.md](references/runner-claude.md) for raw claude -p
reference
→ See [references/metrics-format.md](references/metrics-format.md) for results
schema and EVALUATIONS.md format
