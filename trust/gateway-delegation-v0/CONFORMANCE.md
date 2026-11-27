# Conformance: how to be recorded here

This file is the intake for anyone outside this repository who wants to run
`gateway-delegation-v0` against their own implementation and be recorded. Right
now **the table below is empty**: no third party has run it, and an empty table
is the honest state, not a placeholder to be filled with our own runs.

## What the set is

122 rows: 18 curated cases (`D01`–`D18`) and 104 generated vectors. Every row
states the outcome it must produce: `pass`, `fail`, `record-unresolved`, `absent`,
`check-incomplete`, with a reason code where one applies. The expected outcomes
were written with the rows, not derived by running a checker; that is what makes
a disagreement informative.

## What you need to run

```
python3 check.py --selftest                 # your checker against the stated expectations
node --version                              # only if you also run the JS side
python3 policy_digest.py --check            # the receipt digest must not drift
sha256sum -c SHA256SUMS                     # shipped bytes unchanged
```

To claim parity with our two implementations rather than only with the corpus:

```
python3 crosscheck.py --json parity-report.json
```

`parity-report.json` carries one row per case, both verdicts, and the sha256 of
`check.py`, `check.mjs`, `policy.json`, `expected.json`, so a reader can tell
which pair of checkers produced it.

## What to send to be added to the table

A single file (markdown or JSON) with:

1. **Identity** — who ran it: person or organisation, and whether you are a
   maintainer of this repository (maintainers' runs are self-runs, and get
   labelled as such).
2. **Environment** — OS, kernel or version string, Python version, Node version,
   and the commit sha of this repository you used.
3. **Command lines** — the exact commands, copied from your shell, not
   paraphrased.
4. **Result** — exit code of `check.py --selftest`, number of rows matched,
   number of mismatches, and for each mismatch the row id plus your verdict and
   code.
5. **Divergences** — if your implementation disagrees with the stated
   expectation, say which reading of the policy produced it. A disagreement is
   not automatically your error or ours; it is a finding, and it is recorded as
   one.
6. **What you did not run** — the parts you skipped, stated plainly.

Send it as an issue or a pull request that adds one row to the table below. We
record the row as submitted; we do not upgrade anyone's wording, and we do not
list runs we cannot trace to a command line.

## The table

| Date | Who | Environment | Rows matched | Mismatches | Recorded as |
|---|---|---|---|---|---|
| — | — | — | — | — | *no third-party run on record yet* |

"Recorded as" takes one of: `third-party` (someone with no role in this
repository), `self-run` (a maintainer or the author), `machine` (an automated
system whose owner is not independent).

## Known gaps, as of 2026-11-28

Mutation testing (`mutation_check.py`) injects one defect at a time into the
decision code and runs `check.py --selftest` with expectations untouched. All
**35 candidate sites** in `check.py` are used, not a sample: **35 killed, 0
survived, 0 invalid** (`mutation-report.json` carries the per-operator tally).

Getting there changed the harness, not the corpus. The first pass (25 sampled
mutants) left two alive, and expanding to every candidate site left four more.
All six were holes in *this repository's own assertions*, not in the rows:

| Mutant | Where | Why it lived | Assertion now in `selftest()` |
|---|---|---|---|
| `!=` → `==` | `permissive_check`, subject | no row makes the defect checker reject a row the real checker passes, so flipping it was invisible | a row the real checker passes must also pass the permissive one |
| `and` → `or` | `check_case`, receipt caseId | the receipt check only runs after something else already failed, so the case verdict is identical either way | a receipt naming another case must leave the receipt check `fail` |
| `or` → `and` | `permissive_check`, revocation | a revoked row fails on the real checker anyway, so the disagreement count stayed healthy | the permissive checker must still refuse a revoked row |
| `==` → `!=` ×3 | `run()`, the three `unknown` buckets | the split test built its own buckets and never inspected the row `run()` hands out | each hold must be filed in exactly one bucket, checked on the emitted row |

So the score is 100% of 35, and that is a statement about the assertions, not
about the suite's strength. What it still does **not** cover:

- only operator-level defects inside `check.py`; no scenario-level, fixture-level
  or cross-implementation mutations, and no mutations of `check.mjs`;
- one defect at a time; no combined or adversarial sequences;
- the expected values themselves are never mutated (deliberately — see
  `VECTORS.md`), so a wrong-but-consistent expectation is out of scope for this
  measure.

The corpus stayed at 122 rows. No row was added to chase a mutant score.

## Timestamps

`SHA256SUMS` (146 shipped files) carries an OpenTimestamps proof in
`SHA256SUMS.ots`: four public calendars accepted the commitment, and the
attestation is **pending confirmation in the Bitcoin blockchain** at the time
of writing. `ots info SHA256SUMS.ots` shows the proof; `ots upgrade` completes
it once a block includes it. The proof commits to the list, and the list is
what pins the files, so the chain is: block → `SHA256SUMS` → each file.

## Why there is no "certified" wording anywhere in this file

A conformance suite can say what it tested and what it did not. It cannot
certify an implementation, and this one does not: the five states exist
precisely so that "we could not tell" is not reported as "pass".
