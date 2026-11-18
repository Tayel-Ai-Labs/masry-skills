"""Run the masry-writing eval: each prompt with and without the skill.

Usage:
    python3 skills/masry-writing/evals/run.py              # all evals
    python3 skills/masry-writing/evals/run.py --ids 1 3    # some evals

Needs the Claude Code CLI (`claude`) logged in. Standard library only.

For every eval it:
  1. generates a baseline answer (plain system prompt) and a skill answer
     (SKILL.md + references/tells.md as system prompt), same model;
  2. counts register slips and tells with regexes (deterministic);
  3. asks a grader model to judge both answers blind against the
     expectations (answers are shuffled and labelled A/B).

Results go to evals/results/<timestamp>.json and a summary is printed.
"""

import argparse
import concurrent.futures
import datetime
import json
import random
import re
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL_DIR = HERE.parent
GEN_MODEL = "sonnet"
GRADER_MODEL = "opus"
BASELINE_SYSTEM = "You are a helpful assistant."

# Words that should not appear in Egyptian-register text. Optional clitic
# prefix (و ف ب ل) allowed; must stand as a whole word.
MSA_MARKERS = [
    "هذا", "هذه", "هؤلاء", "الذي", "التي", "الذين", "سوف", "لم", "لن", "ليس",
    "لديك", "لدينا", "لديه", "ماذا", "لماذا", "كيف", "أين", "متى", "أيضاً", "أيضا",
]
# Words that should not appear in formal MSA text.
EGYPTIAN_MARKERS = [
    "ده", "دي", "دول", "مش", "عايز", "عايزين", "إزاي", "ازاي", "بتاع", "بتاعة",
    "اللي", "كده", "دلوقتي", "علشان", "عشان", "إيه", "ليه", "فين",
]
TELL_PHRASES = [
    "في عالمنا", "عالمنا المتسارع", "في ظل التطور", "يلعب دور", "تلعب دور",
    "دوراً محورياً", "دورا محوريا", "دوراً مهماً", "على صعيد", "في هذا السياق",
    "في هذا الصدد", "تجدر الإشارة", "لا شك أن", "مما لا شك فيه",
    "بالإضافة إلى ذلك", "علاوة على ذلك", "حيث إن", "يُعد من أهم", "يعد من أهم",
    "تجربة فريدة", "لا مثيل لها", "الأفضل على الإطلاق", "نسعى جاهدين",
    "في الختام", "ختاماً", "لا تتردد", "نتمنى لكم", "قم ب",
]


def word_re(words):
    alts = "|".join(re.escape(w) for w in words)
    return re.compile(r"(?<![\w])(?:[وفبل])?(?:%s)(?![\w])" % alts)


MSA_RE = word_re(MSA_MARKERS)
EGY_RE = word_re(EGYPTIAN_MARKERS)
DASH_RE = re.compile("[–—]")


def skill_system_prompt():
    skill = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    tells = (SKILL_DIR / "references" / "tells.md").read_text(encoding="utf-8")
    return skill + "\n\n---\n\n# references/tells.md\n\n" + tells


# Run every call from an empty directory. From inside the project, the CLI
# auto-loads CLAUDE.md files from parent folders (e.g. ~/Desktop/CLAUDE.md),
# which leaked real project names into the answers of the first run.
ISOLATED_CWD = tempfile.mkdtemp(prefix="masry-eval-")


def claude(prompt, system, model):
    cmd = [
        "claude", "-p", "--model", model, "--no-session-persistence",
        "--tools", "", "--system-prompt", system, prompt,
    ]
    out = subprocess.run(cmd, capture_output=True, text=True, timeout=600, cwd=ISOLATED_CWD)
    if out.returncode != 0:
        raise RuntimeError("claude failed: " + (out.stderr or out.stdout)[:300])
    return out.stdout.strip()


def deliverable(text):
    """The part meant to be pasted: everything before a line that is just ---.

    Notes to the user come after that line and are written to the user, often
    in Egyptian, so counting them would flag slips the deliverable doesn't have.
    """
    return re.split(r"\n\s*---\s*\n", text, maxsplit=1)[0]


def deterministic(text, register):
    text = deliverable(text)
    found_tells = [t for t in TELL_PHRASES if t in text]
    if register == "egyptian":
        slips = MSA_RE.findall(text)
    else:
        slips = EGY_RE.findall(text)
    return {
        "register_slips": len(slips),
        "slip_words": sorted(set(slips)),
        "tells": len(found_tells),
        "tell_phrases": found_tells,
        "dashes": len(DASH_RE.findall(text)),
    }


GRADER_PROMPT = """You are a native Egyptian Arabic editor grading two answers
to the same request. Judge each answer against each expectation strictly.

Request:
<request>
{prompt}
</request>

Expectations (id: description):
{expectations}

<answer id="A">
{a}
</answer>

<answer id="B">
{b}
</answer>

Return only JSON, no prose, in exactly this shape:
{{"A": {{"<expectation id>": {{"pass": true, "why": "<short reason>"}}, ...}},
  "B": {{...}},
  "more_natural": "A" | "B" | "tie"}}
"""


def grade(ev, baseline, skilled):
    order = [("baseline", baseline), ("skill", skilled)]
    random.shuffle(order)
    labels = {"A": order[0][0], "B": order[1][0]}
    exp = "\n".join("- " + e for e in ev["expectations"])
    raw = claude(
        GRADER_PROMPT.format(prompt=ev["prompt"], expectations=exp, a=order[0][1], b=order[1][1]),
        "You grade writing. Output JSON only.",
        GRADER_MODEL,
    )
    m = re.search(r"\{.*\}", raw, re.S)
    data = json.loads(m.group(0))
    result = {labels["A"]: data["A"], labels["B"]: data["B"]}
    nat = data.get("more_natural", "tie")
    result["more_natural"] = labels.get(nat, "tie")
    return result


def run_one(ev, skill_sys):
    baseline = claude(ev["prompt"], BASELINE_SYSTEM, GEN_MODEL)
    skilled = claude(ev["prompt"], skill_sys, GEN_MODEL)
    graded = grade(ev, baseline, skilled)
    return {
        "id": ev["id"],
        "prompt": ev["prompt"],
        "register": ev["register"],
        "baseline": {"text": baseline, "checks": deterministic(baseline, ev["register"]), "grades": graded["baseline"]},
        "skill": {"text": skilled, "checks": deterministic(skilled, ev["register"]), "grades": graded["skill"]},
        "more_natural": graded["more_natural"],
    }


def summarize(results):
    def tally(arm):
        passed = total = slips = tells = dashes = 0
        for r in results:
            for g in r[arm]["grades"].values():
                total += 1
                passed += bool(g.get("pass"))
            c = r[arm]["checks"]
            slips += c["register_slips"]
            tells += c["tells"]
            dashes += c["dashes"]
        return passed, total, slips, tells, dashes

    lines = ["", "%-9s %-14s %-14s %-6s %-7s" % ("arm", "expectations", "register slips", "tells", "dashes")]
    for arm in ("baseline", "skill"):
        p, t, s, tl, d = tally(arm)
        lines.append("%-9s %3d/%-10d %-14d %-6d %-7d" % (arm, p, t, s, tl, d))
    wins = {k: sum(r["more_natural"] == k for r in results) for k in ("skill", "baseline", "tie")}
    lines.append("")
    lines.append("grader picked as more natural: skill %(skill)d, baseline %(baseline)d, tie %(tie)d" % wins)
    lines.append("")
    for r in results:
        failed = [k for k, g in r["skill"]["grades"].items() if not g.get("pass")]
        lines.append("eval %2d  skill fails: %s" % (r["id"], ", ".join(failed) or "-"))
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ids", type=int, nargs="*")
    ap.add_argument("--workers", type=int, default=4)
    args = ap.parse_args()

    evals = json.loads((HERE / "evals.json").read_text(encoding="utf-8"))["evals"]
    if args.ids:
        evals = [e for e in evals if e["id"] in args.ids]
    skill_sys = skill_system_prompt()

    results = []
    with concurrent.futures.ThreadPoolExecutor(args.workers) as pool:
        futures = {pool.submit(run_one, e, skill_sys): e["id"] for e in evals}
        for f in concurrent.futures.as_completed(futures):
            try:
                results.append(f.result())
                print("eval %d done" % futures[f], file=sys.stderr)
            except Exception as exc:  # keep the other evals running
                print("eval %d FAILED: %s" % (futures[f], exc), file=sys.stderr)
    results.sort(key=lambda r: r["id"])

    out_dir = HERE / "results"
    out_dir.mkdir(exist_ok=True)
    stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    path = out_dir / ("%s.json" % stamp)
    path.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")

    print(summarize(results))
    print("\nsaved:", path)
    if len(results) < len(evals):
        sys.exit(1)


if __name__ == "__main__":
    main()
