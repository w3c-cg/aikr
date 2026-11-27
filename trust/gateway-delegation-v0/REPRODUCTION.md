# Reproduction — how to check this package yourself

Short version: clone, change into this directory, run `python check.py --selftest`.
Exit 0 means the table in `expected.json` was reproduced and the set caught the
defects it claims to catch. Nothing here needs credentials, a network, or an
account.

## What was run

| | |
|---|---|
| Package path | `trust/gateway-delegation-v0/` |
| Commit | see the parent commit of the file edits; the content is immutable at that commit |
| Interpreter | CPython 3.13.18 (Windows, MSC v.1944, 64-bit) — this run |
| Dependencies | none beyond the standard library (`argparse`, `datetime`, `glob`, `json`, `os`, `sys`) |
| Network | not used |
| Evaluated instant | `2026-11-23T00:00:00Z` (pinned in `policy.json`) |

## Commands and what they should print

```
cd trust/gateway-delegation-v0
python check.py            # 122 rows (18 curated + 104 vectors), exit 0
python check.py --selftest # nine [OK] lines, exit 0
node check.mjs             # the same 122 rows from the second implementation
python crosscheck.py       # both implementations, exit 0 when they agree
python policy_digest.py --check  # digest recomputed from policy.json, exit 0
```

Observed on the run above:

```
122 cases: absent 3, check-incomplete 6, fail 56, pass 33, record-unresolved 24

[OK] expected.json matches the checker on 18 cases
[OK] a permissive checker (content ignored, unknown folded into pass) is caught on 13 cases:
     D03, D05, D06, D07, D08, D10, D11, D12, D13, D14, D15, D17, D18
[OK] tamper test: D02 with an in-grant scope now gives pass (was fail)
[OK] bound test: 24h -> 25h changes 1 case(s) (D13)
[OK] receipt test: D16 refused without a receipt; adding one clears the receipt check
[OK] lineage test: D18 with the cited digest added to the chain no longer holds as unresolved
[OK] policy digest: recomputed from policy.json, matches the stored value
[OK] split test: record-only -> record-unresolved, checker-only -> check-incomplete,
     absent-only -> absent, mixed -> record-unresolved with
     POINTER_UNREACHABLE/NO_DECLARED_SCOPE/WINDOW_UNPARSABLE
[OK] vector set: 104 rows match their stated expectations (0 mismatches)
      distribution: pass 32 / record-unresolved 18 / absent 2 / check-incomplete 5 / fail 47

rows compared: 122 (curated 18 + vectors 104)
disagreements: 0
```

Exit codes: `0` when the run and the selftest agree; the selftest returns `1`
if any expectation is missed.

## The nine selftest claims, stated so they can be falsified

1. **Expectation match** — every row of `expected.json` equals the checker's
   result and first code, on all 18 cases.
2. **Permissive checker is caught** — a checker that ignores content, folds
   both kinds of hold into `pass`, ignores staleness and never reads the
   signer key or the lineage disagrees on 13 of 18 cases. If a future edit drops
   that below 5, the selftest fails.
3. **Tamper moves the result** — D02 with an in-grant scope becomes `pass`,
   which proves the table is computed from fixtures, not asserted in prose.
4. **Bound is not silently widened** — raising `revocationFreshnessBoundSeconds`
   from 86400 to 90000 flips D13 from `record-unresolved` to `pass`. A policy
   that loosens the bound without saying so becomes visible in one command.
5. **The receipt requirement is live** — D16 is a refusal with no receipt; adding
   a receipt that binds the decision, the case id and the policy digest clears the
   receipt check. If the requirement is deleted from `check.py`, this item fails.
6. **A citation must be walked** — D18 cites a digest outside its chain; adding
   that digest to the chain clears the unresolved verdict. A gateway that accepts
   a non-empty citation without walking it is caught by the same row.
7. **The policy digest is reproducible** — the digest in `policy.json` is
   recomputed from the file's own bytes (with the digest field blanked) and must
   equal the stored value. A receipt that binds to a digest nobody can regenerate
   from the file would fail here.
8. **A hold names its side** — three cases built from D01 in memory: record-only
   (unreachable evidence pointer) gives `record-unresolved`; checker-only
   (unparsable mandate window) gives `check-incomplete`; undeclared-scope-only
   gives `absent`; all three together give `record-unresolved` *and* fill
   `unknown.record`, `unknown.absent` and `unknown.checker`.
   If the split is folded back into one bucket, this item fails.
9. **The vector set matches what it states** — 104 vectors carry their own
   `expect` block, written with the vector rather than derived from a run. If any
   row disagrees the selftest fails; a set that merely reprints the checker's own
   output would pass this item for the wrong reason.

## Cross-machine check

Run on a second machine and network path: Ubuntu, CPython 3.12.11, Node 22.23.4,
in a clean directory cloned over the public network with no credentials
(`git clone -q --branch gateway-delegation-v0 --single-branch
https://github.com/zhaoxinghua09-cell/aikr.git`), at commit `8d9dc45` and again at
`6fb9a91` after the fourth state was added. The `6fb9a91` figures are the current
ones; the `8d9dc45` figures are kept below because they are what that commit printed.

```
# at 6fb9a91
python3 check.py            -> 122 rows, exit 0
  122 cases: absent 3, check-incomplete 6, fail 56, pass 33, record-unresolved 24
python3 check.py --selftest -> nine [OK] lines plus the distribution line, exit 0
     [OK] split test: record-only -> record-unresolved, checker-only -> check-incomplete,
          absent-only -> absent, mixed -> record-unresolved with
          POINTER_UNREACHABLE/NO_DECLARED_SCOPE/WINDOW_UNPARSABLE
python3 crosscheck.py       -> rows compared: 122, disagreements: 0, exit 0
sha256sum -c SHA256SUMS     -> 144 files, all OK

# at 8d9dc45, for comparison
python3 check.py            -> 122 rows, exit 0
  122 cases: check-incomplete 9, fail 56, pass 33, record-unresolved 24
python3 check.py --selftest -> nine [OK] lines, exit 0
  [OK] policy digest: recomputed from policy.json, matches the stored value
  [OK] split test: record-only -> record-unresolved, checker-only -> check-incomplete, ...
  [OK] vector set: 104 rows match their stated expectations (0 mismatches)
python3 crosscheck.py       -> rows compared: 122, disagreements: 0, exit 0
sha256sum -c SHA256SUMS     -> 143 files, 0 mismatches
```

Every row matched the Windows run, and both implementations agreed on all 122
rows on a third platform-independent pair of interpreters (CPython here, Node
there). An earlier Linux attempt on the 18-case revision failed at
`sha256sum -c` only because the manifest carried Windows backslash paths; it now
uses `/` and passes on both. That is recorded rather than quietly fixed. If your
run differs, the useful report is the row that differs and your interpreter
version — that is the kind of disagreement this set exists to surface.

## Integrity

`SHA256SUMS` carries a digest for every file here except itself, so what you run
is what was reviewed:

```
sha256sum -c SHA256SUMS     # or: shasum -a 256 -c SHA256SUMS
```

Every file is LF line endings (`.gitattributes` enforces it on checkout).
`expected.json` and the fixtures are UTF-8 without a BOM.

The manifest itself is timestamped: `SHA256SUMS.ots` is an OpenTimestamps proof
committing to `SHA256SUMS` (146 files). While the attestation is still pending
in Bitcoin, `ots info SHA256SUMS.ots` shows the four calendar attestations and
**`ots verify` exits non-zero by design** — it reports "pending", not "invalid".
Once a block includes it, `ots upgrade SHA256SUMS.ots` completes the proof and
then:

```
ots verify SHA256SUMS.ots      # exit 0 only when the Bitcoin header is attached
sha256sum -c SHA256SUMS        # and the files are the ones the list pins
```

A pending proof is still useful: four independent calendars accepted the same
commitment at the same time, which is a public record that the list existed
then. It is not, yet, a Bitcoin-anchored one, and this file says so rather than
calling it verified.

## What this does not establish

A pass here means "no violation detected within the declared inputs", not
"the action is safe". The set is synthetic: it does not exercise cryptographic
correctness, network identity, multi-hop delegation chains, concurrency, or the
truth of anything a record points at. It cannot tell you whether a given gateway
implementation is correct — only whether it behaves like this table on these
inputs.
