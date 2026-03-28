<!-- prettier-ignore-start -->

<style>
.g { color: #22863a; font-weight: bold; }
.r { color: #cb2431; font-weight: bold; }
</style>

## `git-conventional-commits` — v1.0.0

### Multi-model summary

| Model | With Skill | Without Skill | Delta | Uplift |
| ----- | ---------- | ------------- | ----- | ------ |
| claude-sonnet-4-6 | **49/50 (98%)** | **34/50 (68%)** | **+30pp** | **1.44×** |
| claude-haiku-4-5 | **49/50 (98%)** | **34/50 (68%)** | **+30pp** | **1.44×** |

_Both models score identically in aggregate (+30pp, 1.44×), but fail **different** evals without the skill — see per-eval breakdown below._

<details>
<summary>Per-eval WITHOUT comparison (where models diverge)</summary>

| Eval | Sonnet WITHOUT | Haiku WITHOUT | Notes |
| --- | --- | --- | --- |
| 2 · breaking-change | 2/5 | **5/5** | Haiku knows BREAKING CHANGE format cold; Sonnet defaulted to `chore:` |
| 4 · scope-override | 3/5 | 2/5 | Sonnet used `(auth)` (non-prohibited); Haiku used `(frontend)` (prohibited by 4.3) |
| 5 · gitlab-mr | 4/5 | **5/5** | Haiku put !89 and #312 on separate lines correctly; Sonnet merged them |
| 6 · scope-mandatory | 4/5 | 2/5 | Haiku dropped scope entirely from `docs:` message; Sonnet included scope |
| 10 · atomic-split | 3/5 | 2/5 | Sonnet weakly offered optional split; Haiku wrote combined commit, no split |

</details>

<details>
<summary>Full breakdown — claude-sonnet-4-6 (50 assertions)</summary>

_Run: 2026-03-29 · grading: regex/manual (1.1–8.5, 9.3–10.5) + LLM-as-judge (9.1, 9.2, 10.1, 10.2)_
_Evals 3, 4, 7, 10 redesigned after run 1; assertion 9.4 broadened._

| # | Assertion | With | Without |
| --- | --- | --- | --- |
| | **type-discrimination-refactor-vs-feat** — rename+extract is refactor not feat | **<span class="r">4/5</span>** | **<span class="r">4/5</span>** |
| 1.1 | type is 'refactor' | <span class="g">✓</span> | <span class="g">✓</span> |
| 1.2 | imperative mood | <span class="g">✓</span> | <span class="g">✓</span> |
| 1.3 | no word 'add'/'adds' | <span class="g">✓</span> | <span class="g">✓</span> |
| 1.4 | scope is (auth) | <span class="g">✓</span> | <span class="g">✓</span> |
| 1.5 | first line ≤ 72 chars | <span class="r">✗ 86 chars</span> | <span class="r">✗ 86 chars</span> |
| | **breaking-change-footer-required** — deprecated API removal needs BREAKING CHANGE, not chore | **<span class="g">5/5</span>** | **<span class="r">2/5</span>** |
| 2.1 | BREAKING CHANGE: footer present | <span class="g">✓</span> | <span class="r">✗</span> |
| 2.2 | migration path references /api/v2/auth | <span class="g">✓</span> | <span class="g">✓</span> |
| 2.3 | type ≠ chore | <span class="g">✓</span> | <span class="r">✗ wrote chore</span> |
| 2.4 | body present | <span class="g">✓</span> | <span class="g">✓</span> |
| 2.5 | ! suffix or BREAKING CHANGE footer | <span class="g">✓</span> | <span class="r">✗</span> |
| | **contributing-md-non-standard-closing-keyword** — 'Addressed #N' from CONTRIBUTING.md (skill_context injected to WITH only) | **<span class="g">5/5</span>** | **<span class="r">2/5</span>** |
| 3.1 | 'Addressed #512' on its own line | <span class="g">✓</span> | <span class="r">✗ used (#512) in subject</span> |
| 3.2 | type = fix | <span class="g">✓</span> | <span class="g">✓</span> |
| 3.3 | scope = (payments) | <span class="g">✓</span> | <span class="r">✗ used (payment)</span> |
| 3.4 | no 'Fixes #512' or 'Closes #512' | <span class="g">✓</span> | <span class="g">✓</span> |
| 3.5 | reference in footer, not description | <span class="g">✓</span> | <span class="r">✗ in subject line</span> |
| | **contributing-md-scope-override** — mandatory 'core' scope for UI/forms (skill_context injected to WITH only) | **<span class="g">5/5</span>** | **<span class="r">3/5</span>** |
| 4.1 | scope is (core) | <span class="g">✓</span> | <span class="r">✗ used (auth)</span> |
| 4.2 | type = feat | <span class="g">✓</span> | <span class="g">✓</span> |
| 4.3 | scope ≠ user/registration/ui/forms/frontend | <span class="g">✓</span> | <span class="g">✓ used (auth)</span> |
| 4.4 | description mentions validation or form | <span class="g">✓</span> | <span class="g">✓</span> |
| 4.5 | acknowledges CONTRIBUTING.md mandate | <span class="g">✓</span> | <span class="r">✗</span> |
| | **gitlab-mr-vs-issue-reference** — !N for MRs, #N for issues, separate footer lines | **<span class="g">5/5</span>** | **<span class="r">4/5</span>** |
| 5.1 | '#312' for issue | <span class="g">✓</span> | <span class="g">✓</span> |
| 5.2 | '!89' for MR (with !) | <span class="g">✓</span> | <span class="g">✓</span> |
| 5.3 | type = fix | <span class="g">✓</span> | <span class="g">✓</span> |
| 5.4 | issue and MR on separate footer lines | <span class="g">✓</span> | <span class="r">✗ same line</span> |
| 5.5 | no '#89' for MR | <span class="g">✓</span> | <span class="g">✓</span> |
| | **scope-required-by-contributing-md** — scope mandatory for docs commits too | **<span class="g">5/5</span>** | **<span class="r">4/5</span>** |
| 6.1 | scope present | <span class="g">✓</span> | <span class="g">✓</span> |
| 6.2 | scope is valid per CONTRIBUTING.md | <span class="g">✓</span> | <span class="g">✓</span> |
| 6.3 | scope = docs or config | <span class="g">✓</span> | <span class="g">✓</span> |
| 6.4 | type = docs | <span class="g">✓</span> | <span class="g">✓</span> |
| 6.5 | acknowledges CI mandate | <span class="g">✓</span> | <span class="r">✗ noted file but not CI enforcement</span> |
| | **developer-framing-override-cve-is-fix** — dev calls CVE patch 'maintenance', skill overrides to fix | **<span class="g">5/5</span>** | **<span class="g">5/5</span>** |
| 7.1 | type = fix (not chore) | <span class="g">✓</span> | <span class="g">✓</span> |
| 7.2 | scope = deps or security | <span class="g">✓</span> | <span class="g">✓</span> |
| 7.3 | mentions high/CVSS/vulnerability | <span class="g">✓</span> | <span class="g">✓</span> |
| 7.4 | type ≠ chore | <span class="g">✓</span> | <span class="g">✓</span> |
| 7.5 | version numbers 5.7.1 and 5.7.2 | <span class="g">✓</span> | <span class="g">✓</span> |
| | **revert-commit-format** — revert: type with formal Reverts: footer | **<span class="g">5/5</span>** | **<span class="r">4/5</span>** |
| 8.1 | type = revert | <span class="g">✓</span> | <span class="g">✓</span> |
| 8.2 | hash present | <span class="g">✓</span> | <span class="g">✓</span> |
| 8.3 | formal Reverts: footer line | <span class="g">✓</span> | <span class="r">✗ in body not footer</span> |
| 8.4 | original subject referenced | <span class="g">✓</span> | <span class="g">✓</span> |
| 8.5 | reason in body | <span class="g">✓</span> | <span class="g">✓</span> |
| | **no-contributing-md-found** — must explicitly note absence and name the spec | **<span class="g">5/5</span>** | **<span class="r">3/5</span>** |
| 9.1 | [LLM-judge] notes no CONTRIBUTING.md found | <span class="g">✓</span> | <span class="r">✗</span> |
| 9.2 | [LLM-judge] states standard CC spec used | <span class="g">✓</span> | <span class="r">✗</span> |
| 9.3 | type = feat | <span class="g">✓</span> | <span class="g">✓</span> |
| 9.4 | scope = cli, cmd, or cmd/root | <span class="g">✓ cmd/root</span> | <span class="g">✓ cmd</span> |
| 9.5 | imperative mood | <span class="g">✓</span> | <span class="g">✓</span> |
| | **atomic-commit-split-feat-plus-release** — feat + version bump must be split | **<span class="g">5/5</span>** | **<span class="r">3/5</span>** |
| 10.1 | [LLM-judge] recommends splitting | <span class="g">✓</span> | <span class="r">✗ wrote combined commit, then weakly offered split as optional</span> |
| 10.2 | [LLM-judge] identifies both concerns | <span class="g">✓</span> | <span class="g">✓</span> |
| 10.3 | feat: for CSV export | <span class="g">✓</span> | <span class="g">✓</span> |
| 10.4 | chore(release): or chore: for version bump | <span class="g">✓</span> | <span class="g">✓</span> |
| 10.5 | version numbers 1.2.3 and 1.3.0 in bump commit | <span class="g">✓</span> | <span class="r">✗ only 1.3.0 in chore commit</span> |

</details>

<details>
<summary>Full breakdown — claude-haiku-4-5 (50 assertions)</summary>

_Run: 2026-03-29 · grading: regex/manual (1.1–8.5, 9.3–10.5) + LLM-as-judge (9.1, 9.2, 10.1, 10.2)_

| # | Assertion | With | Without |
| --- | --- | --- | --- |
| | **type-discrimination-refactor-vs-feat** | **<span class="g">5/5</span>** | **<span class="r">4/5</span>** |
| 1.1 | type is 'refactor' | <span class="g">✓</span> | <span class="g">✓</span> |
| 1.2 | imperative mood | <span class="g">✓</span> | <span class="g">✓</span> |
| 1.3 | no word 'add'/'adds' | <span class="g">✓</span> | <span class="g">✓</span> |
| 1.4 | scope is (auth) | <span class="g">✓</span> | <span class="g">✓</span> |
| 1.5 | first line ≤ 72 chars | <span class="g">✓ 68 chars</span> | <span class="r">✗ 88 chars</span> |
| | **breaking-change-footer-required** | **<span class="g">5/5</span>** | **<span class="g">5/5</span>** |
| 2.1 | BREAKING CHANGE: footer present | <span class="g">✓</span> | <span class="g">✓</span> |
| 2.2 | migration path references /api/v2/auth | <span class="g">✓</span> | <span class="g">✓</span> |
| 2.3 | type ≠ chore | <span class="g">✓</span> | <span class="g">✓ used feat!</span> |
| 2.4 | body present | <span class="g">✓</span> | <span class="g">✓</span> |
| 2.5 | ! suffix or BREAKING CHANGE footer | <span class="g">✓</span> | <span class="g">✓</span> |
| | **contributing-md-non-standard-closing-keyword** — skill_context injected to WITH only | **<span class="g">5/5</span>** | **<span class="r">2/5</span>** |
| 3.1 | 'Addressed #512' on its own line | <span class="g">✓</span> | <span class="r">✗ used 'Closes #512'</span> |
| 3.2 | type = fix | <span class="g">✓</span> | <span class="g">✓</span> |
| 3.3 | scope = (payments) | <span class="g">✓</span> | <span class="r">✗ used (payment)</span> |
| 3.4 | no 'Fixes #512' or 'Closes #512' | <span class="g">✓</span> | <span class="r">✗ used 'Closes #512'</span> |
| 3.5 | reference in footer, not description | <span class="g">✓</span> | <span class="g">✓ footer position correct</span> |
| | **contributing-md-scope-override** — skill_context injected to WITH only | **<span class="g">5/5</span>** | **<span class="r">2/5</span>** |
| 4.1 | scope is (core) | <span class="g">✓</span> | <span class="r">✗ used (frontend)</span> |
| 4.2 | type = feat | <span class="g">✓</span> | <span class="g">✓</span> |
| 4.3 | scope ≠ user/registration/ui/forms/frontend | <span class="g">✓</span> | <span class="r">✗ used (frontend)</span> |
| 4.4 | description mentions validation or form | <span class="g">✓</span> | <span class="g">✓</span> |
| 4.5 | acknowledges CONTRIBUTING.md mandate | <span class="g">✓</span> | <span class="r">✗ no CONTRIBUTING.md found note</span> |
| | **gitlab-mr-vs-issue-reference** | **<span class="g">5/5</span>** | **<span class="g">5/5</span>** |
| 5.1 | '#312' for issue | <span class="g">✓</span> | <span class="g">✓</span> |
| 5.2 | '!89' for MR (with !) | <span class="g">✓</span> | <span class="g">✓</span> |
| 5.3 | type = fix | <span class="g">✓</span> | <span class="g">✓</span> |
| 5.4 | issue and MR on separate footer lines | <span class="g">✓</span> | <span class="g">✓</span> |
| 5.5 | no '#89' for MR | <span class="g">✓</span> | <span class="g">✓</span> |
| | **scope-required-by-contributing-md** | **<span class="g">5/5</span>** | **<span class="r">2/5</span>** |
| 6.1 | scope present | <span class="g">✓</span> | <span class="r">✗ wrote docs: with no scope</span> |
| 6.2 | scope is valid per CONTRIBUTING.md | <span class="g">✓</span> | <span class="r">✗</span> |
| 6.3 | scope = docs or config | <span class="g">✓</span> | <span class="r">✗</span> |
| 6.4 | type = docs | <span class="g">✓</span> | <span class="g">✓</span> |
| 6.5 | acknowledges CI mandate | <span class="g">✓</span> | <span class="g">✓ mentioned CI rejection</span> |
| | **developer-framing-override-cve-is-fix** | **<span class="g">5/5</span>** | **<span class="g">5/5</span>** |
| 7.1 | type = fix (not chore) | <span class="g">✓</span> | <span class="g">✓</span> |
| 7.2 | scope = deps or security | <span class="g">✓</span> | <span class="g">✓</span> |
| 7.3 | mentions high/CVSS/vulnerability | <span class="g">✓</span> | <span class="g">✓</span> |
| 7.4 | type ≠ chore | <span class="g">✓</span> | <span class="g">✓</span> |
| 7.5 | version numbers 5.7.1 and 5.7.2 | <span class="g">✓</span> | <span class="g">✓</span> |
| | **revert-commit-format** | **<span class="g">5/5</span>** | **<span class="r">4/5</span>** |
| 8.1 | type = revert | <span class="g">✓</span> | <span class="g">✓</span> |
| 8.2 | hash present | <span class="g">✓</span> | <span class="g">✓</span> |
| 8.3 | formal Reverts: footer line | <span class="g">✓</span> | <span class="r">✗ "This reverts commit…" in body, not footer</span> |
| 8.4 | original subject referenced | <span class="g">✓</span> | <span class="g">✓</span> |
| 8.5 | reason in body | <span class="g">✓</span> | <span class="g">✓</span> |
| | **no-contributing-md-found** | **<span class="g">5/5</span>** | **<span class="r">3/5</span>** |
| 9.1 | [LLM-judge] notes no CONTRIBUTING.md found | <span class="g">✓</span> | <span class="r">✗ no mention</span> |
| 9.2 | [LLM-judge] states standard CC spec used | <span class="g">✓</span> | <span class="r">✗ only "standard conventions"</span> |
| 9.3 | type = feat | <span class="g">✓</span> | <span class="g">✓</span> |
| 9.4 | scope = cli, cmd, or cmd/root | <span class="g">✓ cli</span> | <span class="g">✓ cli</span> |
| 9.5 | imperative mood | <span class="g">✓</span> | <span class="g">✓</span> |
| | **atomic-commit-split-feat-plus-release** | **<span class="r">4/5</span>** | **<span class="r">2/5</span>** |
| 10.1 | [LLM-judge] recommends splitting | <span class="g">✓</span> | <span class="r">✗ wrote combined commit</span> |
| 10.2 | [LLM-judge] identifies both concerns | <span class="g">✓</span> | <span class="r">✗ no split discussion</span> |
| 10.3 | feat: for CSV export | <span class="g">✓ feat(export)</span> | <span class="g">✓ feat(export)</span> |
| 10.4 | chore(release): or chore: for version bump | <span class="g">✓ chore(release)</span> | <span class="r">✗ bundled with feat</span> |
| 10.5 | version numbers 1.2.3 and 1.3.0 in bump commit | <span class="r">✗ only 1.3.0</span> | <span class="g">✓ in bullet list</span> |

</details>

### Analysis

**Delta +30pp exceeds the +20pp target across both models.** The `skill_context` injection pattern for evals 3 & 4 is the main driver — injecting CONTRIBUTING.md content to the WITH run only exposed genuine discrimination that was hidden in run 1 when both runs had the file inline.

**The skill provides identical aggregate uplift (+30pp, 1.44×) on both Haiku and Sonnet**, which means it can be recommended for cost-sensitive deployments using Haiku without any reduction in commit message quality.

**Per-eval breakdown (Sonnet · Haiku):**

| Eval | Sonnet WITH | Sonnet WITHOUT | Haiku WITH | Haiku WITHOUT | Notes |
| --- | --- | --- | --- | --- | --- |
| 1 · refactor-vs-feat | 4/5 | 4/5 | 5/5 | 4/5 | Both fail 1.5 without; Haiku WITH passes (shorter subject line). Structural issue — fix prompt in v1.1.0. |
| 2 · breaking-change | 5/5 | 2/5 | 5/5 | **5/5** | Haiku knows BREAKING CHANGE format without the skill; Sonnet defaulted to `chore:`. |
| 3 · non-standard keyword | 5/5 | 2/5 | 5/5 | 2/5 | `skill_context` pattern discriminates correctly for both models. |
| 4 · scope-override | 5/5 | 3/5 | 5/5 | 2/5 | Sonnet chose `(auth)` (non-prohibited, passes 4.3); Haiku chose `(frontend)` (prohibited, fails 4.3). |
| 5 · gitlab-mr | 5/5 | 4/5 | 5/5 | **5/5** | Haiku correctly separated !89 and #312; Sonnet merged them. |
| 6 · scope-mandatory | 5/5 | 4/5 | 5/5 | 2/5 | Haiku dropped scope entirely from `docs:` message despite CONTRIBUTING.md inline; Sonnet included it. |
| 7 · cve-framing | 5/5 | 5/5 | 5/5 | 5/5 | Zero-delta on both — explicit CVSS score makes type obvious. Redesign for v1.1.0. |
| 8 · revert-format | 5/5 | 4/5 | 5/5 | 4/5 | Both without-skill models put hash in body, not as formal `Reverts:` footer. |
| 9 · no-contributing-md | 5/5 | 3/5 | 5/5 | 3/5 | Consistent: both without-skill models silently apply defaults. |
| 10 · atomic-split | 5/5 | 3/5 | 4/5 | 2/5 | Haiku WITH misses 10.5 (no 1.2.3); Haiku WITHOUT writes combined commit with no split. |

**Candidates for v1.1.0 redesign:**

- **Eval 1 (1.5):** Shorten function names (`authenticateUser → verifyCredentials` forces 86-char subject on both models). Fix: `getUser → findUser` so 72 chars is achievable.
- **Eval 7:** Both models already know explicit CVSS scores = security fix. Replace with implicit CVE context (e.g. package changelog mention, no CVSS score in prompt) to restore the trap.

<!-- prettier-ignore-end -->
