# -*- coding: utf-8 -*-
"""Rebuild SHA256SUMS: one line per shipped file, lowercase sha256, posix path.

Excluded: SHA256SUMS itself, and the AER-1 fetch cache (aer1/), which is
third-party bytes fetched at build time and never shipped.
"""
import hashlib, io, os

HERE = r"D:\Workbuddy\_aikr_fork\trust\gateway-delegation-v0"
SKIP_DIRS = {"aer1", "__pycache__", ".git"}
SKIP_FILES = {"SHA256SUMS"}
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
