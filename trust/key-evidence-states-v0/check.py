"""Reference checker for the key and evidence states test set.

Runs every case in fixtures/cases/ and every mutation control below, and
compares each result with expected.json. Exits 0 only if the fixtures match
SHA256SUMS and every result matches.

Results are three-valued: pass, fail, could-not-determine. A check that
cannot be completed is never reported as pass or as fail.

Usage: python check.py [-v]
"""

from __future__ import annotations

import base64
import copy
import hashlib
import json
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

import rfc8785
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

HERE = Path(__file__).resolve().parent
FIX = HERE / "fixtures"
PASS, FAIL, CND = "pass", "fail", "could-not-determine"
DECISION = {PASS: "admit", FAIL: "refuse", CND: "hold"}


def t(s: str) -> datetime:
    return datetime.fromisoformat(s.replace("Z", "+00:00"))


def duration(s: str) -> timedelta:
    m = re.fullmatch(r"P(?:(\d+)D)?(?:T(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?)?", s)
    if not m:
        raise ValueError(f"unsupported duration {s}")
    d, h, mi, se = (int(x or 0) for x in m.groups())
    return timedelta(days=d, hours=h, minutes=mi, seconds=se)


def b64d(s: str) -> bytes:
    return base64.urlsafe_b64decode(s + "=" * (-len(s) % 4))


def verify(obj: dict, public_key: str) -> bool:
    """obj is {payload, sig}; sig.value must be Ed25519 over JCS(payload)."""
    try:
        Ed25519PublicKey.from_public_bytes(b64d(public_key)).verify(
            b64d(obj["sig"]["value"]), rfc8785.dumps(obj["payload"]))
        return True
    except (InvalidSignature, ValueError, KeyError):
        return False


def serialize(doc: dict) -> bytes:
    return (json.dumps(doc, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode()


def attested_time(obj: dict, policy: dict) -> tuple[str, datetime | None]:
    """Signing time from the timestamp token: ('ok', T), ('absent', None) or ('bad', None)."""
    tok = obj.get("timestamp")
    if tok is None:
        return "absent", None
    tsa = policy["timestampAuthority"]
    digest = hashlib.sha256(rfc8785.dumps({"payload": obj["payload"], "sig": obj["sig"]}))
    if (tok["sig"]["kid"] != tsa["kid"] or not verify(tok, tsa["publicKey"])
            or tok["payload"]["digest"] != "sha256:" + digest.hexdigest()):
        return "bad", None
    return "ok", t(tok["payload"]["time"])


class Outcome(Exception):
    def __init__(self, result: str, reason: str):
        self.result, self.reason = result, reason


def evaluate(inp: dict) -> tuple[str, str, list[tuple[str, str, str]]]:
    """Return (result, reason, trace). trace lists (check, result, reason)."""
    policy, stmt, lookup, history = inp["policy"], inp["statement"], inp["lookup"], inp["history"]
    now = t(inp["evaluationInstant"])
    trace: list[tuple[str, str, str]] = []

    def note(check: str, result: str, reason: str) -> None:
        trace.append((check, result, reason))

    # 1. Was the validation source reachable at all?
    if lookup["status"] != "ok":
        note("source", CND, "SOURCE_UNAVAILABLE")
        return finish(trace, None)
    note("source", PASS, "OK")

    # 2. Is the document the one the lookup record says was fetched?
    if hashlib.sha256(serialize(history)).hexdigest() != lookup["sha256"]:
        note("history-digest", FAIL, "HISTORY_DIGEST_MISMATCH")
        return finish(trace, None)
    note("history-digest", PASS, "OK")

    # 3. Is the lookup recent enough under the declared staleness bound?
    age = now - t(lookup["fetchedAt"])
    if age > duration(policy["stalenessBound"]):
        note("freshness", CND, "STALE_LOOKUP")
    else:
        note("freshness", PASS, "OK")

    def revoked_at(kid: str, public_key: str, when: datetime) -> None:
        if "revocations" not in history:
            raise Outcome(CND, "NO_STATUS_SOURCE")
        for r in history["revocations"]:
            if r["payload"]["kid"] != kid:
                continue
            if r["sig"]["kid"] != kid or not verify(r, public_key):
                raise Outcome(CND, "REVOCATION_UNVERIFIABLE")
            if when >= t(r["payload"]["effectiveFrom"]):
                raise Outcome(FAIL, "KEY_REVOKED")

    def resolve(kid: str, depth: int = 0) -> dict:
        """Key and interval for kid, from the pinned anchor via signed lineage only.
        The unsigned key listing in the history document is never trusted."""
        a = policy["anchor"]
        if kid == a["kid"]:
            return {"publicKey": a["publicKey"], "from": t(a["validFrom"]),
                    "until": t(a["validUntil"]) if a["validUntil"] else None}
        if depth > 8:
            raise Outcome(FAIL, "NO_LINEAGE")
        links = [x for x in history["lineage"] if x["payload"]["successor"] == kid
                 and x["payload"]["identifier"] == policy["identifier"]]
        if not links:
            # Absence is a definite no only if the policy says the source publishes all
            # lineage; otherwise a handover may exist elsewhere, so continuity is open.
            if policy.get("lineageComplete"):
                raise Outcome(FAIL, "NO_LINEAGE")
            raise Outcome(CND, "LINEAGE_NOT_ESTABLISHED")
        link = links[0]
        pred_kid = link["payload"]["predecessor"]
        pred = resolve(pred_kid, depth + 1)
        if link["sig"]["kid"] != pred_kid or not verify(link, pred["publicKey"]):
            raise Outcome(FAIL, "BAD_LINEAGE")
        status, when = attested_time(link, policy)
        if status != "ok":
            raise Outcome(FAIL, "BAD_LINEAGE")
        if not within(pred, when):
            raise Outcome(FAIL, "LINEAGE_OUTSIDE_INTERVAL")
        try:
            revoked_at(pred_kid, pred["publicKey"], when)
        except Outcome as o:
            if o.result == FAIL:
                raise
            unresolved.append(o.reason)  # key still resolves; record the open question
        p = link["payload"]
        return {"publicKey": p["successorPublicKey"], "from": t(p["successorValidFrom"]),
                "until": t(p["successorValidUntil"]) if p["successorValidUntil"] else None}

    # 4. Is the signing key linked to the pinned anchor by signed lineage?
    kid = stmt["sig"]["kid"]
    unresolved: list[str] = []
    try:
        k = resolve(kid)
        note("lineage", CND if unresolved else PASS, unresolved[0] if unresolved else "OK")
    except Outcome as o:
        note("lineage", o.result, o.reason)
        return finish(trace, None)

    # 5. Does the signature verify over the JCS bytes of the payload?
    if not verify(stmt, k["publicKey"]):
        note("signature", FAIL, "BAD_SIGNATURE")
        return finish(trace, None)
    note("signature", PASS, "OK")

    # 6. When was it signed, according to an attested source?
    status, signed = attested_time(stmt, policy)
    if status == "bad":
        note("signing-time", FAIL, "BAD_TIMESTAMP")
        return finish(trace, None)
    if status == "absent":
        note("signing-time", "absent", "judged at the evaluation instant")
    else:
        note("signing-time", PASS, "OK")
    ref = signed or now

    # 7. Was the key inside its validity interval at that time?
    if not within(k, ref):
        if signed is None:
            note("interval", CND, "SIGNING_TIME_UNATTESTED")
        else:
            note("interval", FAIL, "KEY_OUTSIDE_VALIDITY")
        return finish(trace, None)
    note("interval", PASS, "OK")

    # 8. Was the key revoked at that time?
    try:
        revoked_at(kid, k["publicKey"], ref)
        note("revocation", PASS, "OK")
    except Outcome as o:
        if o.reason == "KEY_REVOKED" and signed is None:
            note("revocation", CND, "SIGNING_TIME_UNATTESTED")
        else:
            note("revocation", o.result, o.reason)
        return finish(trace, None)

    current = within(k, now)
    try:
        revoked_at(kid, k["publicKey"], now)
    except Outcome:
        current = False
    return finish(trace, current)


def within(k: dict, when: datetime) -> bool:
    return k["from"] <= when and (k["until"] is None or when < k["until"])


def finish(trace: list, current: bool | None) -> tuple[str, str, list]:
    for want in (FAIL, CND):
        for check, result, reason in trace:
            if result == want:
                return want, reason, trace
    return PASS, "OK_CURRENT" if current else "OK_HISTORICAL", trace


def load_case(cid: str) -> dict:
    c = json.loads((FIX / "cases" / f"{cid}.json").read_text(encoding="utf-8"))
    lk = c["lookup"]
    history = None
    if lk["status"] == "ok":
        history = json.loads((FIX / lk["document"]).read_text(encoding="utf-8"))
    return {"id": cid, "evaluationInstant": c["evaluationInstant"], "lookup": lk,
            "history": history,
            "policy": json.loads((FIX / c["policy"]).read_text(encoding="utf-8")),
            "statement": json.loads((FIX / c["statement"]).read_text(encoding="utf-8"))}


# Mutation controls. Each takes a passing input, makes one small change, and
# must flip the result. Edits to the history document re-record its digest
# (as if a fresh source served the changed document), except M11.

def flip(sig_value: str) -> str:
    raw = bytearray(b64d(sig_value))
    raw[0] ^= 0x01
    return base64.urlsafe_b64encode(bytes(raw)).rstrip(b"=").decode()


def rehash(i: dict) -> None:
    i["lookup"]["sha256"] = hashlib.sha256(serialize(i["history"])).hexdigest()


def m01(i):
    i["statement"]["sig"]["value"] = flip(i["statement"]["sig"]["value"])


def m02(i):
    i["evaluationInstant"] = "2026-10-14T00:00:00Z"


def m03(i):
    i["history"]["lineage"] = []
    rehash(i)


def m04(i):
    i["history"]["lineage"][0]["sig"]["value"] = flip(i["history"]["lineage"][0]["sig"]["value"])
    rehash(i)


def m05(i):
    i["policy"]["anchor"]["validUntil"] = "2026-01-01T00:00:00Z"


def m06(i):
    i["statement"]["timestamp"]["payload"]["time"] = "2026-02-01T12:00:01Z"


def m07(i):
    del i["statement"]["timestamp"]


def m08(i):
    i["history"]["revocations"][0]["payload"]["effectiveFrom"] = "2026-08-01T00:00:00Z"
    rehash(i)


def m09(i):
    i["lookup"] = {k: v for k, v in i["lookup"].items() if k not in ("document", "sha256")}
    i["lookup"]["status"] = "unavailable"
    i["history"] = None


def m10(i):
    del i["history"]["revocations"]
    rehash(i)


def m11(i):
    del i["history"]["revocations"]  # digest left as recorded


MUTATIONS = {
    "M01": ("C01", "flip one byte of the statement signature", m01),
    "M02": ("C01", "move the evaluation instant 3 days later", m02),
    "M03": ("C01", "drop the lineage statement for k-2026", m03),
    "M04": ("C01", "flip one byte of the lineage signature", m04),
    "M05": ("C02", "close the anchor interval before the signing time", m05),
    "M06": ("C02", "move the timestamp token time by one second", m06),
    "M07": ("C02", "remove the timestamp token", m07),
    "M08": ("C06", "move the revocation effectiveFrom without re-signing", m08),
    "M09": ("C01", "make the validation source unavailable", m09),
    "M10": ("C01", "remove the revocation list from the source", m10),
    "M11": ("C01", "alter the history without updating the recorded digest", m11),
}


def check_sums() -> bool:
    ok = True
    for line in (HERE / "SHA256SUMS").read_text(encoding="utf-8").splitlines():
        digest, name = line.split("  ", 1)
        if hashlib.sha256((HERE / name).read_bytes()).hexdigest() != digest:
            print(f"SHA256 mismatch: {name}")
            ok = False
    return ok


def main() -> int:
    verbose = "-v" in sys.argv
    expected = json.loads((HERE / "expected.json").read_text(encoding="utf-8"))
    sums_ok = check_sums()
    print(f"fixtures match SHA256SUMS: {'yes' if sums_ok else 'NO'}")
    failures = 0

    def report(label: str, desc: str, inp: dict, exp: dict) -> None:
        nonlocal failures
        result, reason, trace = evaluate(inp)
        got = {"result": result, "decision": DECISION[result], "reason": reason}
        want = {k: exp[k] for k in ("result", "decision", "reason")}
        ok = got == want
        failures += not ok
        print(f"{'ok  ' if ok else 'MISMATCH'} {label:4} {result:20} {DECISION[result]:7} "
              f"{reason:26} {desc}")
        if not ok:
            print(f"     expected {want}")
        if verbose or not ok:
            for check, r, why in trace:
                print(f"       {check:15} {r:20} {why}")

    print("\nCases")
    for cid in sorted(expected["cases"]):
        inp = load_case(cid)
        situation = json.loads((FIX / "cases" / f"{cid}.json").read_text())["situation"]
        report(cid, situation, inp, expected["cases"][cid])

    print("\nMutation controls")
    for mid, (base, desc, fn) in MUTATIONS.items():
        inp = copy.deepcopy(load_case(base))
        fn(inp)
        report(mid, f"{base}: {desc}", inp, expected["mutations"][mid])

    total = len(expected["cases"]) + len(MUTATIONS)
    print(f"\n{total - failures}/{total} match expected.json")
    return 0 if sums_ok and failures == 0 and len(expected["mutations"]) == len(MUTATIONS) else 1


if __name__ == "__main__":
    sys.exit(main())
