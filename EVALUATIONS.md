<!-- prettier-ignore-start -->

<style>
.g { color: #22863a; font-weight: bold; }
.r { color: #cb2431; font-weight: bold; }
</style>

# Evaluations

## Summary

| Skill | Model | Version | Assertions | With Skill | Without Skill | Delta | Uplift | Concern |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [`git-conventional-commits`](skills/git-conventional-commits/EVALUATIONS.md) | claude-sonnet-4-6 | v1.1.0 | 50 | 100% | 70% | +30pp | 1.43× | |
| [`git-conventional-commits`](skills/git-conventional-commits/EVALUATIONS.md) | claude-haiku-4-5 | v1.1.0 | 50 | 94% | 68% | +26pp | 1.38× | |
| [`git-conventional-commits`](skills/git-conventional-commits/EVALUATIONS.md) | qwen/qwen3.5-9b | v1.1.0 | 50 | 82% | 62% | +20pp⚠ | 1.32× | eval 10 WITHOUT timeout |
| [`git-conventional-commits`](skills/git-conventional-commits/EVALUATIONS.md) | qwen3-coder-30b-a3b-instruct | v1.1.0 | 50 | 80% | 64% | +16pp | 1.25× | Low delta |
| [`git-conventional-commits`](skills/git-conventional-commits/EVALUATIONS.md) | nvidia/nemotron-3-nano-30b-a3b | v1.0.0 | 50 | 80% | 54% | +26pp | 1.48× | ⚠ lower abs. score |

<!-- prettier-ignore-end -->
