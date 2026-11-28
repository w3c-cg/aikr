#!/usr/bin/env python3
"""Build review-packet.md: one file a reviewer can be handed, without network.

The packet carries the claims, the instructions that let them be falsified, the
curated table, the vector grid, the ten checks, and the observed distribution.
It does not carry credentials, and it is generated from the files in this
directory so it cannot drift from them silently.

    python3 make_review_packet.py
"""
import collections
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import check as _check  # noqa: E402

policy, cases = _check.load_inputs()
vectors = _check.load_vectors()
rows = _check.run(cases + vectors, policy)

tally = collections.Counter(r["result"] for r in rows)
codes = collections.Counter(r["code"] for r in rows if r["code"])
by_class = {("I%d" % i): 0 for i in range(1, 12)}
for v in vectors:
    for inv in v.get("invariant", []):
        if inv in by_class:
            by_class[inv] += 1


def section(path, title):
    with open(os.path.join(HERE, path), encoding="utf-8") as f:
        return "## %s\n\n%s\n" % (title, f.read().strip())


table = ["| Case | Result | Decision | Code | Situation |", "|---|---|---|---|---|"]
for r in rows:
    if r["id"].startswith("D"):
        table.append("| %s | %s | %s | %s | %s |" % (
            r["id"], r["result"], r["decision"], r["code"] or "—",
            r.get("about", "").replace("|", "/")))

vectors_table = ["| Class | Vectors |", "|---|---|"]
for k, v in by_class.items():
    vectors_table.append("| %s | %d |" % (k, v))

out = []
out.append("# Review packet — gateway delegation v0\n")
out.append("Generated from the files in this directory. Nothing here is fetched "
           "from the network; every number below was computed by running the "
           "checker at build time.\n")
out.append("## Observed distribution\n")
out.append("- rows: %d (%d curated + %d vectors)\n" % (len(rows), len(cases), len(vectors)))
out.append("- pass %d · record-unresolved %d · absent %d · check-incomplete %d · fail %d\n" % (
    tally.get("pass", 0), tally.get("record-unresolved", 0), tally.get("absent", 0),
    tally.get("check-incomplete", 0), tally.get("fail", 0)))
out.append("- distinct codes: %d\n" % len(codes))
out.append("- holds by side: record-unresolved %d · absent %d · check-incomplete %d — the "
           "row also carries `unknown.record`, `unknown.absent` and `unknown.checker`, so a "
           "consumer that reads only the verdict still knows which side it is on, and one "
           "that reads the split knows the remedy\n" % (
               tally.get("record-unresolved", 0), tally.get("absent", 0),
               tally.get("check-incomplete", 0)))
out.append("\n".join(vectors_table) + "\n")
out.append("## Curated cases\n")
out.append("\n".join(table) + "\n")
out.append("## Decision map and policy choices\n")
out.append("```json\n%s\n```\n" % json.dumps(
    {"evaluatedAt": policy["evaluatedAt"],
     "revocationFreshnessBoundSeconds": policy["revocationFreshnessBoundSeconds"],
     "decisionMap": policy["decisionMap"],
     "policyDigest": policy.get("policyDigest", "")}, ensure_ascii=False, indent=2))
out.append(section("EXTERNAL-REVIEW.md", "Notes for an independent reviewer"))
out.append(section("README.md", "README"))
out.append(section("VECTORS.md", "Vector set"))

with open(os.path.join(HERE, "review-packet.md"), "w", encoding="utf-8", newline="\n") as f:
    f.write("\n".join(out))
print("review-packet.md: %d rows, %d bytes" % (
    len(rows), os.path.getsize(os.path.join(HERE, "review-packet.md"))))
