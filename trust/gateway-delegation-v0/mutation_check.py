#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""mutation_check.py — 度量这套评测能不能"抓错"，而不是只证明"我们对"。

做法（变异测试，25 个变异体）：
  在 check.py 的判定代码里逐处注入一个缺陷（翻比较符、翻真假、把 fail 写成
  pass、把 and 写成 or …），把整目录复制到临时目录，跑 `check.py --selftest`。
  期望值没有改动，所以：
    - selftest 报错 => 这个缺陷被语料抓住了（KILLED）
    - selftest 仍通过 => 语料漏了这个缺陷（SURVIVED，要补用例）
    - 变异后代码语法就坏 => 不计分（INVALID），否则分数会虚高

用法：
  python mutation_check.py                 # 跑 25 个变异体，打印并写 mutation-report.json
  python mutation_check.py --limit 25 --json mutation-report.json

只读本目录、不联网、不改动仓库里的任何文件；临时副本跑完即删。
"""
import argparse
import datetime
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = "check.py"

# (名字, 正则, 替换) —— 只在判定区生效，一行一处
OPERATORS = [
    ("eq-flip", r"==", "!="),
    ("ne-flip", r"!=", "=="),
    ("ge-to-gt", r">=", ">"),
    ("gt-to-ge", r"(?<![=<>])>(?!=)", ">="),
    ("le-to-lt", r"<=", "<"),
    ("lt-to-le", r"(?<![=<>])<(?![=])", "<="),
    ("and-to-or", r"\band\b", "or"),
    ("or-to-and", r"\bor\b", "and"),
    ("true-to-false", r"\bTrue\b", "False"),
    ("false-to-true", r"\bFalse\b", "True"),
    ("pass-to-fail", r'"pass"', '"fail"'),
    ("fail-to-pass", r'"fail"', '"pass"'),
]

SKIP_MARKERS = ("def selftest", "def main(", "import ", "from ", "print(", "argparse",
                "parser.", "#", '"""', "def load_", "def parse_time", "def print_table")


def read_source():
    with open(os.path.join(HERE, TARGET), encoding="utf-8") as handle:
        return handle.read()


def allowed_region(lines):
    """判定代码所在区间：从 check_case 起，到 selftest 之前。"""
    start = next((i for i, ln in enumerate(lines) if ln.startswith("def check_case")), None)
    end = next((i for i, ln in enumerate(lines) if ln.startswith("def selftest")), None)
    if start is None or end is None:
        raise SystemExit("check_case / selftest not found: the harness is out of date")
    return start, end


def candidates(lines, start, end):
    out = []
    for idx in range(start, end):
        line = lines[idx]
        stripped = line.strip()
        if not stripped or any(m in stripped for m in SKIP_MARKERS):
            continue
        for name, pattern, repl in OPERATORS:
            if re.search(pattern, line):
                out.append({"op": name, "line_no": idx + 1, "pattern": pattern,
                            "repl": repl, "line": stripped[:110]})
    return out


def pick(cands, limit):
    """All candidate sites by default (limit<=0); a positive limit keeps the
    old sampling (one per operator first, then by line number)."""
    if not limit or limit <= 0:
        return cands
    by_op = {}
    for c in cands:
        by_op.setdefault(c["op"], []).append(c)
    chosen = []
    for op, items in by_op.items():
        chosen.append(items[0])
    rest = [c for c in cands if c not in chosen]
    rest.sort(key=lambda c: c["line_no"])
    for c in rest:
        if len(chosen) >= limit:
            break
        chosen.append(c)
    return chosen[:limit]


def run_mutant(mut, src_lines, tmp):
    lines = list(src_lines)
    idx = mut["line_no"] - 1
    new_line = re.sub(mut["pattern"], mut["repl"], lines[idx], count=1)
    if new_line == lines[idx]:
        return {"state": "INVALID", "why": "regex did not change the line"}
    lines[idx] = new_line
    path = os.path.join(tmp, TARGET)
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write("".join(lines))
    proc = subprocess.run([sys.executable, TARGET, "--selftest"], cwd=tmp,
                          capture_output=True, text=True, timeout=300)
    tail = (proc.stdout + proc.stderr).strip().splitlines()
    tail = tail[-1] if tail else ""
    if "SyntaxError" in proc.stderr or "IndentationError" in proc.stderr:
        return {"state": "INVALID", "why": "mutant does not parse"}
    if proc.returncode != 0:
        return {"state": "KILLED", "rc": proc.returncode, "last": tail}
    return {"state": "SURVIVED", "rc": 0, "last": tail}


def main():
    parser = argparse.ArgumentParser(description="Mutation-test the checker against its own corpus")
    parser.add_argument("--limit", type=int, default=0,
                        help="0 (default) = every candidate site; a positive number samples that many")
    parser.add_argument("--json", default="mutation-report.json")
    parser.add_argument("--strict", action="store_true",
                        help="exit 1 when a mutant survives; default is 0 because this is a measurement, not a gate")
    args = parser.parse_args()

    source = read_source()
    lines = source.splitlines(keepends=True)
    start, end = allowed_region(lines)
    all_cands = candidates(lines, start, end)
    picked = pick(all_cands, args.limit)

    results = []
    workroot = tempfile.mkdtemp(prefix="aikr-mut-")
    try:
        for i, mut in enumerate(picked, 1):
            tmp = os.path.join(workroot, "m%02d" % i)
            shutil.copytree(HERE, tmp, ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc"))
            res = run_mutant(mut, lines, tmp)
            res.update({"n": i, "op": mut["op"], "line_no": mut["line_no"], "line": mut["line"]})
            results.append(res)
            print("%-3d %-13s L%-4d %-10s %s" % (i, mut["op"], mut["line_no"], res["state"], mut["line"][:64]))
    finally:
        shutil.rmtree(workroot, ignore_errors=True)

    killed = [r for r in results if r["state"] == "KILLED"]
    survived = [r for r in results if r["state"] == "SURVIVED"]
    invalid = [r for r in results if r["state"] == "INVALID"]
    scored = len(killed) + len(survived)
    rate = (100.0 * len(killed) / scored) if scored else 0.0

    print("\nmutants: %d  killed: %d  survived: %d  invalid: %d  (score %.1f%% of %d scored)" % (
        len(results), len(killed), len(survived), len(invalid), rate, scored))
    if survived:
        print("SURVIVED — these are the gaps the corpus does not catch:")
        for r in survived:
            print("  L%-4d %-13s %s" % (r["line_no"], r["op"], r["line"]))

    report = {
        "schema": "aikr-mutation-report/0",
        "subject": "gateway-delegation-v0",
        "target": TARGET,
        "generated_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "checker_sha256": hashlib.sha256(source.encode("utf-8")).hexdigest(),
        "python": sys.version.split()[0],
        "candidates_found": len(all_cands),
        "mutants": len(results),
        "killed": len(killed),
        "survived": len(survived),
        "invalid": len(invalid),
        "score_percent": round(rate, 1),
        "by_operator": {
            op: {"mutants": len(items),
                 "killed": sum(1 for r in items if r["state"] == "KILLED")}
            for op, items in sorted(
                {op: [r for r in results if r["op"] == op] for op in {r["op"] for r in results}}.items())
        },
        "method": "one defect per mutant in the decision code only; expected values untouched; "
                  "selftest must fail for the mutant to count as killed; syntactically broken mutants excluded",
        "limits": "operator-level mutations inside check.py only; no scenario-level, "
                  "cross-implementation or fixture mutations are attempted here",
        "results": results,
    }
    with open(os.path.join(HERE, args.json), "w", encoding="utf-8", newline="\n") as handle:
        json.dump(report, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    print("report -> %s" % args.json)
    if survived and args.strict:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
