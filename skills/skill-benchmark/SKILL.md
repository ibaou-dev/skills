---
name: skill-benchmark
description:
  "Benchmarks any Agent Skills skill across multiple AI models by running evals
  with and without the skill. Produces with/without/delta pass-rate tables,
  timing, and token metrics per model. Use when you want to quantify skill
  uplift, compare models, or validate that a skill works across Claude and
  OpenCode free models."
user-invocable: true
license: MIT
compatibility:
  Designed for Claude Code or similar AI coding agents. Requires claude CLI and
  optionally opencode CLI.
metadata:
  author: ibaou-dev
  version: "1.0.0"
  openclaw:
    emoji: "📊"
    homepage: https://github.com/ibaou-dev/skills
    requires:
      bins:
        - claude
    install: []
allowed-tools:
  Read Glob Grep Bash(claude:*) Bash(opencode:*) Bash(python3:*) Agent
---

**Persona:** You are a benchmark engineer. You measure skill uplift with rigor —
no cherry-picking, no skipped baselines, clear confidence intervals.

## Step 1: Load Evals

Read `<skill>/evals/evals.json`. Confirm assertions are present. Count total
assertions.

If no evals.json exists, stop and ask the user to create one using the eval
design guidelines in CLAUDE.md.

## Step 2: Configure Models

Present available runners:

| Runner                | Command                    | Notes                     |
| --------------------- | -------------------------- | ------------------------- |
| `claude`              | `claude -p --skill <path>` | Current Claude Code model |
| `opencode:<model-id>` | `opencode --model <id>`    | Free models via OpenCode  |

Ask the user which models to benchmark. Default: `claude` only.

For OpenCode multi-model benchmarking, see
[references/runner-opencode.md](references/runner-opencode.md).

## Step 3: Run Matrix

For each model × {`with_skill`, `without_skill`}, spawn parallel subagents (all
runs in the same turn). Save outputs to:

```
/tmp/<skill-name>-workspace/benchmark/
  <model-name>/
    with_skill/
      eval-<id>-output.txt
      timing.json
    without_skill/
      eval-<id>-output.txt
      timing.json
```

See [references/runner-claude.md](references/runner-claude.md) for `claude -p`
invocation syntax.

## Step 4: Grade

For each run output, grade against all assertions:

- **Regex-gradeable assertions:** apply regex programmatically
- **`[LLM-judge]` assertions:** spawn a grader subagent reading the grader
  prompt from `.agents/skills/skill-creator/agents/grader.md`

Save `grading.json` per run:

```json
{
  "eval_id": 1,
  "model": "claude-sonnet-4-6",
  "mode": "with_skill",
  "assertions": [
    { "id": "1.1", "pass": true },
    { "id": "1.2", "pass": false, "evidence": "used 'added' not imperative" }
  ],
  "pass_count": 4,
  "total": 5
}
```

## Step 5: Aggregate

Build cross-model benchmark table using
`python3 .agents/skills/skill-creator/scripts/aggregate_benchmark.py`.

Output format:

| Model               | With | Without | Delta | Tokens | Time |
| ------------------- | ---- | ------- | ----- | ------ | ---- |
| claude-sonnet-4-6   | 96%  | 54%     | +42pp | 8400   | 23s  |
| opencode:free-model | 78%  | 41%     | +37pp | 6200   | 18s  |

See [references/metrics-format.md](references/metrics-format.md) for
benchmark.json schema.

## Step 6: Output

1. Print the markdown table to the conversation
2. Append results to `EVALUATIONS.md` in the skill's repo following the format
   in CLAUDE.md
3. Optionally generate static HTML review:

```bash
python3 .agents/skills/skill-creator/eval-viewer/generate_review.py \
  --workspace /tmp/<skill-name>-workspace/benchmark \
  --static /tmp/review.html
# WSL2: open \\wsl.localhost\Ubuntu\tmp\review.html in Windows browser
```

→ See [references/runner-claude.md](references/runner-claude.md) for claude -p
syntax → See [references/runner-opencode.md](references/runner-opencode.md) for
OpenCode invocation → See
[references/metrics-format.md](references/metrics-format.md) for benchmark.json
schema
