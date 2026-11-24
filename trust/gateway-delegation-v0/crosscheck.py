#!/usr/bin/env python3
"""Run both implementations over the curated cases and the vector set, and
compare the outcomes row by row. Exit 1 on any disagreement.

    python3 crosscheck.py

The Python side runs in-process; the JavaScript side is `check.mjs`, run with
`node`. If node is absent the script says so and exits 2 rather than pretending
the cross-check passed.
"""
import json
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import check as py  # noqa: E402

node = shutil.which("node")
if node is None:
    print("node not found: the cross-check needs Node.js; nothing is claimed without it")
    sys.exit(2)

policy, cases = py.load_inputs()
vectors = py.load_vectors()
rows_py = py.run(cases + vectors, policy)

out = subprocess.run([node, os.path.join(HERE, "check.mjs")], cwd=HERE,
                     capture_output=True, text=True)
if out.returncode != 0:
    print("check.mjs failed:\n" + out.stderr)
    sys.exit(1)
rows_js = json.loads(out.stdout)["results"]

if len(rows_py) != len(rows_js):
    print("row count differs: python %d, javascript %d" % (len(rows_py), len(rows_js)))
    sys.exit(1)

disagree = []
for a, b in zip(rows_py, rows_js):
    if (a["result"], a["code"]) != (b["result"], b["code"]):
        disagree.append((a["id"], (a["result"], a["code"]), (b["result"], b["code"])))

print("rows compared: %d (curated %d + vectors %d)" % (len(rows_py), len(cases), len(vectors)))
print("disagreements: %d" % len(disagree))
for row in disagree:
    print("  %s  python=%s/%s  javascript=%s/%s" % (row[0], row[1][0], row[1][1], row[2][0], row[2][1]))
if disagree:
    sys.exit(1)
print("two implementations, same verdict on every row")
