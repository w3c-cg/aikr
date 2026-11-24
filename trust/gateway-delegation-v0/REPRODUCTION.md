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
python check.py            # table of 18 rows, exit 0
python check.py --selftest # six [OK] lines, exit 0
```

Observed on the run above:

```
18 cases: could-not-determine 8, fail 9, pass 1

[OK] expected.json matches the checker on 18 cases
[OK] a permissive checker (content ignored, unknown folded into pass) is caught on 13 cases:
     D03, D05, D06, D07, D08, D10, D11, D12, D13, D14, D15, D17, D18
[OK] tamper test: D02 with an in-grant scope now gives pass (was fail)
[OK] bound test: 24h -> 25h changes 1 case(s) (D13)
[OK] receipt test: D16 refused without a receipt; adding one clears the receipt check
[OK] lineage test: D18 with the cited digest added to the chain no longer holds as unresolved
```

Exit codes: `0` when the run and the selftest agree; the selftest returns `1`
if any expectation is missed.

## The six selftest claims, stated so they can be falsified

1. **Expectation match** — every row of `expected.json` equals the checker's
   result and first code, on all 18 cases.
2. **Permissive checker is caught** — a checker that ignores content, folds
   `could-not-determine` into `pass`, ignores staleness and never reads the
   signer key or the lineage disagrees on 13 of 18 cases. If a future edit drops
   that below 5, the selftest fails.
3. **Tamper moves the result** — D02 with an in-grant scope becomes `pass`,
   which proves the table is computed from fixtures, not asserted in prose.
4. **Bound is not silently widened** — raising `revocationFreshnessBoundSeconds`
   from 86400 to 90000 flips D13 from `could-not-determine` to `pass`. A policy
   that loosens the bound without saying so becomes visible in one command.
5. **The receipt requirement is live** — D16 is a refusal with no receipt; adding
   a receipt that binds the decision, the case id and the policy digest clears the
   receipt check. If the requirement is deleted from `check.py`, this item fails.
6. **A citation must be walked** — D18 cites a digest outside its chain; adding
   that digest to the chain clears the unresolved verdict. A gateway that accepts
   a non-empty citation without walking it is caught by the same row.

## Cross-machine check

**Status: pending for this revision.** The 15-case version of this package was
run on a second machine (Ubuntu 22.04, CPython 3.12.11) in a clean directory
cloned over the public network with no credentials, and matched (`7/7/1`, four
`[OK]` lines). The 18-case revision has so far been run only on the Windows
machine above; the Linux re-run is recorded here once it has actually been
executed, not before. Until that line is replaced, treat the cross-machine claim
as **not established for this revision**. If your run differs, the useful report
is the row that differs and your interpreter version — that is the kind of
disagreement this set exists to surface.

## Integrity

`SHA256SUMS` carries a digest for every file here except itself, so what you run
is what was reviewed:

```
sha256sum -c SHA256SUMS     # or: shasum -a 256 -c SHA256SUMS
```

Every file is LF line endings (`.gitattributes` enforces it on checkout).
`expected.json` and the fixtures are UTF-8 without a BOM.

## What this does not establish

A pass here means "no violation detected within the declared inputs", not
"the action is safe". The set is synthetic: it does not exercise cryptographic
correctness, network identity, multi-hop delegation chains, concurrency, or the
truth of anything a record points at. It cannot tell you whether a given gateway
implementation is correct — only whether it behaves like this table on these
inputs.
