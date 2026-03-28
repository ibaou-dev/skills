#!/usr/bin/env python3
"""
Benchmark any skill's evals.json against models via OpenRouter API.

Usage:
    python scripts/benchmark_openrouter.py \\
        --skill skills/git-conventional-commits \\
        --model nvidia/nemotron-3-nano-30b-a3b:free \\
        --mode both

    # With skill only (fast check):
    python scripts/benchmark_openrouter.py \\
        --skill skills/git-conventional-commits \\
        --model mistralai/mistral-7b-instruct:free \\
        --mode with

    # Custom judge model for LLM-as-judge assertions:
    python scripts/benchmark_openrouter.py \\
        --skill skills/git-conventional-commits \\
        --model nvidia/nemotron-3-nano-30b-a3b:free \\
        --judge-model openai/gpt-4o-mini \\
        --mode both

    # Save results to JSON:
    python scripts/benchmark_openrouter.py ... --output results.json

Config (in priority order):
    1. CLI flag:    --api-key sk-or-...
    2. Env var:     OPENROUTER_API_KEY=sk-or-...
    3. .env file:   OPENROUTER_API_KEY=sk-or-...
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path
from typing import Optional

import requests

OPENROUTER_API = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_TEMPERATURE = 0.2
REQUEST_TIMEOUT = 90  # seconds
RETRY_DELAY = 5       # seconds between retries on rate-limit


# ---------------------------------------------------------------------------
# Config helpers
# ---------------------------------------------------------------------------

def load_dotenv(path: Path = Path(".env")) -> None:
    """Load key=value pairs from a .env file into os.environ (no overwrite)."""
    if not path.exists():
        return
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        k, v = k.strip(), v.strip().strip('"').strip("'")
        os.environ.setdefault(k, v)


def get_api_key(cli_value: Optional[str]) -> str:
    load_dotenv()
    key = cli_value or os.environ.get("OPENROUTER_API_KEY", "")
    if not key:
        sys.exit(
            "ERROR: No OpenRouter API key found.\n"
            "  Set OPENROUTER_API_KEY in your environment, .env file, or pass --api-key."
        )
    return key


# ---------------------------------------------------------------------------
# Skill loading
# ---------------------------------------------------------------------------

def load_skill_body(skill_dir: Path) -> str:
    """Read SKILL.md and strip YAML frontmatter."""
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return ""
    text = skill_md.read_text()
    if text.startswith("---"):
        parts = text.split("---", 2)
        return parts[2].strip() if len(parts) >= 3 else text
    return text


def load_evals(skill_dir: Path) -> list[dict]:
    evals_file = skill_dir / "evals" / "evals.json"
    if not evals_file.exists():
        sys.exit(f"ERROR: evals.json not found at {evals_file}")
    return json.loads(evals_file.read_text())


def build_prompt(eval_case: dict, skill_body: str, mode: str) -> str:
    """Build the full prompt for a single eval case."""
    user_prompt = eval_case["prompt"]

    if mode == "without":
        return user_prompt

    # WITH skill: prepend skill body
    skill_context = eval_case.get("skill_context", "")
    if skill_context:
        injected = (
            f"{skill_body}\n\n"
            f"--- CONTRIBUTING.md content (found at repo root) ---\n"
            f"{skill_context}\n"
            f"--- END CONTRIBUTING.md ---\n\n"
            f"{user_prompt}"
        )
    else:
        injected = f"{skill_body}\n\n---\n\nNow write the conventional commit message for the following scenario:\n\n{user_prompt}"
    return injected


# ---------------------------------------------------------------------------
# OpenRouter API
# ---------------------------------------------------------------------------

def call_model(api_key: str, model: str, prompt: str, retries: int = 2) -> str:
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/ibaou-dev/skills",
        "X-Title": "agentic-skills benchmark",
    }
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": DEFAULT_TEMPERATURE,
    }
    for attempt in range(retries + 1):
        try:
            resp = requests.post(
                OPENROUTER_API,
                headers=headers,
                json=payload,
                timeout=REQUEST_TIMEOUT,
            )
            if resp.status_code == 429 and attempt < retries:
                print(f"  [rate-limit] retrying in {RETRY_DELAY}s…", flush=True)
                time.sleep(RETRY_DELAY)
                continue
            resp.raise_for_status()
            data = resp.json()
            return data["choices"][0]["message"]["content"]
        except requests.RequestException as e:
            if attempt == retries:
                raise
            time.sleep(RETRY_DELAY)
    return ""


# ---------------------------------------------------------------------------
# Assertion grader
# ---------------------------------------------------------------------------

def _extract_commit(text: str) -> str:
    """
    Extract the commit message from a code block if the model wrapped its output.
    Many smaller models write:
        Here is the commit:
        ```
        fix(auth): ...
        ```
    This returns just the content inside the first code block, stripped.
    Falls back to the full text if no code block is found.
    """
    # Match ```...``` (with optional language tag on the opening fence)
    m = re.search(r"```[a-z]*\n(.*?)```", text, re.DOTALL)
    if m:
        return m.group(1).strip()
    # Also handle single-backtick inline commits (rare but happens)
    m = re.search(r"`([a-z]+(?:\([^)]+\))?!?:.+)`", text)
    if m:
        return m.group(1).strip()
    return text.strip()


def _first_line(text: str) -> str:
    """First non-empty line of the extracted commit message."""
    commit = _extract_commit(text)
    for line in commit.splitlines():
        if line.strip():
            return line.strip()
    return ""


def _scope(first_line: str) -> str:
    m = re.match(r"^[a-z]+\(([^)]+)\)", first_line)
    return m.group(1) if m else ""


def _desc(first_line: str) -> str:
    m = re.match(r"^[a-z]+(?:\([^)]+\))?!?:\s*(.+)", first_line)
    return m.group(1).strip() if m else first_line


def _in_footer(text: str, pattern: str) -> bool:
    """Return True if pattern appears in a footer line (after a blank line) in the commit body."""
    commit = _extract_commit(text)
    lines = commit.splitlines()
    after_blank = False
    for i, line in enumerate(lines):
        if i > 0 and not lines[i - 1].strip():
            after_blank = True
        if after_blank and pattern in line:
            return True
    return False


def llm_judge(api_key: str, judge_model: str, assertion_text: str, response: str) -> tuple[bool, str]:
    """Ask a capable model to judge a semantic assertion."""
    prompt = (
        f"You are grading an AI-generated git commit message against an assertion.\n\n"
        f"ASSERTION:\n{assertion_text}\n\n"
        f"MODEL OUTPUT:\n{response}\n\n"
        f"Does the model output satisfy the assertion? "
        f"Reply with exactly one word: PASS or FAIL, then optionally a brief reason."
    )
    try:
        result = call_model(api_key, judge_model, prompt, retries=1)
        passed = result.strip().upper().startswith("PASS")
        note = result.strip() if not passed else ""
        return passed, note
    except Exception as e:
        return False, f"judge error: {e}"


def grade_assertion(
    assertion: dict,
    response: str,
    api_key: str = "",
    judge_model: str = "",
) -> tuple[bool, str]:
    """Grade one assertion. Returns (passed, note)."""
    aid = assertion["id"]
    text = assertion["text"]
    r = response                 # full response — for narrative/acknowledgment checks
    c = _extract_commit(response) # commit message only — for format/structure checks
    fl = _first_line(r)          # first line of commit (code-fence-aware)

    # ---- Eval 1 ----
    if aid == "1.1":
        ok = fl.lower().startswith("refactor")
        return ok, "" if ok else f"starts with: {fl[:30]}"

    if aid == "1.2":
        desc = _desc(fl)
        first_word = desc.split()[0].lower() if desc.split() else ""
        good = {"extract", "rename", "restructure", "move", "refactor", "update",
                "replace", "change", "split", "break", "reorganize"}
        ok = first_word in good
        return ok, "" if ok else f"first word: '{first_word}'"

    if aid == "1.3":
        fl_lower = fl.lower()
        ok = " add " not in fl_lower and not fl_lower.startswith("add ") and " adds " not in fl_lower
        return ok, "" if ok else "contains 'add'/'adds'"

    if aid == "1.4":
        ok = "(auth)" in fl
        return ok, "" if ok else f"no (auth): {fl[:60]}"

    if aid == "1.5":
        ok = len(fl) <= 72
        return ok, "" if ok else f"{len(fl)} chars"

    # ---- Eval 2 ----
    if aid == "2.1":
        ok = "BREAKING CHANGE:" in c
        return ok, "" if ok else "no BREAKING CHANGE: footer"

    if aid == "2.2":
        ok = "/api/v2/auth" in r or ("v2" in r.lower() and "auth" in r.lower())
        return ok, "" if ok else "no v2 migration path"

    if aid == "2.3":
        ok = not fl.lower().startswith("chore")
        return ok, "" if ok else "type is chore"

    if aid == "2.4":
        non_empty = [l for l in c.splitlines() if l.strip()]
        ok = len(non_empty) > 1
        return ok, "" if ok else "no body (single line only)"

    if aid == "2.5":
        ok = "!" in fl or "BREAKING CHANGE:" in c
        return ok, "" if ok else "neither ! suffix nor BREAKING CHANGE footer"

    # ---- Eval 3 ----
    if aid == "3.1":
        ok = any(
            re.match(r"Addressed #512", line.strip())
            for line in c.splitlines()
        )
        return ok, "" if ok else "no 'Addressed #512' footer line"

    if aid == "3.2":
        ok = fl.lower().startswith("fix")
        return ok, "" if ok else f"type: {fl[:20]}"

    if aid == "3.3":
        ok = "(payments)" in fl
        return ok, "" if ok else f"scope: {_scope(fl) or 'none'}"

    if aid == "3.4":
        ok = "Fixes #512" not in c and "Closes #512" not in c and "Resolves #512" not in c
        return ok, "" if ok else "used Fixes/Closes/Resolves #512"

    if aid == "3.5":
        ok = _in_footer(r, "#512") and "#512" not in fl
        return ok, "" if ok else "reference in subject or not in footer"

    # ---- Eval 4 ----
    if aid == "4.1":
        ok = "(core)" in fl
        return ok, "" if ok else f"scope: {_scope(fl) or 'none'}"

    if aid == "4.2":
        ok = fl.lower().startswith("feat")
        return ok, "" if ok else f"type: {fl[:20]}"

    if aid == "4.3":
        bad = {"(user)", "(registration)", "(ui)", "(forms)", "(frontend)"}
        ok = not any(s in fl for s in bad)
        return ok, "" if ok else f"bad scope: {_scope(fl)}"

    if aid == "4.4":
        ok = any(w in r.lower() for w in ["validation", "validate", "form", "registration"])
        return ok, "" if ok else "no mention of validation/form"

    if aid == "4.5":
        ok = "contributing" in r.lower()
        return ok, "" if ok else "no CONTRIBUTING.md acknowledgment"

    # ---- Eval 5 ----
    if aid == "5.1":
        ok = "#312" in c
        return ok, "" if ok else "no #312"

    if aid == "5.2":
        ok = "!89" in c
        return ok, "" if ok else "no !89 (exclamation prefix)"

    if aid == "5.3":
        ok = fl.lower().startswith("fix")
        return ok, "" if ok else f"type: {fl[:20]}"

    if aid == "5.4":
        lines = c.splitlines()
        idx_312 = next((i for i, l in enumerate(lines) if "#312" in l), -1)
        idx_89 = next((i for i, l in enumerate(lines) if "!89" in l), -1)
        ok = idx_312 >= 0 and idx_89 >= 0 and idx_312 != idx_89
        return ok, "" if ok else "refs on same line or missing"

    if aid == "5.5":
        ok = "#89" not in c
        return ok, "" if ok else "contains #89 (should be !89)"

    # ---- Eval 6 ----
    if aid == "6.1":
        ok = bool(re.match(r"^[a-z]+\([^)]+\)", fl))
        return ok, "" if ok else f"no scope: {fl[:50]}"

    if aid == "6.2":
        scope = _scope(fl)
        valid = {"api", "cli", "docs", "config", "auth", "db"}
        ok = scope in valid
        return ok, "" if ok else f"invalid scope: '{scope}'"

    if aid == "6.3":
        scope = _scope(fl)
        ok = scope in {"docs", "config"}
        return ok, "" if ok else f"scope: '{scope}'"

    if aid == "6.4":
        ok = fl.lower().startswith("docs")
        return ok, "" if ok else f"type: {fl[:20]}"

    if aid == "6.5":
        ok = any(w in r.lower() for w in ["mandatory", "required", "must", "ci", "rejected", "enforce"])
        return ok, "" if ok else "no mandate/CI mention"

    # ---- Eval 7 ----
    if aid == "7.1":
        ok = fl.lower().startswith("fix")
        return ok, "" if ok else f"type: {fl[:20]}"

    if aid == "7.2":
        scope = _scope(fl)
        ok = scope in {"deps", "security", "deps/security"}
        return ok, "" if ok else f"scope: '{scope}'"

    if aid == "7.3":
        ok = any(w in r.lower() for w in ["high", "cvss", "vulnerability", "vulnerab", "security"])
        return ok, "" if ok else "no severity mention"

    if aid == "7.4":
        ok = not fl.lower().startswith("chore")
        return ok, "" if ok else "type is chore"

    if aid == "7.5":
        ok = "5.7.1" in c and "5.7.2" in c
        return ok, "" if ok else "missing version numbers"

    # ---- Eval 8 ----
    if aid == "8.1":
        ok = fl.lower().startswith("revert")
        return ok, "" if ok else f"type: {fl[:20]}"

    if aid == "8.2":
        ok = "abc123def456789" in c or "abc123" in c
        return ok, "" if ok else "no commit hash"

    if aid == "8.3":
        ok = any(re.match(r"Reverts\s+", line.strip()) for line in c.splitlines())
        return ok, "" if ok else "no formal 'Reverts ...' footer line"

    if aid == "8.4":
        ok = "oauth2" in r.lower() or "pkce" in r.lower()
        return ok, "" if ok else "no OAuth2/PKCE reference"

    if aid == "8.5":
        ok = any(w in r.lower() for w in ["provider", "endpoint", "changed", "broken", "incompatible", "no longer"])
        return ok, "" if ok else "no reason in body"

    # ---- Eval 9 (LLM-as-judge for 9.1, 9.2) ----
    if aid == "9.1":
        if api_key and judge_model:
            return llm_judge(api_key, judge_model, text, r)
        patterns = ["no contributing", "not found", "contributing.md not", "couldn't find",
                    "could not find", "absent", "no contributing.md", "without contributing"]
        ok = any(p in r.lower() for p in patterns)
        return ok, "" if ok else "no absence acknowledgment (regex fallback)"

    if aid == "9.2":
        if api_key and judge_model:
            return llm_judge(api_key, judge_model, text, r)
        patterns = ["conventional commits specification", "conventionalcommits",
                    "standard cc spec", "cc spec", "standard spec",
                    "conventional commits spec", "conventional commit spec"]
        ok = any(p in r.lower() for p in patterns)
        return ok, "" if ok else "no spec reference (regex fallback)"

    if aid == "9.3":
        ok = fl.lower().startswith("feat")
        return ok, "" if ok else f"type: {fl[:20]}"

    if aid == "9.4":
        ok = any(s in fl for s in ["(cli)", "(cmd)", "(cmd/root)"])
        return ok, "" if ok else f"scope: {_scope(fl) or 'none'}"

    if aid == "9.5":
        desc = _desc(fl)
        first_word = desc.split()[0].lower() if desc.split() else ""
        ok = first_word in {"add", "implement", "introduce", "create", "enable", "support", "expose"}
        return ok, "" if ok else f"not imperative: '{first_word}'"

    # ---- Eval 10 (LLM-as-judge for 10.1, 10.2) ----
    if aid == "10.1":
        if api_key and judge_model:
            return llm_judge(api_key, judge_model, text, r)
        ok = any(p in r.lower() for p in ["split", "separate", "two commit", "2 commit",
                                            "separate commit", "individual commit"])
        return ok, "" if ok else "no split recommendation (regex fallback)"

    if aid == "10.2":
        if api_key and judge_model:
            return llm_judge(api_key, judge_model, text, r)
        has_feat = "csv" in r.lower() or "export" in r.lower()
        has_bump = "version" in r.lower() or "bump" in r.lower() or "1.3.0" in r
        ok = has_feat and has_bump
        return ok, "" if ok else "missing one or both concerns (regex fallback)"

    if aid == "10.3":
        ok = bool(re.search(r"feat(\(export\))?:", r))  # check full response (split proposals may be outside code block)
        return ok, "" if ok else "no feat:/feat(export): for CSV export"

    if aid == "10.4":
        ok = bool(re.search(r"chore(\(release\))?:", r))
        return ok, "" if ok else "no chore(release): for version bump"

    if aid == "10.5":
        ok = "1.2.3" in r and "1.3.0" in r
        return ok, "" if ok else "missing 1.2.3 or 1.3.0"

    return False, f"unhandled assertion {aid}"


# ---------------------------------------------------------------------------
# Run one eval case
# ---------------------------------------------------------------------------

def run_eval(
    eval_case: dict,
    skill_body: str,
    mode: str,
    api_key: str,
    model: str,
    judge_model: str,
    verbose: bool,
) -> dict:
    prompt = build_prompt(eval_case, skill_body, mode)

    print(f"  [{mode:7s}] eval {eval_case['id']:2d} · {eval_case['name']}", end="", flush=True)
    start = time.monotonic()
    try:
        response = call_model(api_key, model, prompt)
    except Exception as e:
        print(f"  ERROR: {e}")
        return {
            "eval_id": eval_case["id"],
            "name": eval_case["name"],
            "mode": mode,
            "response": "",
            "results": [],
            "passed": 0,
            "total": len(eval_case["assertions"]),
            "error": str(e),
        }
    elapsed = time.monotonic() - start
    print(f"  ({elapsed:.1f}s)", flush=True)

    if verbose:
        print(f"\n--- response ---\n{response}\n--- end ---\n")

    results = []
    for assertion in eval_case["assertions"]:
        passed, note = grade_assertion(
            assertion, response,
            api_key=api_key if judge_model else "",
            judge_model=judge_model,
        )
        results.append({
            "id": assertion["id"],
            "text": assertion["text"],
            "passed": passed,
            "note": note,
        })

    passed_count = sum(1 for r in results if r["passed"])
    return {
        "eval_id": eval_case["id"],
        "name": eval_case["name"],
        "mode": mode,
        "response": response,
        "results": results,
        "passed": passed_count,
        "total": len(results),
        "elapsed_s": round(elapsed, 2),
    }


# ---------------------------------------------------------------------------
# Output formatting
# ---------------------------------------------------------------------------

PASS = "\033[32m✓\033[0m"
FAIL = "\033[31m✗\033[0m"


def print_summary(all_runs: list[dict], model: str, modes: list[str]) -> None:
    print(f"\n{'='*70}")
    print(f"Model: {model}")
    print(f"{'='*70}\n")

    # Group by mode
    by_mode: dict[str, list[dict]] = {}
    for run in all_runs:
        by_mode.setdefault(run["mode"], []).append(run)

    if "with" in by_mode and "without" in by_mode:
        # Side-by-side table
        with_runs = {r["eval_id"]: r for r in by_mode["with"]}
        without_runs = {r["eval_id"]: r for r in by_mode["without"]}
        all_ids = sorted(set(with_runs) | set(without_runs))

        header = f"{'Eval':<40} {'WITH':>6} {'WITHOUT':>9} {'Δ':>5}"
        print(header)
        print("-" * len(header))
        total_with = total_without = total_assertions = 0
        for eid in all_ids:
            w = with_runs.get(eid, {})
            wo = without_runs.get(eid, {})
            name = w.get("name") or wo.get("name") or str(eid)
            wp = w.get("passed", 0)
            wt = w.get("total", 0)
            wop = wo.get("passed", 0)
            wot = wo.get("total", 0)
            delta = wp - wop
            delta_str = f"+{delta}" if delta > 0 else str(delta)
            print(f"  {eid:2d}. {name[:35]:<35} {wp}/{wt}   {wop}/{wot}   {delta_str:>3}")
            total_with += wp
            total_without += wop
            total_assertions += wt
        print("-" * len(header))
        pct_w = 100 * total_with / total_assertions if total_assertions else 0
        pct_wo = 100 * total_without / total_assertions if total_assertions else 0
        delta_pp = pct_w - pct_wo
        uplift = (pct_w / pct_wo) if pct_wo else float("inf")
        print(f"  {'TOTAL':<38} {total_with}/{total_assertions}  {total_without}/{total_assertions}  {delta_pp:+.0f}pp")
        print(f"\n  WITH:    {total_with}/{total_assertions} ({pct_w:.0f}%)")
        print(f"  WITHOUT: {total_without}/{total_assertions} ({pct_wo:.0f}%)")
        print(f"  Delta:   {delta_pp:+.0f}pp  ({uplift:.2f}×)")

    else:
        # Single mode
        mode = modes[0]
        runs = by_mode.get(mode, [])
        total_passed = sum(r["passed"] for r in runs)
        total_total = sum(r["total"] for r in runs)
        print(f"Mode: {mode}")
        for run in runs:
            icon = PASS if run["passed"] == run["total"] else FAIL
            print(f"  {run['eval_id']:2d}. {run['name'][:45]:<45} {run['passed']}/{run['total']}")
            if run["passed"] < run["total"]:
                for res in run["results"]:
                    if not res["passed"]:
                        print(f"       {FAIL} {res['id']}: {res['note'] or res['text'][:60]}")
        pct = 100 * total_passed / total_total if total_total else 0
        print(f"\n  TOTAL: {total_passed}/{total_total} ({pct:.0f}%)")

    print()


def print_assertion_detail(all_runs: list[dict]) -> None:
    """Print per-assertion pass/fail for each run."""
    for run in all_runs:
        if run.get("error"):
            continue
        print(f"\n  Eval {run['eval_id']} [{run['mode']}] · {run['name']} — {run['passed']}/{run['total']}")
        for res in run["results"]:
            icon = PASS if res["passed"] else FAIL
            note = f"  ({res['note']})" if res["note"] else ""
            print(f"    {icon} {res['id']}: {res['text'][:65]}{note}")


def to_evaluations_md_row(model: str, skill_name: str, version: str, all_runs: list[dict]) -> str:
    """Generate a markdown table row suitable for EVALUATIONS.md."""
    by_mode = {}
    for run in all_runs:
        by_mode.setdefault(run["mode"], []).append(run)

    if "with" in by_mode and "without" in by_mode:
        total_assertions = sum(r["total"] for r in by_mode["with"])
        pct_w = 100 * sum(r["passed"] for r in by_mode["with"]) / total_assertions
        pct_wo = 100 * sum(r["passed"] for r in by_mode["without"]) / total_assertions
        delta = pct_w - pct_wo
        uplift = pct_w / pct_wo if pct_wo else float("inf")
        return (
            f"| `{skill_name}` | {model} | {version} | {total_assertions} "
            f"| {pct_w:.0f}% | {pct_wo:.0f}% | {delta:+.0f}pp | {uplift:.2f}× |"
        )
    elif "with" in by_mode:
        total = sum(r["total"] for r in by_mode["with"])
        pct = 100 * sum(r["passed"] for r in by_mode["with"]) / total
        return f"| `{skill_name}` | {model} | {version} | {total} | {pct:.0f}% | — | — | — |"
    else:
        total = sum(r["total"] for r in by_mode.get("without", []))
        pct = 100 * sum(r["passed"] for r in by_mode.get("without", [])) / total
        return f"| `{skill_name}` | {model} | {version} | {total} | — | {pct:.0f}% | — | — |"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Benchmark a skill against OpenRouter models.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("--skill", default="skills/git-conventional-commits",
                   help="Path to skill directory (default: skills/git-conventional-commits)")
    p.add_argument("--model", required=True,
                   help="OpenRouter model ID, e.g. nvidia/nemotron-3-nano-30b-a3b:free")
    p.add_argument("--mode", choices=["with", "without", "both"], default="both",
                   help="Run with-skill, without-skill, or both (default: both)")
    p.add_argument("--judge-model", default="",
                   help="Model for LLM-as-judge assertions (9.1, 9.2, 10.1, 10.2). "
                        "Falls back to regex heuristics if omitted.")
    p.add_argument("--api-key", default="",
                   help="OpenRouter API key (overrides env/OPENROUTER_API_KEY)")
    p.add_argument("--evals", default="",
                   help="Comma-separated eval IDs to run, e.g. 1,3,9 (default: all)")
    p.add_argument("--output", default="",
                   help="Save full results JSON to this path")
    p.add_argument("--detail", action="store_true",
                   help="Print per-assertion pass/fail detail")
    p.add_argument("--verbose", action="store_true",
                   help="Print full model responses")
    p.add_argument("--skill-version", default="v1.0.0",
                   help="Skill version string for EVALUATIONS.md row (default: v1.0.0)")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    api_key = get_api_key(args.api_key)

    skill_dir = Path(args.skill)
    if not skill_dir.exists():
        sys.exit(f"ERROR: skill directory not found: {skill_dir}")

    skill_body = load_skill_body(skill_dir)
    evals = load_evals(skill_dir)
    skill_name = skill_dir.name

    # Filter evals if requested
    if args.evals:
        wanted = {int(x.strip()) for x in args.evals.split(",")}
        evals = [e for e in evals if e["id"] in wanted]
        if not evals:
            sys.exit(f"ERROR: no evals match IDs {args.evals}")

    modes = ["with", "without"] if args.mode == "both" else [args.mode]

    print(f"\nBenchmarking: {skill_name}")
    print(f"Model:        {args.model}")
    print(f"Mode:         {args.mode}")
    if args.judge_model:
        print(f"Judge model:  {args.judge_model}")
    print(f"Evals:        {len(evals)} cases × {len(modes)} mode(s)\n")

    all_runs: list[dict] = []

    for mode in modes:
        print(f"Running [{mode}] …")
        for eval_case in evals:
            run = run_eval(
                eval_case=eval_case,
                skill_body=skill_body,
                mode=mode,
                api_key=api_key,
                model=args.model,
                judge_model=args.judge_model,
                verbose=args.verbose,
            )
            all_runs.append(run)

    print_summary(all_runs, args.model, modes)

    if args.detail:
        print_assertion_detail(all_runs)

    # EVALUATIONS.md row
    print("\nEVALUATIONS.md row:")
    print(to_evaluations_md_row(args.model, skill_name, args.skill_version, all_runs))

    if args.output:
        out = {
            "model": args.model,
            "skill": skill_name,
            "skill_version": args.skill_version,
            "judge_model": args.judge_model,
            "mode": args.mode,
            "runs": all_runs,
        }
        Path(args.output).write_text(json.dumps(out, indent=2))
        print(f"\nResults saved to {args.output}")


if __name__ == "__main__":
    main()
