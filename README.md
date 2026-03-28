# agentic-skills

AI agent skills for git workflows and developer productivity. Compatible with
Claude Code, OpenCode, and Gemini CLI.

## Skills

<!-- prettier-ignore-start -->

| # | Skill | Description | User-invocable | Version | Directory (tok) | Ultrathink |
| --- | --- | --- | --- | --- | --- | --- |
| ✅ | [`git-conventional-commits`](skills/git-conventional-commits/) | Creates git commit messages following Conventional Commits spec with CONTRIBUTING.md detection | Yes | v1.0.0 | — | — |
| 👷 | [`skill-benchmark`](skills/skill-benchmark/) | Multi-model benchmark orchestrator for any Agent Skills skill | Yes | v1.0.0 | 0 | — |

<!-- prettier-ignore-end -->

## Install

```bash
# All skills
npx skills add ibaou-dev/skills

# Single skill
npx skills add ibaou-dev/skills --skill git-conventional-commits
```

## Skill evaluations

| Skill | Model | Version | Assertions | With Skill | Without Skill | Delta | Uplift |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [`git-conventional-commits`](skills/git-conventional-commits/EVALUATIONS.md) | claude-sonnet-4-6 | v1.0.0 | 50 | 98% | 68% | +30pp | 1.44× |
| [`git-conventional-commits`](skills/git-conventional-commits/EVALUATIONS.md) | claude-haiku-4-5 | v1.0.0 | 50 | 98% | 68% | +30pp | 1.44× |

## Development

See [CLAUDE.md](CLAUDE.md) for authoring guidelines, eval setup, and
benchmarking workflow.

## License

MIT
