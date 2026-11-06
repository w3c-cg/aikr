"""Rebuild the fixtures for the key and evidence states test set.

Every key is derived from a published seed string, and Ed25519 signatures
are deterministic, so running this script twice produces byte-identical
files. The keys are test keys and protect nothing.

Usage: python generate.py      (writes fixtures/ and SHA256SUMS)
"""

from __future__ import annotations

import base64
import hashlib
import json
from pathlib import Path

import rfc8785
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat

HERE = Path(__file__).resolve().parent
FIX = HERE / "fixtures"
SEED = "w3c-cg/aikr trust/key-evidence-states-v0 seed "
IDENTIFIER = "urn:example:subject-a"
SOURCE = "https://keys.example/subject-a/history.json"


def b64u(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def key(name: str) -> Ed25519PrivateKey:
    seed = hashlib.sha256((SEED + name).encode("utf-8")).digest()
    return Ed25519PrivateKey.from_private_bytes(seed)


def pub(name: str) -> str:
    raw = key(name).public_key().public_bytes(Encoding.Raw, PublicFormat.Raw)
    return b64u(raw)


def sign(payload: dict, kid: str) -> dict:
    """Return {payload, sig} where sig.value = Ed25519(JCS(payload))."""
    value = key(kid).sign(rfc8785.dumps(payload))
    return {"payload": payload, "sig": {"alg": "Ed25519", "kid": kid, "value": b64u(value)}}


def timestamped(obj: dict, time: str) -> dict:
    """Attach a timestamp token from the pinned timestamp authority.

    The token signs the SHA-256 of JCS({payload, sig}) of the object, so it
    binds the signature as well as the payload.
    """
    digest = hashlib.sha256(rfc8785.dumps({"payload": obj["payload"], "sig": obj["sig"]}))
    token = sign({"type": "timestamp", "digest": "sha256:" + digest.hexdigest(), "time": time},
                 "tsa-1")
    return {**obj, "timestamp": token}


def statement(kid: str, claimed_time: str, tsa_time: str | None) -> dict:
    obj = sign({"type": "statement", "identifier": IDENTIFIER, "kid": kid,
                "claim": "example claim, content irrelevant to the checks",
                "signedAt": claimed_time}, kid)
    return timestamped(obj, tsa_time) if tsa_time else obj


def write(path: Path, data: dict) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    path.write_text(text, encoding="utf-8", newline="\n")
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def main() -> None:
    policy = {
        "identifier": IDENTIFIER,
        "anchor": {"kid": "k-2025", "publicKey": pub("k-2025"),
                   "validFrom": "2025-01-01T00:00:00Z", "validUntil": "2026-04-01T00:00:00Z"},
        "timestampAuthority": {"kid": "tsa-1", "publicKey": pub("tsa-1")},
        "stalenessBound": "PT24H",
        "onUnknown": "hold",
        "lineageComplete": True,
    }
    write(FIX / "policy.json", policy)
    write(FIX / "policy-open.json", {**policy, "lineageComplete": False})

    lineage = timestamped(sign({
        "type": "lineage", "identifier": IDENTIFIER,
        "predecessor": "k-2025", "successor": "k-2026",
        "successorPublicKey": pub("k-2026"),
        "successorValidFrom": "2026-03-01T00:00:00Z", "successorValidUntil": None,
    }, "k-2025"), "2026-03-01T00:00:00Z")
    keys = [
        {"kid": "k-2025", "publicKey": pub("k-2025")},
        {"kid": "k-2026", "publicKey": pub("k-2026"), "successorOf": "k-2025"},
        {"kid": "k-x", "publicKey": pub("k-x"), "successorOf": "k-2025"},
    ]
    revocation = sign({
        "type": "revocation", "identifier": IDENTIFIER, "kid": "k-2026",
        "effectiveFrom": "2026-09-01T00:00:00Z", "reason": "retired",
    }, "k-2026")

    base = {"identifier": IDENTIFIER, "keys": keys, "lineage": [lineage]}
    histories = {
        "complete": {**base, "revocations": []},
        "revoked": {**base, "revocations": [revocation]},
        "no-status": dict(base),  # the source publishes no revocation status at all
    }
    digests = {n: write(FIX / "history" / f"{n}.json", h) for n, h in histories.items()}

    statements = {
        "s-current": statement("k-2026", "2026-10-10T12:00:00Z", "2026-10-10T12:00:00Z"),
        "s-old-inside": statement("k-2025", "2026-02-01T12:00:00Z", "2026-02-01T12:00:00Z"),
        "s-old-after": statement("k-2025", "2026-05-01T12:00:00Z", "2026-05-01T12:00:00Z"),
        "s-old-untimed": statement("k-2025", "2026-02-01T12:00:00Z", None),
        "s-successor": statement("k-x", "2026-10-10T12:00:00Z", "2026-10-10T12:00:00Z"),
        "s-before-revocation": statement("k-2026", "2026-08-15T12:00:00Z",
                                         "2026-08-15T12:00:00Z"),
    }
    for n, s in statements.items():
        write(FIX / "statements" / f"{n}.json", s)

    eval_at = "2026-10-11T00:00:00Z"
    fresh = "2026-10-10T23:00:00Z"

    def lookup(history: str | None, fetched_at: str) -> dict:
        if history is None:
            return {"method": "https GET of key history document", "source": SOURCE,
                    "fetchedAt": fetched_at, "status": "unavailable",
                    "error": "connection timed out"}
        return {"method": "https GET of key history document", "source": SOURCE,
                "fetchedAt": fetched_at, "status": "ok",
                "document": f"history/{history}.json", "sha256": digests[history]}

    cases = [
        ("C01", "Positive control: current key, fresh lookup, valid signature",
         "s-current", lookup("complete", fresh)),
        ("C02", "Old key, signature timestamped inside its historical interval",
         "s-old-inside", lookup("complete", fresh)),
        ("C03", "Old key, signature timestamped after its interval closed",
         "s-old-after", lookup("complete", fresh)),
        ("C04", "Stale lookup: history fetched 5 days before evaluation, bound 24 hours",
         "s-current", lookup("complete", "2026-10-06T00:00:00Z")),
        ("C05", "Successor key listed by the source with no lineage statement",
         "s-successor", lookup("complete", fresh)),
        ("C06", "Revoked key, signature timestamped before the revocation took effect",
         "s-before-revocation", lookup("revoked", fresh)),
        ("C07", "Revoked key, signature timestamped after the revocation took effect",
         "s-current", lookup("revoked", fresh)),
        ("C08", "Validation source unavailable",
         "s-current", lookup(None, fresh)),
        ("C09", "Revocation status unknowable: source publishes no revocation list",
         "s-current", lookup("no-status", fresh)),
        ("C10", "Old key, signing time only self-asserted (no timestamp token)",
         "s-old-untimed", lookup("complete", fresh)),
        ("C11", "As C05, under a policy that does not assume the source publishes all lineage",
         "s-successor", lookup("complete", fresh), "policy-open.json"),
    ]
    for cid, desc, stmt, lk, *pol in cases:
        write(FIX / "cases" / f"{cid}.json",
              {"id": cid, "situation": desc, "evaluationInstant": eval_at,
               "policy": pol[0] if pol else "policy.json",
               "statement": f"statements/{stmt}.json", "lookup": lk})

    files = sorted(p for p in FIX.rglob("*.json"))
    lines = [f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(HERE).as_posix()}"
             for p in files]
    (HERE / "SHA256SUMS").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print(f"wrote {len(files)} fixture files and SHA256SUMS")


if __name__ == "__main__":
    main()
