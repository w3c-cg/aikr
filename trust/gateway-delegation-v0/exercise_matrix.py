# -*- coding: utf-8 -*-
"""对照 draft-he-agentproto-verifier-evidence 的 EXR-1：每一项检查的"拒绝通路"到底有没有被走到过。
对 122 行逐检查统计 pass / non-pass，并统计"该检查是唯一非 pass"的行数（单因归因）。"""
import json, check as C

inp, cur = C.load_inputs()
vec = C.load_vectors()
rows = C.run(cur + vec, inp)

stat = {}
for r in rows:
    for c in r["checks"]:
        s = stat.setdefault(c["check"], {"rows": 0, "pass": 0, "nonpass": 0, "sole": 0, "codes": {}})
        s["rows"] += 1
        if c["result"] == C.PASS:
            s["pass"] += 1
        else:
            s["nonpass"] += 1
            s["codes"][c["code"]] = s["codes"].get(c["code"], 0) + 1
    bad = [c for c in r["checks"] if c["result"] != C.PASS]
    if len(bad) == 1:
        stat[bad[0]["check"]]["sole"] += 1

print("%-16s %6s %6s %8s %7s  %s" % ("check", "rows", "pass", "nonpass", "sole", "codes"))
for name, s in sorted(stat.items()):
    flag = ""
    if s["nonpass"] == 0:
        flag = "  <-- UNEXERCISED"
    elif s["sole"] == 0:
        flag = "  <-- no sole-cause row"
    print("%-16s %6d %6d %8d %7d  %s%s" % (name, s["rows"], s["pass"], s["nonpass"], s["sole"],
                                          ",".join(sorted(s["codes"]))[:38], flag))

unex = [n for n, s in stat.items() if s["nonpass"] == 0]
noso = [n for n, s in stat.items() if s["nonpass"] and s["sole"] == 0]

# receipt 是条件检查：只在 decision=refuse 的行上求值，所以"唯一非 pass"在结构上不可能。
# 改为核：它是否只在 refuse 行上出现（这是它的域断言），并给出域内判别比。
rec_rows = [r for r in rows if any(c["check"] == "receipt" for c in r["checks"])]
rec_on_allow = [r["id"] for r in rec_rows if r["decision"] != "refuse"]
receipt_domain = {"rows_with_receipt_check": len(rec_rows),
                  "on_allow_decision": rec_on_allow,
                  "pass": stat["receipt"]["pass"], "nonpass": stat["receipt"]["nonpass"],
                  "note": "条件检查：仅在 refuse 路径求值，故不存在 single-cause 行；"
                          "域内 8 pass / 48 non-pass 构成同域正负对照"}
if rec_on_allow:
    raise SystemExit("receipt check evaluated on non-refuse rows: %s" % rec_on_allow)

out = {"schema": "aikr-exercise-matrix/0", "rows": len(rows), "checks": len(stat),
       "unexercised": unex, "no_sole_cause": noso, "receipt_domain": receipt_domain,
       "detail": stat,
       "method": "EXR-1 口径：一项检查的拒绝通路被走到过才算 exercised；single-cause 指该行只有它非 pass",
       "limits": ["exercised + 单因 不等于 discriminating pair：本表没有事先声明的反事实种群",
                  "只覆盖当前 122 行，新增语料可能改变结论"]}
open("exercise-matrix.json", "w", encoding="utf-8").write(json.dumps(out, ensure_ascii=False, indent=2) + "\n")
print("\nunexercised: %s   no single-cause: %s" % (unex or "none", noso or "none"))
