# OpenCode Runner Reference

## Discovery symlink setup

Make skills discoverable to OpenCode by symlinking into `~/.agents/skills/`:

```bash
# Symlink a skill for OpenCode discovery
ln -s /home/ibaou/workspace/agentic-skills/skills/git-conventional-commits \
  ~/.agents/skills/git-conventional-commits

# Verify
ls -la ~/.agents/skills/
```

OpenCode auto-discovers skills from `~/.agents/skills/` and `.agents/skills/` in
the project directory.

## Basic invocation

```bash
# Non-interactive run with a specific model
opencode run --model <model-id> --no-interactive "Your prompt here"

# With a skill loaded (after symlinking to ~/.agents/skills/)
opencode run --model <model-id> --skill git-conventional-commits --no-interactive "prompt"

# Pipe prompt from file (for long prompts)
opencode run --model <model-id> --no-interactive < prompt.txt
```

## Available free models (as of 2026-03)

Check `opencode models` for the current list. Common free tiers:

```bash
opencode models list
```

Typical free model IDs vary by OpenCode version. Use `opencode models list` to
discover available IDs before benchmarking.

## Batch eval pattern

```bash
#!/bin/bash
MODEL="<model-id>"
SKILL_PATH="/home/ibaou/workspace/agentic-skills/skills/git-conventional-commits"
WORKSPACE="/tmp/git-conventional-commits-workspace/benchmark"
SKILL_NAME="git-conventional-commits"

# Ensure symlink exists
ln -sf "$SKILL_PATH" ~/.agents/skills/"$SKILL_NAME"

mkdir -p "$WORKSPACE/$MODEL/with_skill" "$WORKSPACE/$MODEL/without_skill"

# With skill
for i in $(seq 1 10); do
  PROMPT=$(jq -r ".[] | select(.id == $i) | .prompt" skills/git-conventional-commits/evals/evals.json)
  opencode run --model "$MODEL" --skill "$SKILL_NAME" --no-interactive "$PROMPT" \
    > "$WORKSPACE/$MODEL/with_skill/eval-$i-output.txt"
done

# Without skill
for i in $(seq 1 10); do
  PROMPT=$(jq -r ".[] | select(.id == $i) | .prompt" skills/git-conventional-commits/evals/evals.json)
  opencode run --model "$MODEL" --no-interactive "$PROMPT" \
    > "$WORKSPACE/$MODEL/without_skill/eval-$i-output.txt"
done
```

## Output format

Same as `claude -p` — raw model response to stdout. Grade post-hoc against
evals.json assertions.

## Notes

- `--no-interactive` is required for scripting; omit for interactive sessions
- OpenCode free models may have rate limits — add `sleep 1` between calls if
  needed
- Model availability and IDs change; always run `opencode models list` first
- Token counts in OpenCode output may differ from Claude API token counts
- For fair comparison, run Claude and OpenCode benchmarks with the same eval
  prompts and workspace
