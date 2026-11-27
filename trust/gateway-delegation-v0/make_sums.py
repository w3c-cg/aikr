# -*- coding: utf-8 -*-
"""Rebuild SHA256SUMS: one line per shipped file, lowercase sha256, posix path.

Excluded on purpose:
  - SHA256SUMS itself (it cannot contain its own hash);
  - SHA256SUMS.ots (an OpenTimestamps proof *of* SHA256SUMS: listing it would
    change the file the proof commits to, and the proof would stop verifying);
  - the AER-1 fetch cache (aer1/), third-party bytes fetched at build time;
  - regenerated run reports (parity-report.json, mutation-report.json): their
    content changes on every run, so pinning them here would make the check
    fail for reasons that are not drift.

The directory is taken from this file's location, so the same script runs on a
Linux runner and on a Windows checkout.
"""
import hashlib, io, os

HERE = os.path.dirname(os.path.abspath(__file__))
SKIP_DIRS = {"aer1", "__pycache__", ".git"}
SKIP_FILES = {"SHA256SUMS", "SHA256SUMS.ots", "parity-report.json", "mutation-report.json"}
SKIP_EXT = {".pyc"}

entries = []
for root, dirs, files in os.walk(HERE):
    dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS)
    for name in sorted(files):
        if name in SKIP_FILES or os.path.splitext(name)[1] in SKIP_EXT:
            continue
        path = os.path.join(root, name)
        rel = os.path.relpath(path, HERE).replace(os.sep, "/")
        with open(path, "rb") as fh:
            digest = hashlib.sha256(fh.read()).hexdigest()
        entries.append("%s  %s" % (digest, rel))

entries.sort(key=lambda line: line.split("  ", 1)[1])
with io.open(os.path.join(HERE, "SHA256SUMS"), "w", encoding="utf-8", newline="\n") as fh:
    fh.write("\n".join(entries) + "\n")
print("SHA256SUMS: %d files" % len(entries))
print("includes policy_digest.py:", any(e.endswith(" policy_digest.py") for e in entries))
