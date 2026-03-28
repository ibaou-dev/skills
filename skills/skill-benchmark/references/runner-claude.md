# Claude Runner Reference

## Basic invocation

```bash
# Run a prompt with claude -p (non-interactive, print mode)
claude -p "Your prompt here"

# Run with a skill loaded
claude -p --skill /path/to/skill "Your prompt here"

# Run with skill and pipe output to file
claude -p --skill /path/to/skill "Your prompt here" > output.txt

# Run with explicit model
claude -p --model claude-sonnet-4-6 "Your prompt here"
```

## Skill path conventions

```bash
# Absolute path to skill directory (contains SKILL.md)
claude -p --skill /home/ibaou/workspace/agentic-skills/skills/git-conventional-commits "..."

# Relative path (from cwd)
claude -p --skill ./skills/git-conventional-commits "..."
```

## Without-skill baseline

```bash
# No --skill flag — pure model, no skill loaded
claude -p "Your prompt here"

# Explicitly disable all skills from auto-loading (if needed)
claude -p --no-skills "Your prompt here"
```

## Capturing timing and token usage

```bash
# Time the invocation
time claude -p --skill ./skills/git-conventional-commits "prompt" > output.txt

# Get token usage from response (claude -p may print usage to stderr)
claude -p "prompt" 2>timing.txt 1>output.txt
```

## Batch eval runner pattern

```bash
#!/bin/bash
# Run all evals for a skill
SKILL_PATH="./skills/git-conventional-commits"
WORKSPACE="/tmp/git-conventional-commits-workspace/benchmark"

mkdir -p "$WORKSPACE/claude/with_skill" "$WORKSPACE/claude/without_skill"

# With skill
for i in $(seq 1 10); do
  PROMPT=$(jq -r ".[] | select(.id == $i) | .prompt" skills/git-conventional-commits/evals/evals.json)
  claude -p --skill "$SKILL_PATH" "$PROMPT" > "$WORKSPACE/claude/with_skill/eval-$i-output.txt"
done

# Without skill
for i in $(seq 1 10); do
  PROMPT=$(jq -r ".[] | select(.id == $i) | .prompt" skills/git-conventional-commits/evals/evals.json)
  claude -p "$PROMPT" > "$WORKSPACE/claude/without_skill/eval-$i-output.txt"
done
```

## Parallel eval pattern (via skill-creator subagents)

When running in Claude Code with the skill-creator, spawn parallel subagents — all with_skill and without_skill runs in the same turn:

```
# In skill-creator context, the Agent tool is used to spawn:
# - Agent 1: run eval 1 with_skill
# - Agent 2: run eval 1 without_skill
# - Agent 3: run eval 2 with_skill
# ...all in parallel
```

This reduces total wall-clock time from O(N*2) to O(max_parallelism).

## Output format

`claude -p` outputs the model's response to stdout. In benchmark context:
- Save raw response to `eval-<id>-output.txt`
- Grade against assertions post-hoc
- LLM-judge assertions require a second `claude -p` call with the grader prompt

## Notes

- `claude -p` is non-interactive — safe for scripting
- Skills are loaded from the directory containing `SKILL.md`
- The skill's `allowed-tools` frontmatter gates which tools are available during the run
- Use the same model version for with/without comparisons to isolate skill effect
