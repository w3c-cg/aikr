#!/usr/bin/env python3
"""Run both implementations over the curated cases and the vector set, and
compare the outcomes row by row. Exit 1 on any disagreement.

    python3 crosscheck.py                 # human-readable
    python3 crosscheck.py --json parity-report.json

The Python side runs in-process; the JavaScript side is `check.mjs`, run with
`node`. If node is absent the script says so and exits 2 rather than pretending
the cross-check passed.

`--json` writes a machine-readable parity report: one row per case, both
implementations' result and code, whether they agree, and the sha256 of the
inputs (both checkers, the policy, the expected file). The report compares our
two checkers; it says nothing about any third-party implementation.
"""
import argparse
import datetime
import hashlib
import json
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import check as py  # noqa: E402

SCHEMA = "aikr-parity-report/0"


def sha256_of(path):
    with open(path, "rb") as handle:
        return hashlib.sha256(handle.read()).hexdigest()


def inputs_block():
    files = ["check.py", "check.mjs", "policy.json", "expected.json"]
    block = {}
    for name in files:
        path = os.path.join(HERE, name)
        block[name] = sha256_of(path) if os.path.exists(path) else ""
    try:
        import policy_digest as pd
        with open(os.path.join(HERE, "policy.json"), encoding="utf-8") as handle:
            block["policyDigest"] = pd.digest_of_text(handle.read())
    except Exception as exc:  # reported, never guessed
        block["policyDigest"] = "unavailable: %s" % type(exc).__name__
    return block


def main():
    parser = argparse.ArgumentParser(description="Cross-implementation parity check")
    parser.add_argument("--json", default=None, help="write the parity report here")
    args = parser.parse_args()

    node = shutil.which("node")
    if node is None:
        print("node not found: the cross-check needs Node.js; nothing is claimed without it")
        return 2

    policy, cases = py.load_inputs()
    vectors = py.load_vectors()
    rows_py = py.run(cases + vectors, policy)

    out = subprocess.run([node, os.path.join(HERE, "check.mjs")], cwd=HERE,
                         capture_output=True, text=True)
    if out.returncode != 0:
        print("check.mjs failed:\n" + out.stderr)
        return 1
    rows_js = json.loads(out.stdout)["results"]

    if len(rows_py) != len(rows_js):
        print("row count differs: python %d, javascript %d" % (len(rows_py), len(rows_js)))
        return 1

    disagree = []
    joined = []
    for a, b in zip(rows_py, rows_js):
        same = (a["result"], a["code"]) == (b["result"], b["code"]) and a.get("unknown") == b.get("unknown")
        if not same:
            disagree.append((a["id"], (a["result"], a["code"]), (b["result"], b["code"])))
        joined.append({
            "id": a["id"],
            "python": {"result": a["result"], "code": a["code"]},
            "javascript": {"result": b["result"], "code": b["code"]},
            "agree": same,
            "hold_group": "" if a["result"] in ("pass", "fail") else a["result"],
        })

    print("rows compared: %d (curated %d + vectors %d)" % (len(rows_py), len(cases), len(vectors)))
    print("disagreements: %d" % len(disagree))
    for row in disagree:
        print("  %s  python=%s/%s  javascript=%s/%s" % (row[0], row[1][0], row[1][1], row[2][0], row[2][1]))

    if args.json:
        node_version = subprocess.run([node, "--version"], capture_output=True, text=True).stdout.strip()
        report = {
            "schema": SCHEMA,
            "subject": "gateway-delegation-v0",
            "generated_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "python": sys.version.split()[0],
            "node": node_version,
            "inputs": inputs_block(),
            "rows_total": len(rows_py),
            "curated": len(cases),
            "vectors": len(vectors),
            "disagreements": len(disagree),
            "verdict": "agree" if not disagree else "diverge",
            "rows": joined,
        }
        with open(args.json, "w", encoding="utf-8", newline="\n") as handle:
            json.dump(report, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
        print("parity report -> %s (%d rows, verdict %s)" % (args.json, len(joined), report["verdict"]))

    if disagree:
        return 1
    print("two implementations, same verdict and same hold group on every row")
    return 0


if __name__ == "__main__":
    sys.exit(main())
