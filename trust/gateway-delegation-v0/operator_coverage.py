#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""operator_coverage.py — 把"12 个声明算子类里 5 个 sites 0"这件事说清楚。

mutation_report 只说"这一类在判定区没有位点"。读者无法分辨两种情况：
  (a) 这一类在被测代码里**不存在**（例如代码里根本没有 `<=`），所以没有位点；
  (b) 这一类**存在**，但扫描器漏了它 —— 那才是真洞。

本脚本逐类判定：
  COVERED  位点 >= 1 且该类的变异体全部被杀
  ABSENT   两个实现的相关代码区间里都搜不到这种构造（并给出 0 次计数为证）
  GAP      构造在，但没有位点，或有存活体 —— 退出码 1，不许写成"已覆盖"

用法：python3 operator_coverage.py            # 打印表
      python3 operator_coverage.py --json operator-coverage.json
"""
import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

# 每类：(名字, Python 区间内正则, JavaScript 区间内正则, 人话说明)
CLASSES = [
    ("eq-flip", r"[^=!<>]==", r"===", "等于改不等"),
    ("ne-flip", r"!=", r"!==", "不等改等于"),
    ("ge-to-gt", r">=", r">=", ">= 改 >"),
    ("gt-to-ge", r"(?<![=<>])>(?!=)", r"(?<![=<>])>(?!=)", "> 改 >="),
    ("le-to-lt", r"<=", r"<=", "<= 改 <"),
    ("lt-to-le", r"(?<![=<>])<(?![=])", r"(?<![=<>])<(?![=])", "< 改 <="),
    ("and-to-or", r"\band\b", r"&&", "and 改 or"),
    ("or-to-and", r"\bor\b", r"\|\|", "or 改 and"),
    ("true-to-false", r"\bTrue\b", r"\btrue\b", "真改假"),
    ("false-to-true", r"\bFalse\b", r"\bfalse\b", "假改真"),
    ("pass-to-fail", r'"pass"', r'"pass"', "pass 改 fail"),
    ("fail-to-pass", r'"fail"', r'"fail"', "fail 改 pass"),
]

SKIP = ("def selftest", "def main(", "import ", "from ", "print(", "argparse", "parser.",
        "#", '"""', "def load_", "def parse_time", "def print_table")


def py_region(lines):
    start = next((i for i, ln in enumerate(lines) if ln.startswith("def check_case")), None)
    end = next((i for i, ln in enumerate(lines) if ln.startswith("def selftest")), None)
    if start is None or end is None:
        raise SystemExit("check.py: check_case .. selftest not found — harness out of date")
    return start, end


def js_region(lines):
    start = next((i for i, ln in enumerate(lines) if re.match(r"function\s+checkCase|const\s+checkCase|checkCase\s*=", ln)), None)
    if start is None:
        raise SystemExit("check.mjs: checkCase not found — harness out of date")
    end = next((i for i in range(start + 1, len(lines)) if re.match(r"function\s+|const\s+\w+\s*=", lines[i])), len(lines))
    return start, end


def scan(path, start, end, pattern, skip_markers=True):
    lines = open(os.path.join(HERE, path), encoding="utf-8").read().splitlines()
    hits = []
    for idx in range(start, end):
        line = lines[idx]
        if skip_markers and any(m in line for m in SKIP):
            continue
        for _ in re.finditer(pattern, line):
            hits.append({"file": path, "line_no": idx + 1, "text": line.strip()[:100]})
    return hits


def main():
    ap = argparse.ArgumentParser(description="Classify operator coverage: covered / absent-by-construction / gap")
    ap.add_argument("--json", default="operator-coverage.json")
    args = ap.parse_args()

    py_lines = open(os.path.join(HERE, "check.py"), encoding="utf-8").read().splitlines()
    js_lines = open(os.path.join(HERE, "check.mjs"), encoding="utf-8").read().splitlines()
    py_s, py_e = py_region(py_lines)
    js_s, js_e = js_region(js_lines)

    rep = json.load(open(os.path.join(HERE, "mutation-report.json"), encoding="utf-8"))
    declared = rep["by_operator_declared"]
    cross = json.load(open(os.path.join(HERE, "mutation-cross-report.json"), encoding="utf-8"))
    cross_killed_ops = {r["op"] for r in cross["results"] if r.get("state") == "KILLED"}

    rows, gaps = [], []
    for name, py_pat, js_pat, human in CLASSES:
        sites = declared[name]["sites_in_decision_code"]
        mutants = declared[name]["mutants"]
        killed = declared[name]["killed"]
        py_hits = scan("check.py", py_s, py_e, py_pat)
        js_hits = scan("check.mjs", js_s, js_e, js_pat)
        if sites >= 1 and killed == mutants:
            status = "COVERED"
        elif sites == 0 and mutants == 0 and not py_hits and not js_hits:
            status = "ABSENT"
        else:
            status = "GAP"
        row = {"class": name, "what": human, "sites": sites, "mutants": mutants, "killed": killed,
               "occurrences_check_py": len(py_hits), "occurrences_check_mjs": len(js_hits),
               "where_py": [h["line_no"] for h in py_hits][:5],
               "where_js": [h["line_no"] for h in js_hits][:5],
               "cross_impl_killed": name in cross_killed_ops,
               "status": status}
        rows.append(row)
        if status == "GAP":
            gaps.append(row)

    covered = [r for r in rows if r["status"] == "COVERED"]
    absent = [r for r in rows if r["status"] == "ABSENT"]
    print("%-15s %6s %8s %6s %6s %6s  %s" % ("class", "sites", "mutants", "killed", "py#", "js#", "status"))
    for r in rows:
        print("%-15s %6d %8d %6d %6d %6d  %s" % (r["class"], r["sites"], r["mutants"], r["killed"],
                                                 r["occurrences_check_py"], r["occurrences_check_mjs"], r["status"]))
    print("\ndeclared %d | covered %d | absent by construction %d | gap %d" % (
        len(rows), len(covered), len(absent), len(gaps)))
    if absent:
        print("absent (0 occurrences in both implementations' decision code; not a coverage hole):")
        for r in absent:
            print("  %-15s %s" % (r["class"], r["what"]))

    out = {
        "schema": "aikr-operator-coverage/0",
        "subject": "gateway-delegation-v0",
        "inputs": {"mutation_report": "mutation-report.json", "mutation_cross_report": "mutation-cross-report.json"},
        "scanned_regions": {"check.py": [py_s + 1, py_e], "check.mjs": [js_s + 1, js_e]},
        "declared": len(rows),
        "covered": len(covered),
        "absent": len(absent),
        "gap": len(gaps),
        "classes": rows,
        "note": "ABSENT means the construct does not occur in the decision code of either implementation; "
                "it is proven here by a zero occurrence count, not excused by a comment. Any class that "
                "occurs but has no site, or has a surviving mutant, is a GAP and exits 1.",
    }
    with open(os.path.join(HERE, args.json), "w", encoding="utf-8", newline="\n") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    print("report -> %s" % args.json)
    if gaps:
        print("GAP — these classes occur in the code but are not measured:")
        for r in gaps:
            print("  %-15s sites %d mutants %d survivors %d" % (r["class"], r["sites"], r["mutants"], r["mutants"] - r["killed"]))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
