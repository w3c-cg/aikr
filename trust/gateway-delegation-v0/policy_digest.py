#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""policy_digest.py — compute and check the digest the receipts bind to.

Definition (also stated in policy.json, notes.policyDigest):
  sha256 over the bytes of policy.json as written, with the string
  "policyDigest": "" in place of the digest value (i.e. the value is
  removed, the surrounding JSON text is not otherwise reformatted).

Usage:
  python policy_digest.py          # print the digest of policy.json
  python policy_digest.py --check  # exit 1 if policy.json's own value drifts
"""
import hashlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(HERE, "policy.json")


def digest_of_text(text):
    stripped = re.sub(r'("policyDigest"\s*:\s*)"(?:[^"\\]|\\.)*"', r'\1""', text, count=1)
    return "sha256:" + hashlib.sha256(stripped.encode("utf-8")).hexdigest()


def main():
    with open(PATH, encoding="utf-8") as handle:
        text = handle.read()
    computed = digest_of_text(text)
    stored = json.loads(text).get("policyDigest", "")
    if "--check" in sys.argv:
        ok = stored == computed
        print("policyDigest stored=%s computed=%s %s" % (stored, computed, "OK" if ok else "DRIFT"))
        return 0 if ok else 1
    print(computed)
    return 0


if __name__ == "__main__":
    sys.exit(main())
