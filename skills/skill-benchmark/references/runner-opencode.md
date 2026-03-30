# OpenCode Runner Reference

> **Note:** For benchmarking, prefer `scripts/benchmark.py --executor opencode`.
> It handles symlink management, workspace isolation, ANSI stripping, and results
> persistence automatically. This file documents the underlying CLI for reference.


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
opencode run --model <model-id> "Your prompt here"

# With a skill loaded: symlink skill first, then run — opencode auto-triggers it
ln -sf /path/to/skills/<name> ~/.agents/skills/<name>
opencode run --model <model-id> "Your prompt here"

# Without skill: remove symlink or run in an isolated workspace
opencode run --dir /tmp/empty-workspace --model <model-id> "Your prompt here"
```

Note: `--no-interactive` and `--skill` flags do not exist in opencode 1.3.4+.
Skill loading is automatic when the skill is symlinked into `~/.agents/skills/`.

## Available free models (as of 2026-03)

Check `opencode models` for the current list. Common free tiers:

```bash
opencode models list
```

Typical free model IDs vary by OpenCode version. Use `opencode models list` to
discover available IDs before benchmarking.

## Manual batch eval pattern (if not using benchmark.py)

```bash
#!/bin/bash
MODEL="<model-id>"
SKILL_NAME="<skill-name>"
SKILL_PATH="/path/to/skills/$SKILL_NAME"
WORKSPACE="/tmp/$SKILL_NAME-workspace/benchmark"
EVALS_JSON="skills/$SKILL_NAME/evals/evals.json"

# With skill: ensure symlink, run in isolated workspace
ln -sf "$SKILL_PATH" ~/.agents/skills/"$SKILL_NAME"
mkdir -p "$WORKSPACE/$MODEL/with_skill"
for i in $(seq 1 10); do
  PROMPT=$(jq -r ".[] | select(.id == $i) | .prompt" "$EVALS_JSON")
  opencode run --dir "$WORKSPACE" --model "$MODEL" "$PROMPT" \
    > "$WORKSPACE/$MODEL/with_skill/eval-$i-output.txt"
done

# Without skill: remove symlink
rm -f ~/.agents/skills/"$SKILL_NAME"
mkdir -p "$WORKSPACE/$MODEL/without_skill"
for i in $(seq 1 10); do
  PROMPT=$(jq -r ".[] | select(.id == $i) | .prompt" "$EVALS_JSON")
  opencode run --dir "$WORKSPACE" --model "$MODEL" "$PROMPT" \
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
