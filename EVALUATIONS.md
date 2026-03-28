<!-- prettier-ignore-start -->

<style>
.g { color: #22863a; font-weight: bold; }
.r { color: #cb2431; font-weight: bold; }
</style>

# Evaluations

## Summary

| Skill | Version | Assertions | With Skill | Without Skill | Delta | Uplift | Concern |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `git-conventional-commits` | v1.0.0 | 50 | 96% | 80% | +16pp | 1.20× | **Low delta** |
| **Total (1 skill)** | | **50** | **96%** | **80%** | **+16pp** | **1.20×** | |

---

## `git-conventional-commits` — v1.0.0

|             | With Skill      | Without Skill   | Delta     |
| ----------- | --------------- | --------------- | --------- |
| **Overall** | **48/50 (96%)** | **40/50 (80%)** | **+16pp** |

<details>
<summary>Full breakdown (50 assertions)</summary>

_Model: claude-sonnet-4-6 · 1 run · 2026-03-29 · grading: regex/manual (assertions 1.1–8.5, 9.3–10.5) + LLM-as-judge (assertions 9.1, 9.2, 10.1, 10.2)_

| # | Assertion | With | Without |
| --- | --- | --- | --- |
| | **type-discrimination-refactor-vs-feat** — rename+extract is refactor not feat | **<span class="g">4/5</span>** | **<span class="r">4/5</span>** |
| 1.1 | type is exactly 'refactor' | <span class="g">✓</span> | <span class="g">✓</span> |
| 1.2 | imperative mood | <span class="g">✓</span> | <span class="g">✓</span> |
| 1.3 | no word "add" or "adds" | <span class="g">✓</span> | <span class="g">✓</span> |
| 1.4 | scope is (auth) | <span class="g">✓</span> | <span class="g">✓</span> |
| 1.5 | first line ≤ 72 chars | <span class="r">✗ 86 chars</span> | <span class="r">✗ 86 chars</span> |
| | **breaking-change-footer-required** — deprecated API removal needs BREAKING CHANGE, not chore | **<span class="g">5/5</span>** | **<span class="r">2/5</span>** |
| 2.1 | BREAKING CHANGE: footer present | <span class="g">✓</span> | <span class="r">✗</span> |
| 2.2 | migration path references /api/v2/auth | <span class="g">✓</span> | <span class="g">✓</span> |
| 2.3 | type ≠ chore | <span class="g">✓</span> | <span class="r">✗ wrote chore</span> |
| 2.4 | body present | <span class="g">✓</span> | <span class="g">✓</span> |
| 2.5 | ! suffix or BREAKING CHANGE footer | <span class="g">✓</span> | <span class="r">✗</span> |
| | **github-contributing-md-detection** — use exact "Fixes #N" keyword from CONTRIBUTING.md | **<span class="g">5/5</span>** | **<span class="g">5/5</span>** |
| 3.1 | "Fixes #847" on its own line | <span class="g">✓</span> | <span class="g">✓</span> |
| 3.2 | type = fix | <span class="g">✓</span> | <span class="g">✓</span> |
| 3.3 | scope = (db/pool) | <span class="g">✓</span> | <span class="g">✓</span> |
| 3.4 | reference in footer, not description | <span class="g">✓</span> | <span class="g">✓</span> |
| 3.5 | descriptive message | <span class="g">✓</span> | <span class="g">✓</span> |
| | **jira-tracker-key-extraction** — use PLAT-N not #N for Jira | **<span class="g">5/5</span>** | **<span class="g">5/5</span>** |
| 4.1 | "Closes PLAT-2891" in footer | <span class="g">✓</span> | <span class="g">✓</span> |
| 4.2 | type = feat | <span class="g">✓</span> | <span class="g">✓</span> |
| 4.3 | key = PLAT (not invented) | <span class="g">✓</span> | <span class="g">✓</span> |
| 4.4 | reference in footer section | <span class="g">✓</span> | <span class="g">✓</span> |
| 4.5 | no "#2891" GitHub-style ref | <span class="g">✓</span> | <span class="g">✓</span> |
| | **gitlab-mr-vs-issue-reference** — !N for MRs, #N for issues, separate lines | **<span class="g">5/5</span>** | **<span class="r">4/5</span>** |
| 5.1 | "#312" for issue | <span class="g">✓</span> | <span class="g">✓</span> |
| 5.2 | "!89" for MR (with !) | <span class="g">✓</span> | <span class="g">✓</span> |
| 5.3 | type = fix | <span class="g">✓</span> | <span class="g">✓</span> |
| 5.4 | issue and MR on separate footer lines | <span class="g">✓</span> | <span class="r">✗ same line</span> |
| 5.5 | no "#89" for MR | <span class="g">✓</span> | <span class="g">✓</span> |
| | **scope-required-by-contributing-md** — CONTRIBUTING.md mandates scope for docs commits too | **<span class="g">5/5</span>** | **<span class="r">4/5</span>** |
| 6.1 | scope present | <span class="g">✓</span> | <span class="g">✓</span> |
| 6.2 | scope is valid per CONTRIBUTING.md | <span class="g">✓</span> | <span class="g">✓</span> |
| 6.3 | scope = docs or config | <span class="g">✓</span> | <span class="g">✓</span> |
| 6.4 | type = docs | <span class="g">✓</span> | <span class="g">✓</span> |
| 6.5 | acknowledges scope is mandatory per CONTRIBUTING.md | <span class="g">✓</span> | <span class="r">✗ notes CONTRIBUTING.md but not the CI mandate</span> |
| | **dependency-update-cve-is-fix** — CVE patch is fix not chore | **<span class="g">5/5</span>** | **<span class="g">5/5</span>** |
| 7.1 | type = fix | <span class="g">✓</span> | <span class="g">✓</span> |
| 7.2 | scope = deps or security | <span class="g">✓</span> | <span class="g">✓</span> |
| 7.3 | CVE-2021-23337 in body | <span class="g">✓</span> | <span class="g">✓</span> |
| 7.4 | type ≠ chore | <span class="g">✓</span> | <span class="g">✓</span> |
| 7.5 | version numbers 4.17.15 and 4.17.21 | <span class="g">✓</span> | <span class="g">✓</span> |
| | **revert-commit-format** — use revert: type with hash reference and Reverts footer | **<span class="g">5/5</span>** | **<span class="r">4/5</span>** |
| 8.1 | type = revert | <span class="g">✓</span> | <span class="g">✓</span> |
| 8.2 | hash abc123def456789 present | <span class="g">✓</span> | <span class="g">✓</span> |
| 8.3 | formal Reverts: footer line | <span class="g">✓</span> | <span class="r">✗ in body not footer</span> |
| 8.4 | original subject referenced | <span class="g">✓</span> | <span class="g">✓</span> |
| 8.5 | reason in body | <span class="g">✓</span> | <span class="g">✓</span> |
| | **no-contributing-md-found** — must explicitly note CONTRIBUTING.md absence | **<span class="r">4/5</span>** | **<span class="r">2/5</span>** |
| 9.1 | [LLM-judge] notes no CONTRIBUTING.md found | <span class="g">✓</span> | <span class="r">✗</span> |
| 9.2 | [LLM-judge] states standard CC spec used | <span class="g">✓</span> | <span class="r">✗</span> |
| 9.3 | type = feat | <span class="g">✓</span> | <span class="g">✓</span> |
| 9.4 | scope = (cli) | <span class="r">✗ used cmd/root</span> | <span class="r">✗ used cmd</span> |
| 9.5 | imperative mood | <span class="g">✓</span> | <span class="g">✓</span> |
| | **atomic-commit-split-suggestion** — mixed changeset must be split | **<span class="g">5/5</span>** | **<span class="g">5/5</span>** |
| 10.1 | [LLM-judge] recommends splitting | <span class="g">✓</span> | <span class="g">✓</span> |
| 10.2 | [LLM-judge] identifies 3+ distinct concerns | <span class="g">✓</span> | <span class="g">✓</span> |
| 10.3 | chore/build for Node.js bump | <span class="g">✓</span> | <span class="g">✓</span> |
| 10.4 | feat(api) for health endpoint | <span class="g">✓</span> | <span class="g">✓</span> |
| 10.5 | fix for serializer | <span class="g">✓</span> | <span class="g">✓</span> |

</details>

### Analysis & Eval Improvements Needed

Delta of **+16pp is below the +20pp target**. Root causes:

**Evals with 0 delta (need stronger traps):**

- **Eval 3 & 4** — zero delta because the full CONTRIBUTING.md text was embedded in the prompt, making the correct answer obvious to the model. Fix: supply a CONTRIBUTING.md as a file that the model must detect and read (using Glob), rather than inlining it. Without-skill model won't know to look for it.
- **Eval 7** — `claude-sonnet-4-6` already classifies CVE security patches as `fix` without skill guidance. Trap didn't work for this model. Fix: test a less obvious CVE scenario, e.g. a transitive dependency update or a private package update where the CVE context is buried.
- **Eval 10** — `claude-sonnet-4-6` already recommends atomic commits without skill guidance. Fix: use a subtler mixing case — e.g. test + feature + version bump, where the test looks like it belongs with the feature.

**Assertion calibration issues:**

- **Assertion 9.4** expects scope `cli` but neither model chose it. Both chose `cmd` or `cmd/root` which are reasonable alternatives. Assertion was too strict. Fix: accept `cli`, `cmd`, or `cmd/root` as valid.
- **Assertion 1.5** — both WITH and WITHOUT generated a 86-char first line. The trap (line length) was shared by both, adding noise but not signal. Fix: make the eval prompt provide a shorter change description so the model can fit in 72 chars.

**Recommended next steps to reach +20pp:**

1. Redesign evals 3 & 4 to use file-based CONTRIBUTING.md detection (create a `/tmp/test-repo-workspace/` with the file on disk)
2. Replace eval 7 with a subtler CVE trap
3. Replace eval 10 with a subtler atomicity trap
4. Fix assertion 9.4 to accept cmd/cmd/root/cli variants
5. Re-run and target +25pp before tagging v1.1.0

<!-- prettier-ignore-end -->
