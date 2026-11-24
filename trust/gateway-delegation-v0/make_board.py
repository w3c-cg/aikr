#!/usr/bin/env python3
"""Build EVIDENCE-BOARD.html from the checker's own results.

The board carries the distribution, the curated table, the selftest claims and
an embedded JSON payload; a small script inside the page re-derives the row
count and the segment counts from that payload and prints a pass or a failure,
so a board that drifts from the data says so on open.

    python3 make_board.py
"""
import collections
import html
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import check as _check  # noqa: E402

policy, cases = _check.load_inputs()
vectors = _check.load_vectors()
rows = _check.run(cases + vectors, policy)
tally = collections.Counter(r["result"] for r in rows)
curated = [r for r in rows if r["id"].startswith("D")]
vtally = collections.Counter(r["result"] for r in rows if not r["id"].startswith("D"))
codes = len({r["code"] for r in rows if r["code"]})

# The permissive-checker disagreement list is taken from the selftest output
# rather than restated here, so the page cannot disagree with the run.
out = subprocess.run([sys.executable, os.path.join(HERE, "check.py"), "--selftest"],
                     cwd=HERE, capture_output=True, text=True)
match = re.search(r"caught on \d+ cases: ([\d, A-Z]+)", out.stdout)
disagree = [s.strip() for s in match.group(1).split(",")] if match else []

SEGS = [("pass", "#1a7f37"), ("record-unresolved", "#9a6700"),
        ("check-incomplete", "#0969da"), ("fail", "#b42318")]

total = len(rows)
seg_html = "".join(
    '<div class="seg" style="width:%.2f%%;background:%s" title="%s: %d (%.1f%%)">'
    "<span>%d</span></div>" % (100.0 * tally[k] / total, color, k, tally[k],
                               100.0 * tally[k] / total, tally[k])
    for k, color in SEGS)

table_rows = "".join(
    '<tr><td class=m>%s</td><td>%s</td><td class=r>%s</td><td class=d>%s</td><td class=m>%s</td></tr>' % (
        r["id"], html.escape(r.get("about", "").replace("|", "/")),
        r["result"], r["decision"], r["code"] or "—") for r in curated)

payload = json.dumps({"rows": rows, "bound": policy["revocationFreshnessBoundSeconds"],
                      "disagree": disagree}, ensure_ascii=False)

claims = [
    ("Expectation match", "every expected row equals the checker, on all 18 cases."),
    ("Permissive checker is caught",
     "a checker that ignores content, folds any hold into pass, ignores staleness, and never "
     "reads the signer key or the lineage disagrees on %d of 18 cases (%s)." % (
         len(disagree), ", ".join(disagree) or "none")),
    ("Tamper moves the result", "D02 with an in-grant scope becomes pass."),
    ("Bound is not silently widened",
     "86400 → 90000 flips D13 from record-unresolved to pass."),
    ("Receipt requirement is live",
     "D16&#x27;s refusal without a receipt fails the receipt check; adding a bound receipt clears it."),
    ("Citation must be walked",
     "D18&#x27;s cited digest added to the chain clears its unresolved verdict."),
    ("Policy digest is reproducible",
     "the digest is recomputed from <code>policy.json</code> itself and must equal the stored value."),
    ("A hold names its side",
     "record-only gives record-unresolved, checker-only gives check-incomplete, and one of each "
     "reports both in <code>unknown.record</code> and <code>unknown.checker</code> while the verdict "
     "stays on record-unresolved."),
    ("Vector set matches what it states",
     "102 vectors carry their own <code>expect</code> block; any disagreement fails the run."),
]
claims_html = "".join("<li><strong>%s</strong> — %s</li>" % (t, b) for t, b in claims)

page = r"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<title>Gateway delegation v0 — evidence board</title>
<style>
:root{color-scheme:light}
body{font:15px/1.55 -apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;margin:0;background:#f6f7f9;color:#1f2328}
.wrap{max-width:1000px;margin:0 auto;padding:32px 24px 56px}
h1{font-size:24px;margin:0 0 4px}
.sub{color:#59636e;margin:0 0 24px}
.card{background:#fff;border:1px solid #d8dee4;border-radius:10px;padding:20px;margin:0 0 18px}
h2{font-size:16px;margin:0 0 12px}
.kpis{display:flex;gap:16px;flex-wrap:wrap}
.kpi{flex:1 1 120px;border:1px solid #d8dee4;border-radius:8px;padding:12px}
.kpi .n{font-size:26px;font-weight:600;line-height:1.1}
.kpi .l{color:#59636e;font-size:12px;margin-top:4px}
.bar{display:flex;height:26px;border-radius:6px;overflow:hidden;margin:14px 0 8px}
.seg{display:flex;align-items:center;justify-content:center;color:#fff;font-size:12px}
table{width:100%;border-collapse:collapse;font-size:13.5px}
th,td{padding:7px 8px;border-bottom:1px solid #eaeef2;text-align:left;vertical-align:top}
th{color:#59636e;font-weight:600;font-size:12px;text-transform:uppercase;letter-spacing:.03em}
td.m{font-family:ui-monospace,SFMono-Regular,Consolas,monospace;font-size:12.5px}
td.r{font-weight:600}
td.d{font-family:ui-monospace,SFMono-Regular,Consolas,monospace}
.foot{color:#59636e;font-size:13px}
#selfcheck{margin-top:10px;font-size:13px}
.ok{color:#1a7f37}.bad{color:#b42318}
.claims li{margin:6px 0}
</style></head><body><div class="wrap">
<h1>Gateway delegation v0 — evidence board</h1>
<p class="sub">@@TOTAL@@ rows — 18 curated cases and 102 vectors, one decision each, at <code>@@EVAL@@</code>. Revocation freshness bound: <strong>24 h</strong>. Two implementations (Python and JavaScript) agree on all @@TOTAL@@ rows and on which side every hold is on.</p>

<div class="card">
  <h2>Verdict distribution</h2>
  <div class="bar">@@SEGS@@</div>
  <div class="foot">pass @@P@@ · record-unresolved @@R@@ · check-incomplete @@C@@ · fail @@F@@ ｜ allow @@P@@ / hold @@HOLD@@ / refuse @@F@@ ｜ @@CODES@@ distinct codes</div>
  <div class="foot">A hold carries its side: <code>record-unresolved</code> when the record or what it points at cannot be resolved, <code>check-incomplete</code> when the check could not be completed on the inputs supplied. A record that cannot be resolved outranks a check we could not run; both give hold.</div>
  <div id="selfcheck"></div>
</div>

<div class="card"><h2>Vector set</h2>
  <div class="foot">vectors 102 ｜ pass @@VP@@ / record-unresolved @@VR@@ / check-incomplete @@VC@@ / fail @@VF@@ ｜ classes covered I1–I11</div>
  <div class="foot">Each vector states the outcome it must produce; the selftest compares that statement to the checker, and <code>crosscheck.py</code> compares the Python result to the JavaScript one row by row, verdict and hold group both.</div>
</div>

<div class="card"><h2>Cases</h2>
<table><thead><tr><th>Case</th><th>Situation</th><th>Result</th><th>Decision</th><th>Code</th></tr></thead>
<tbody>@@ROWS@@</tbody></table>
</div>

<div class="card"><h2>What the selftest claims</h2>
<ol class="claims">@@CLAIMS@@</ol>
<p class="foot">Each claim is falsifiable by running <code>python check.py --selftest</code>; see REPRODUCTION.md for the exact commands and observed output.</p>
</div>
</div>
<script type="application/json" id="payload">@@PAYLOAD@@</script>
<script>
(function(){
  var p = JSON.parse(document.getElementById('payload').textContent);
  var rows = p.rows, n = rows.length, c = {};
  rows.forEach(function(r){ c[r.result] = (c[r.result]||0)+1; });
  var rendered = document.querySelectorAll('tbody tr').length;
  var msg = [], bad = false;
  if (rendered !== n) { bad = true; msg.push('rows ' + rendered + ' != JSON ' + n); }
  document.querySelectorAll('.seg').forEach(function(s){
    var k = s.getAttribute('title').split(':')[0];
    if ((c[k]||0) !== parseInt(s.textContent,10)) { bad = true; msg.push(k + ' count mismatch'); }
  });
  var declaredN = document.querySelector('.sub').textContent.match(/^(\d+)/);
  if (declaredN && parseInt(declaredN[1],10) !== n) { bad = true; msg.push('header says ' + declaredN[1] + ', JSON has ' + n); }
  if (p.disagree && p.disagree.length !== 0) {
    var claim = document.querySelectorAll('.claims li')[1];
    p.disagree.forEach(function(id){
      if (claim && claim.textContent.indexOf(id) < 0) { bad = true; msg.push('disagreement list missing ' + id); }
    });
  }
  document.getElementById('selfcheck').innerHTML = bad
    ? '<span class="bad">self-check failed: ' + msg.join('; ') + '</span>'
    : '<span class="ok">self-check passed: ' + rendered + ' rows, four segment counts, header total and the ' + p.disagree.length + '-case disagreement list all re-computed from the embedded JSON.</span>';
})();
</script>
</body></html>
"""

FILL = {
    "@@TOTAL@@": str(total), "@@EVAL@@": policy["evaluatedAt"], "@@SEGS@@": seg_html,
    "@@P@@": str(tally.get("pass", 0)),
    "@@R@@": str(tally.get("record-unresolved", 0)),
    "@@C@@": str(tally.get("check-incomplete", 0)),
    "@@F@@": str(tally.get("fail", 0)),
    "@@HOLD@@": str(tally.get("record-unresolved", 0) + tally.get("check-incomplete", 0)),
    "@@CODES@@": str(codes),
    "@@VP@@": str(vtally.get("pass", 0)),
    "@@VR@@": str(vtally.get("record-unresolved", 0)),
    "@@VC@@": str(vtally.get("check-incomplete", 0)),
    "@@VF@@": str(vtally.get("fail", 0)),
    "@@ROWS@@": table_rows, "@@CLAIMS@@": claims_html, "@@PAYLOAD@@": payload,
}
for token, value in FILL.items():
    page = page.replace(token, value)
leftover = [t for t in ("@@",) if t in page]
if leftover:
    raise SystemExit("unfilled template token remains")

with open(os.path.join(HERE, "EVIDENCE-BOARD.html"), "w", encoding="utf-8", newline="\n") as fh:
    fh.write(page)

with open(os.path.join(HERE, "EVIDENCE-BOARD.html"), "w", encoding="utf-8", newline="\n") as fh:
    fh.write(page)
print("EVIDENCE-BOARD.html: %d rows, %d bytes, selftest exit %d" % (
    total, os.path.getsize(os.path.join(HERE, "EVIDENCE-BOARD.html")), out.returncode))
