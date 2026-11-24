#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Reference checker for trust/gateway-delegation-v0.

Reads policy.json and fixtures/cases/*.json, runs the checks listed in README.md
in order, and reports one result per case. Standard library only; no network;
deterministic at the policy's pinned instant.

Usage:
  python check.py                 # run the set, print the table
  python check.py --json out.json # write the machine-readable results here
  python check.py --selftest      # verify expected.json, and that a permissive
                                  # checker is caught by the set
"""
import argparse
import datetime as dt
import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PASS, FAIL, UNKNOWN = "pass", "fail", "could-not-determine"


def parse_time(value):
    if not isinstance(value, str):
        raise ValueError("not a string")
    text = value.strip()
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    parsed = dt.datetime.fromisoformat(text)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=dt.timezone.utc)
    return parsed.astimezone(dt.timezone.utc)


def load_inputs():
    with open(os.path.join(HERE, "policy.json"), encoding="utf-8") as handle:
        policy = json.load(handle)
    cases = []
    pattern = os.path.join(HERE, "fixtures", "cases", "*.json")
    for path in sorted(glob.glob(pattern)):
        with open(path, encoding="utf-8") as handle:
            cases.append(json.load(handle))
    return policy, cases


def check_case(case, policy):
    """Return (result, code, per-check list). Checks run in the README's order."""
    now = parse_time(policy["evaluatedAt"])
    bound = int(policy["revocationFreshnessBoundSeconds"])
    mandate = case["mandate"]
    request = case["request"]
    payload = request.get("payload") or {}
    checks = []

    # 1. subject: the mandate names the agent it was issued to
    if request.get("agentId") == mandate.get("subject"):
        checks.append(("subject", PASS, ""))
    else:
        checks.append(("subject", FAIL, "SUBJECT_MISMATCH"))

    # 2. mandate window at the evaluation instant
    try:
        issued = parse_time(mandate["issuedAt"])
        expires = parse_time(mandate["expiresAt"])
    except (KeyError, ValueError, TypeError):
        checks.append(("window", UNKNOWN, "WINDOW_UNPARSABLE"))
    else:
        if now < issued:
            checks.append(("window", FAIL, "MANDATE_NOT_YET_VALID"))
        elif now >= expires:
            checks.append(("window", FAIL, "MANDATE_EXPIRED"))
        else:
            checks.append(("window", PASS, ""))

    # 3. mandate signature present and verified at issue time
    if mandate.get("signature") == "ok":
        checks.append(("signature", PASS, ""))
    else:
        checks.append(("signature", FAIL, "MANDATE_UNSIGNED"))

    # 4. attenuation: declared scope must be inside the grant, never wider
    declared = request.get("declaredScope") or []
    granted = mandate.get("grantedScope") or []
    if not declared:
        checks.append(("attenuation", UNKNOWN, "NO_DECLARED_SCOPE"))
    else:
        outside = [item for item in declared if item not in granted]
        if outside:
            checks.append(("attenuation", FAIL, "SCOPE_WIDENED"))
        else:
            checks.append(("attenuation", PASS, ""))

    # 5. content mediation: the payload is inspected before forwarding
    if payload.get("opaque"):
        checks.append(("content", UNKNOWN, "OPAQUE_CONTENT"))
    elif payload.get("instructions"):
        checks.append(("content", FAIL, "CONTENT_OVERRIDE"))
    elif payload.get("claimedRole"):
        checks.append(("content", FAIL, "ROLE_SPOOF"))
    else:
        checks.append(("content", PASS, ""))

    # 6. revocation status, with an age bound
    revocation = case.get("revocation") or {}
    status = revocation.get("status")
    try:
        checked = parse_time(revocation["checkedAt"])
    except (KeyError, ValueError, TypeError):
        checked = None
    if status == "none":
        if checked is None:
            checks.append(("revocation", UNKNOWN, "REVOCATION_UNKNOWN"))
        elif (now - checked).total_seconds() > bound:
            checks.append(("revocation", UNKNOWN, "STALE_REVOCATION"))
        else:
            checks.append(("revocation", PASS, ""))
    elif status == "revoked":
        try:
            effective = parse_time(revocation["effectiveFrom"])
        except (KeyError, ValueError, TypeError):
            effective = None
        if effective is not None and now < effective:
            checks.append(("revocation", UNKNOWN, "REVOCATION_NOT_YET_EFFECTIVE"))
        else:
            checks.append(("revocation", FAIL, "REVOKED"))
    elif status == "unreachable":
        checks.append(("revocation", UNKNOWN, "SOURCE_UNREACHABLE"))
    else:
        checks.append(("revocation", UNKNOWN, "REVOCATION_UNKNOWN"))

    # 7. what the record points at must be reachable at verification time
    evidence = case.get("evidence") or {}
    if evidence.get("pointer") == "reachable":
        checks.append(("evidence", PASS, ""))
    else:
        checks.append(("evidence", UNKNOWN, "POINTER_UNREACHABLE"))

    results = [item[1] for item in checks]
    if FAIL in results:
        result = FAIL
    elif UNKNOWN in results:
        result = UNKNOWN
    else:
        result = PASS
    codes = [item[2] for item in checks if item[2]]
    return result, (codes[0] if codes else ""), checks


def permissive_check(case, policy):
    """The defect the set is meant to catch: policy checked, content ignored,
    unknown folded into pass. Used only by --selftest."""
    mandate = case["mandate"]
    request = case["request"]
    if request.get("agentId") != mandate.get("subject"):
        return FAIL, "SUBJECT_MISMATCH"
    if request.get("declaredScope") and \
            any(s not in (mandate.get("grantedScope") or []) for s in request["declaredScope"]):
        return FAIL, "SCOPE_WIDENED"
    if (case.get("revocation") or {}).get("status") == "revoked":
        return FAIL, "REVOKED"
    return PASS, ""


def run(cases, policy, checker=check_case):
    rows = []
    for case in cases:
        out = checker(case, policy)
        if len(out) == 2:
            result, code = out
            checks = []
        else:
            result, code, checks = out
        rows.append({
            "id": case["id"],
            "result": result,
            "decision": policy["decisionMap"][result],
            "code": code,
            "checks": [{"check": name, "result": res, "code": c} for name, res, c in checks],
            "about": case.get("about", ""),
        })
    return rows


def print_table(rows):
    print("%-4s %-19s %-7s %-26s" % ("case", "result", "decision", "first code"))
    print("-" * 62)
    for row in rows:
        print("%-4s %-19s %-7s %-26s" % (row["id"], row["result"], row["decision"], row["code"] or "-"))
    tally = {}
    for row in rows:
        tally[row["result"]] = tally.get(row["result"], 0) + 1
    print("\n%d cases: %s" % (len(rows), ", ".join("%s %d" % (k, tally[k]) for k in sorted(tally))))


def selftest():
    policy, cases = load_inputs()
    failures = 0
    rows = run(cases, policy)
    expected_path = os.path.join(HERE, "expected.json")
    with open(expected_path, encoding="utf-8") as handle:
        expected = json.load(handle)
    by_id = {item["id"]: item for item in expected["results"]}
    for row in rows:
        want = by_id.get(row["id"])
        if not want:
            print("[FAIL] %s missing from expected.json" % row["id"])
            failures += 1
        elif want["result"] != row["result"] or want["code"] != row["code"]:
            print("[FAIL] %s expected %s/%s, checker gave %s/%s" % (
                row["id"], want["result"], want["code"], row["result"], row["code"]))
            failures += 1
    print("[OK] expected.json matches the checker on %d cases" % (len(rows) - failures))

    permissive = run(cases, policy, permissive_check)
    disagree = [row["id"] for row, ref in zip(permissive, rows) if row["result"] != ref["result"]]
    print("[%s] a permissive checker (content ignored, unknown folded into pass) is caught on %d cases: %s" % (
        "OK" if len(disagree) >= 5 else "FAIL", len(disagree), ", ".join(disagree)))
    if len(disagree) < 5:
        failures += 1

    # A fixture change must move the result: proves the table is computed,
    # not asserted. D02 with an in-grant scope collapses to the D01 result.
    tampered = None
    for case in cases:
        if case["id"] == "D02":
            tampered = json.loads(json.dumps(case))
            tampered["request"]["declaredScope"] = ["tool:search"]
    if tampered is None:
        print("[FAIL] D02 not found for the tamper test")
        failures += 1
    else:
        result, _, _ = check_case(tampered, policy)
        ok = result == PASS
        print("[%s] tamper test: D02 with an in-grant scope now gives %s (was fail)" % (
            "OK" if ok else "FAIL", result))
        if not ok:
            failures += 1
    # A policy change must move the result too. D13 sits one hour outside the
    # 24-hour revocation bound; widening the bound to 25 hours makes it pass,
    # so a silently loosened bound is visible instead of being absorbed.
    widened = json.loads(json.dumps(policy))
    widened["revocationFreshnessBoundSeconds"] = 90000
    flipped = []
    for case in cases:
        ref = next(r for r in rows if r["id"] == case["id"])
        result, _, _ = check_case(case, widened)
        if result != ref["result"]:
            flipped.append(case["id"])
    ok = "D13" in flipped
    print("[%s] bound test: 24h -> 25h changes %d case(s) (%s)" % (
        "OK" if ok else "FAIL", len(flipped), ", ".join(flipped) or "none"))
    if not ok:
        failures += 1
    return 1 if failures else 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", default=None, help="write results here")
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args()
    if args.selftest:
        return selftest()
    policy, cases = load_inputs()
    rows = run(cases, policy)
    print_table(rows)
    if args.json:
        with open(args.json, "w", encoding="utf-8", newline="\n") as handle:
            json.dump({"schema": "aikr-gateway-delegation-results/0", "results": rows},
                      handle, ensure_ascii=False, indent=2)
            handle.write("\n")
        print("\nJSON -> %s" % args.json)
    return 0


if __name__ == "__main__":
    sys.exit(main())
