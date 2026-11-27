# Conformance: how to be recorded here

This file is the intake for anyone outside this repository who wants to run
`gateway-delegation-v0` against their own implementation and be recorded. Right
now **the table below is empty**: no third party has run it, and an empty table
is the honest state, not a placeholder to be filled with our own runs.

## What the set is

122 rows: 18 curated cases (`D01`–`D14`, plus the four rows added when `absent`
became a state) and 104 generated vectors. Every row states the outcome it must
produce: `pass`, `fail`, `record-unresolved`, `absent`, `check-incomplete`, with
a reason code where one applies. The expected outcomes were written with the
rows, not derived by running a checker; that is what makes a disagreement
informative.

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

Mutation testing (`mutation_check.py`, 25 mutants injected into the decision
code, expectations untouched) kills 23 and leaves 2 alive:

| Mutant | Line | What survives |
|---|---|---|
| `!=` → `==` | `check_case`, subject binding | no row distinguishes a flipped subject check from the correct one — another check catches the same case first, so the corpus never exercises this branch alone |
| `and` → `or` | `check_case`, receipt binding | no row carries a receipt issued for a **different** case, so weakening the case-id binding changes nothing |

Both are real gaps, and both would add rows (122 → 124) plus new expectations,
a new crosswalk entry and a new `SHA256SUMS`. They are left for the next corpus
version rather than folded in silently, because every number in this repository
(122 rows; 146 shipped files, was 143 before `CONFORMANCE.md`, `mutation_check.py`
and the regenerated `make_sums.py` were added) is quoted elsewhere.

## Why there is no "certified" wording anywhere in this file

A conformance suite can say what it tested and what it did not. It cannot
certify an implementation, and this one does not: the five states exist
precisely so that "we could not tell" is not reported as "pass".
