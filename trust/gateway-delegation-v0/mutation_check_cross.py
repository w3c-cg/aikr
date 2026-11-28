#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""mutation_check_cross.py — 跨实现变异：把缺陷注入 JS 实现，看 Python 侧能不能发现。

单实现变异（mutation_check.py）问的是"我方语料能不能抓错我方的检查器"。
这一支问的是另一个问题：**两个实现之间能不能互相看住**。做法是把
`check.mjs` 的判定区（checkCase）逐个注入缺陷，跑 `crosscheck.py`：

  - crosscheck 报出 disagreements > 0  => 该缺陷被另一个实现抓住（KILLED）
  - JS 变异体语法就坏               => 不计分（INVALID）
  - 其它非零退出                     => 记为 ERROR，单列，不并入分数

只读本目录，临时副本跑完即删；不联网。
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = "check.mjs"
REGION_START = "function checkCase("
REGION_END = "const policy = readJSON("

OPERATORS = [
    ("eqeq-flip", r"===", "!=="),
    ("neeq-flip", r"!==", "==="),
    ("eq-flip", r"(?<![=!])==(?!=)", "!="),
    ("ne-flip", r"!=(?!=)", "=="),
    ("and-to-or", r"&&", "||"),
    ("or-to-and", r"\|\|", "&&"),
    ("lt-to-le", r"(?<![<>])<(?!=)", "<="),
    ("le-to-lt", r"<=", "<"),
    ("gt-to-ge", r"(?<![<>])>(?!=)", ">="),
    ("ge-to-gt", r">=", ">"),
    ("true-to-false", r"\btrue\b", "false"),
    ("false-to-true", r"\bfalse\b", "true"),
]

SKIP_MARKERS = ("//", "/*", "*", '"""', "const PASS", "const FAIL", "const RECORD",
                "const ABSENT", "const CHECKER", "readJSON(", "listJSON(", "parseTime(")


def region(lines):
    start = next(i for i, ln in enumerate(lines) if ln.startswith(REGION_START))
    end = next(i for i, ln in enumerate(lines) if ln.startswith(REGION_END))
    return start, end


def candidates(lines, start, end):
    out = []
    for idx in range(start, end):
        stripped = lines[idx].strip()
        if not stripped or any(m in stripped for m in SKIP_MARKERS):
            continue
        if stripped.startswith("function ") or stripped.startswith("return"):
            # a return line still carries a comparison; keep it, but drop the
            # bare "return X;" shape that has no operator to flip
            if not any(re.search(p, stripped) for _n, p, _r in OPERATORS):
                continue
        for name, pattern, repl in OPERATORS:
            if re.search(pattern, stripped):
                out.append({"op": name, "line_no": idx + 1, "pattern": pattern,
                            "repl": repl, "line": stripped[:110]})
    return out


def run_one(mut, src_lines, root):
    lines = list(src_lines)
    idx = mut["line_no"] - 1
    new_line = re.sub(mut["pattern"], mut["repl"], lines[idx], count=1)
    if new_line == lines[idx]:
        return {"state": "INVALID", "why": "regex did not change the line"}
    lines[idx] = new_line
    tmp = os.path.join(root, "m%03d" % mut.get("n", mut["line_no"]))
    shutil.copytree(HERE, tmp, ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc"))
    with open(os.path.join(tmp, TARGET), "w", encoding="utf-8", newline="\n") as handle:
        handle.write("".join(lines))

    node = subprocess.run(["node", TARGET], cwd=tmp, capture_output=True, text=True, timeout=120)
    if "SyntaxError" in node.stderr:
        return {"state": "INVALID", "why": "mutant does not parse"}

    cross = subprocess.run([sys.executable, "crosscheck.py"], cwd=tmp,
                           capture_output=True, text=True, timeout=180)
    out = cross.stdout + cross.stderr
    m = re.search(r"disagreements:\s*(\d+)", out)
    if m and int(m.group(1)) > 0:
        return {"state": "KILLED", "disagreements": int(m.group(1)), "rc": cross.returncode}
    if cross.returncode != 0:
        return {"state": "ERROR", "rc": cross.returncode, "last": out.strip().splitlines()[-1][:120]}
    return {"state": "SURVIVED", "rc": 0, "last": out.strip().splitlines()[-1][:120]}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", default="mutation-cross-report.json")
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()

    with open(os.path.join(HERE, TARGET), encoding="utf-8") as handle:
        source = handle.read()
    lines = source.splitlines(keepends=True)
    start, end = region(lines)
    cands = candidates(lines, start, end)
    print("candidates in %s checkCase region: %d" % (TARGET, len(cands)))

    results = []
    root = tempfile.mkdtemp(prefix="aikr-cross-mut-")
    try:
        for i, mut in enumerate(cands, 1):
            mut = dict(mut, n=i)
            res = run_one(mut, lines, root)
            res.update({"n": i, "op": mut["op"], "line_no": mut["line_no"], "line": mut["line"]})
            results.append(res)
            print("%-3d %-12s L%-4d %-9s %s" % (i, mut["op"], mut["line_no"], res["state"],
                                                mut["line"][:60]))
    finally:
        shutil.rmtree(root, ignore_errors=True)

    killed = [r for r in results if r["state"] == "KILLED"]
    survived = [r for r in results if r["state"] == "SURVIVED"]
    invalid = [r for r in results if r["state"] == "INVALID"]
    errors = [r for r in results if r["state"] == "ERROR"]
    scored = len(killed) + len(survived)
    rate = (100.0 * len(killed) / scored) if scored else 0.0

    print("\ncross-impl mutants: %d  killed: %d  survived: %d  invalid: %d  error: %d (score %.1f%%)" % (
        len(results), len(killed), len(survived), len(invalid), len(errors), rate))
    if survived:
        print("SURVIVED — JS drift the Python side did not notice:")
        for r in survived:
            print("  L%-4d %-12s %s" % (r["line_no"], r["op"], r["line"]))

    report = {
        "schema": "aikr-mutation-cross-report/0",
        "subject": "gateway-delegation-v0 cross-implementation mutation",
        "target": TARGET,
        "oracle": "crosscheck.py (python vs javascript verdict + hold group)",
        "candidates_found": len(cands),
        "mutants": len(results),
        "killed": len(killed),
        "survived": len(survived),
        "invalid": len(invalid),
        "error": len(errors),
        "score_percent": round(rate, 1),
        "method": "one defect per mutant inside checkCase; crosscheck disagreement counts as killed; "
                  "syntactically broken mutants excluded; other failures recorded as error, not scored",
        "limits": "operator-level only; does not mutate the corpus, the expectations or check.py",
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
