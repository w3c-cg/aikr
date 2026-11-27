#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_vectors_manifest.py — 让外人用一条命令复现"这套向量是不是 v1 那一套"。

做三件事，任何一件不成立就退出码 1：
  1. 按 manifest 里的路径重算每个向量的 sha256，与 manifest 记录比；
  2. 用 manifest 声明的规则重算 root，与 manifest 记录比；
  3. 与仓内已冻结的 SHA256SUMS 比（向量行必须逐条一致）。

用法：
  python check_vectors_manifest.py            # 默认读 fixtures/vectors/vectors-v1.manifest
  python check_vectors_manifest.py --manifest fixtures/vectors/vectors-v1.manifest
只读本目录，不联网，不写文件。
"""
import argparse
import hashlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT = "fixtures/vectors/vectors-v1.manifest"


def sha256_of(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def main():
    ap = argparse.ArgumentParser(description="Verify the vector-set manifest against disk and SHA256SUMS")
    ap.add_argument("--manifest", default=DEFAULT)
    args = ap.parse_args()

    mpath = os.path.join(HERE, args.manifest)
    with open(mpath, encoding="utf-8") as fh:
        man = json.load(fh)

    fails = []
    # 1. per-file
    missing, mismatch = [], []
    for r in man["files"]:
        p = os.path.join(HERE, r["path"])
        if not os.path.exists(p):
            missing.append(r["path"])
            continue
        if sha256_of(p) != r["sha256"]:
            mismatch.append(r["path"])
    if missing:
        fails.append("missing files: %s" % ", ".join(missing[:5]))
    if mismatch:
        fails.append("sha256 mismatch: %s" % ", ".join(mismatch[:5]))

    # 2. root
    rows = sorted(man["files"], key=lambda r: r["path"])
    root = hashlib.sha256("".join(r["sha256"] + "  " + r["path"] + "\n" for r in rows).encode()).hexdigest()
    if root != man["root"]:
        fails.append("root recomputed %s != declared %s" % (root[:16], man["root"][:16]))

    # 3. frozen sums
    sums_path = os.path.join(HERE, "SHA256SUMS")
    frozen = {}
    if os.path.exists(sums_path):
        with open(sums_path, encoding="utf-8", errors="ignore") as fh:
            for line in fh:
                m = re.match(r"^([0-9a-f]{64})\s+\*?(.+)$", line.strip())
                if m:
                    frozen[m.group(2).strip()] = m.group(1)
        sums_diff = [r["path"] for r in man["files"]
                     if r["path"] in frozen and frozen[r["path"]] != r["sha256"]]
        sums_absent = [r["path"] for r in man["files"] if r["path"] not in frozen]
        if sums_diff:
            fails.append("differs from SHA256SUMS: %s" % ", ".join(sums_diff[:5]))
        if sums_absent:
            fails.append("not pinned in SHA256SUMS: %s" % ", ".join(sums_absent[:5]))

    print("manifest: %s  id=%s  vectors=%d  root=%s" % (
        args.manifest, man.get("id"), len(man["files"]), man["root"][:16]))
    if fails:
        for f in fails:
            print("FAIL %s" % f)
        print("RESULT: FAIL")
        return 1
    print("RESULT: PASS (files, root and SHA256SUMS all agree)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
