# CLAUDE.md

## Project Overview

This is a Claude Code plugin containing AI agent skills for git workflows and developer productivity. The repository provides reusable skill definitions that Claude Code, OpenCode, and Gemini CLI can invoke when working on any codebase.

## Project Structure

```
skills/               # Agent skill definitions
  <skill-name>/
    SKILL.md          # Required: metadata + instructions
    references/       # Optional: detailed documentation loaded on demand
    evals/
      evals.json      # Adversarial evaluation cases
.claude-plugin/       # Plugin metadata for Claude Code
.cursor-plugin/       # Plugin metadata for Cursor (version must match .claude-plugin/plugin.json)
gemini-extension.json # Gemini CLI extension manifest (version must match .claude-plugin/plugin.json)
skills-lock.json      # Reproducible install lock file
EVALUATIONS.md        # Append-only eval results tracker
```

## Agent Skills Specification

All skills MUST conform to the [Agent Skills specification](https://agentskills.io/specification.md). Key requirements are summarized below; the spec is the source of truth when in doubt.

## Frontmatter

New skills go in `skills/<skill-name>/SKILL.md`. Each SKILL.md has YAML frontmatter. Fields per the [Agent Skills spec](https://agentskills.io/specification.md) — **this project requires all fields marked "Project-required"**:

| Field | Required | Constraints |
| --- | --- | --- |
| `name` | Spec-required | 1-64 chars. Lowercase `a-z`, digits, hyphens. No leading/trailing/consecutive hyphens. **Must match parent directory name.** |
| `description` | Spec-required | 1-1024 chars. Describes what the skill does **and when to use it** — this is the primary triggering mechanism. Be specific and slightly "pushy" to avoid under-triggering. |
| `license` | Project-required | `MIT` |
| `compatibility` | Project-required | Base: `Designed for Claude Code or similar AI coding agents.` Extend when needed: add `Requires git`, etc. |
| `metadata` | Project-required | Must include `author`, `version` (semver string e.g. `"1.0.0"`), and `openclaw` (object). |
| `user-invocable` | Project-required | Boolean. `true` for slash-command skills, `false` for contextual auto-trigger skills. |
| `allowed-tools` | Project-required | Space-delimited list of pre-approved tools. |

### ClawHub metadata (`metadata.openclaw`)

| Field | Required | Description |
| --- | --- | --- |
| `emoji` | Yes | Single display emoji |
| `homepage` | Yes | `https://github.com/ibaou-dev/skills` |
| `requires.bins` | Yes | CLI binaries required. Always includes `git` for this repo. |
| `install` | Yes | Array of auto-installable deps. Use `[]` when none needed. |

Example frontmatter:

```yaml
---
name: git-conventional-commits
description: "Creates git commit messages... Use when..."
user-invocable: true
license: MIT
compatibility: Designed for Claude Code or similar AI coding agents. Requires git.
metadata:
  author: ibaou-dev
  version: "1.0.0"
  openclaw:
    emoji: "📝"
    homepage: https://github.com/ibaou-dev/skills
    requires:
      bins:
        - git
    install: []
allowed-tools: Read Glob Grep Bash(git:*)
---
```

**Version discipline:** New skills start at `1.0.0`. When modifying a skill, increment `metadata.version` and the plugin version in all three plugin files (`.claude-plugin/plugin.json`, `.cursor-plugin/plugin.json`, `gemini-extension.json`) — they must always match.

### Description quality

Descriptions are the primary triggering mechanism. A poorly calibrated description wastes context (too broad) or never fires (too vague).

**Too vague** (under-triggering):

```yaml
# Bad — no trigger context
description: Creates git commit messages

# Good — specific triggers
description: "Creates git commit messages following the Conventional Commits specification. Use when creating or reviewing a git commit message, running /git-conventional-commits, or asking about commit format, issue references, scope, or breaking changes — even if the user doesn't explicitly say 'conventional commits'."
```

**Too broad** (over-triggering):

```yaml
# Bad — triggers on all git work
description: Use when doing anything with git.

# Good — narrowed to the specific workflow concern
description: "...Use when the commit message format, type selection, or tracker references are the actual concern."
```

Skills MUST reference the specific workflow concern (commit format, branch naming, issue tracking, etc.) — not generic git concepts. Clear boundary disclaimers with `→ See` cross-references prevent overlap.

## Allowed Tools

Every skill MUST declare `allowed-tools`. Default set for this repo:

```
Read Glob Grep Bash(git:*)
```

Skill-specific extras:

| Extra tool | When to add |
| --- | --- |
| `Edit Write` | Skills that write files (config generation, template creation) |
| `Bash(gh:*)` | GitHub-specific workflows (PR creation, issue linking) |
| `WebFetch` | Skills requiring external doc lookup or spec fetching |
| `Agent` | Orchestrator skills that spawn sub-agents |
| `Bash(claude:*)` | Benchmark/eval skills that run claude -p subprocesses |
| `Bash(opencode:*)` | Benchmark/eval skills that run opencode subprocesses |
| `Bash(python3:*)` | Benchmark/eval skills that run Python aggregation scripts |

## Skill Body

The body contains step-by-step instructions. Use `references/` for depth (referenced via relative links like `[Details](references/details.md)`). Keep file references one level deep from SKILL.md.

### Token budgets

| Budget | Limit | Scope |
| --- | --- | --- |
| Description | ~100 tokens | Loaded at startup for ALL skills |
| SKILL.md (spec) | < 5,000 tokens | Loaded when skill activates |
| SKILL.md (project) | < 2,500 tokens | Project recommendation |
| Full directory | < 10,000 tokens | SKILL.md + all loaded references |

A 100-line SKILL.md is even better. Stay below limits, not at them.

### Top-of-body directives

Place these at the very top of the body, before the first heading:

| Directive | Required | When to include |
| --- | --- | --- |
| **Persona** | Optional | Analytical/generative skills with a well-defined domain |
| **Thinking mode** | Optional | Deep analysis tasks where shallow reasoning produces wrong conclusions |
| **Modes** | Optional | Skills invoked in distinct contexts (audit, coding, review) |

## Evaluation

### Adversarial evaluation design

Evals MUST be adversarial — they test the skill's **unique value**, not common knowledge the model already has. A good eval has a "trap": the natural default model behavior is wrong without the skill, but correct with it.

**Size:** ~10 assertions per 1,000 tokens of skill content (full directory excluding evals), minimum 50 assertions.

**Design principles:**

- Never test common knowledge. If the model passes both with and without the skill, the eval is useless.
- Test the skill's unique guidance — what it teaches that the model wouldn't do by default.
- Create traps — frame the task so the natural approach is wrong. The skill steers toward correct.
- Test judgment, not API knowledge.
- Avoid leading prompts — don't mention the correct approach in the task description.
- Stress-test edge cases and "when NOT to use" guidance.
- When running without-skill evals, do NOT load any overlapping skill that would inflate the baseline.

Store evaluation scenarios in `skills/{name}/evals/evals.json`.

**evals.json format:**

```json
[
  {
    "id": 1,
    "name": "kebab-case-eval-name",
    "description": "What this eval tests",
    "prompt": "The task prompt given to the model",
    "trap": "What the model does wrong without the skill",
    "assertions": [
      { "id": "1.1", "text": "Assertion text — specific, testable, regex-gradeable when possible" },
      { "id": "1.2", "text": "..." }
    ]
  }
]
```

**Grading strategy:** ~80% of assertions should be programmatic (regex, keyword presence, line length check). ~20% may require LLM-as-judge for semantic quality. Flag LLM-graded assertions explicitly in their text.

### Eval workspace

Use `/tmp/<skill-name>-workspace/` as the default workspace for ephemeral eval files. Iteration directories: `/tmp/<skill-name>-workspace/iteration-N/`.

### Running evals via skill-creator

```bash
# Run with and without skill in same turn (parallel subagents)
/skill-creator

# skill-creator provides:
#   eval-viewer/generate_review.py  — static HTML review viewer
#   scripts/aggregate_benchmark.py  — aggregation
#   scripts/run_loop.py             — description optimization loop
#   agents/grader.md, comparator.md, analyzer.md — sub-agent instructions
```

For WSL2 headless environments, use `--static` flag:

```bash
python eval-viewer/generate_review.py ... --static /tmp/review.html
# View via Windows browser: \\wsl.localhost\Ubuntu\tmp\review.html
```

### Evaluation Reporting

Eval results go in `EVALUATIONS.md` at the repo root. Append new skill sections — never overwrite previous runs. The file is wrapped in `<!-- prettier-ignore-start/end -->`.

**Structure per skill:**

```
## `skill-name` — vX.Y.Z

|             | With Skill      | Without Skill   | Delta     |
| ----------- | --------------- | --------------- | --------- |
| **Overall** | **N/N (XX%)** | **N/N (XX%)** | **+XXpp** |

<details>
<summary>Full breakdown (N assertions)</summary>

_Model: claude-sonnet-4-6 · N runs · grading: regex + LLM-as-judge_

| # | Assertion | With | Without |
| --- | --- | --- | --- |
| | **eval-name** — description | **<span class="g">N/N</span>** | **<span class="r">N/N</span>** |
| 1.1 | assertion text | <span class="g">✓</span> | <span class="r">✗</span> |

</details>
```

After updating `EVALUATIONS.md`, update the Summary table at the top and the README.md skill evaluations table.

## Benchmarking with skill-creator

Use `/skill-creator` to drive the full eval loop. The skill-creator is installed as a project-level skill at `.agents/skills/skill-creator/`.

For multi-model benchmarking across Claude and OpenCode free models, use the `skill-benchmark` skill:

```bash
/skill-benchmark
```

**OpenCode discovery symlink:**

```bash
ln -s /home/ibaou/workspace/agentic-skills/skills/<skill-name> ~/.agents/skills/<skill-name>
```

## Workflows

### After updating a skill

After making changes, suggest the following as next steps. Do NOT execute these automatically.

1. Reformat: `npx prettier --write *.md "**/*.md"`
2. Measure tokens:
   - Description: `awk 'NR==1 && /^---$/{found=1; next} found && /^---$/{exit} found && /^description:/{print}' skills/{name}/SKILL.md | tiktoken-cli`
   - SKILL.md: `tiktoken-cli skills/{name}/SKILL.md`
   - Directory: `tiktoken-cli --exclude "evals" skills/{name}/`
3. Update README.md table with measured token counts
4. Increment `metadata.version` in SKILL.md and the plugin version in all 3 plugin files
5. Run skill evaluation via `/skill-creator`
6. Append/update report to `EVALUATIONS.md`
7. Based on eval results, suggest improvements and loop

## Versioning

- **Skill-scoped git tags**: `git-conventional-commits/v1.0.0` — allows per-skill independent versioning
- **Three plugin files must always match**: `.claude-plugin/plugin.json`, `.cursor-plugin/plugin.json`, `gemini-extension.json`
- **skills-lock.json**: tracks resolved refs for reproducible installs
- **After any skill change**: bump `metadata.version` → bump plugin version in all 3 files → `git tag <skill>/v<new>` → `npx skills experimental_install` regenerates lock

```bash
# Install from this repo
npx skills add ibaou-dev/skills --skill git-conventional-commits

# Cross-ref format
`ibaou-dev/skills@git-conventional-commits`
```

## Plugin Configuration

Plugin metadata is defined in `.claude-plugin/plugin.json`, `.cursor-plugin/plugin.json`, and `gemini-extension.json`. All three files MUST have the same `version` value at all times.

## Formats

Write short sentences. Use active voice. Vary sentence length.

### Format 1: Imperative Prose (recommended by skill-creator)

Cut ruthlessly — every word must work. Remove filler words. Use active voice. 3-5 words for impact, then medium length for explanation.

### Format 2: Good / Bad examples

```md
# ✓ Good — {reason}
feat(auth): implement JWT-based authentication

# ✗ Bad — {reason}
add JWT stuff
```

### Format 3: Template / Example-Driven

```md
ALWAYS use this template:

<type>[optional scope]: <description>

Example: feat(auth): implement JWT authentication
```

### Format 4: Bullet Lists (Do / Don't / Avoid)

```md
**Do:**
- Imperative mood in description
- 72-char first-line limit

**Avoid:**
- Past tense ("added", "fixed")
- Vague descriptions ("misc changes")
```

### Format 5: Numbered RFC-style Rules (MUST/MAY/SHOULD)

```md
1. Commits MUST be prefixed with a type
2. The type `feat` MUST be used for new features
3. A scope MAY be provided in parentheses
```
