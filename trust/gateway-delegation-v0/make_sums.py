# -*- coding: utf-8 -*-
"""Rebuild or check SHA256SUMS: one line per shipped file, lowercase sha256, posix path.

Excluded: SHA256SUMS itself, and the AER-1 fetch cache (aer1/), which is
third-party bytes fetched at build time and never shipped.

    python make_sums.py           regenerate the manifest from what is on disk
    python make_sums.py --check   verify the manifest against what is on disk

The default run rebuilds the list from the tree, so a line cannot outlive the file
it names. The --check run reports, per line, whether the file exists and whether
its digest still matches, and exits 1 when it finds either problem - which is the
drift that left a stale policy.json.bak line in the manifest before.
"""
import hashlib, io, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SKIP_DIRS = {"aer1", "__pycache__", ".git"}
SKIP_FILES = {"SHA256SUMS"}
SKIP_EXT = {".pyc"}
MANIFEST = os.path.join(HERE, "SHA256SUMS")


def walk_entries():
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
    return entries


def check():
    with io.open(MANIFEST, encoding="utf-8") as fh:
        lines = [l for l in fh.read().splitlines() if l.strip()]
    missing, mismatched, ok = [], [], 0
    for line in lines:
        digest, rel = line.split("  ", 1)
        path = os.path.join(HERE, rel)
        if not os.path.exists(path):
            missing.append(rel)
            continue
        with open(path, "rb") as fh:
            if hashlib.sha256(fh.read()).hexdigest() != digest:
                mismatched.append(rel)
            else:
                ok += 1
    print("SHA256SUMS: %d lines, %d match, %d mismatched, %d missing on disk"
          % (len(lines), ok, len(mismatched), len(missing)))
    for name in missing:
        print("  missing: %s" % name)
    for name in mismatched:
        print("  mismatched: %s" % name)
    return 1 if (missing or mismatched) else 0


if "--check" in sys.argv[1:]:
    sys.exit(check())

entries = walk_entries()
with io.open(MANIFEST, "w", encoding="utf-8", newline="\n") as fh:
    fh.write("\n".join(entries) + "\n")
print("SHA256SUMS: %d files" % len(entries))
print("includes policy_digest.py:", any(e.endswith(" policy_digest.py") for e in entries))
