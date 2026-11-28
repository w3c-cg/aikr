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
**37 candidate sites** in `check.py` are used, not a sample: **37 killed, 0
survived, 0 invalid** (`mutation-report.json` carries the per-operator tally).

The scan region now starts at the module constants, not at `check_case`: a
`"pass"` written as `"fail"` in the constant block is the most ordinary defect
this suite must catch, and a scan that begins below it can never report it.

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
about the suite's strength.

Per class, so that a reader can see what a 100% is a 100% *of*. The harness
declares 12 operator classes; the decision code gives a site to 7 of them and
`sites 0` to the other 5 — those five are listed rather than dropped, because
"12 classes, all killed" and "7 classes, all killed, 5 unmeasured" are different
claims:

| Class | Sites in the decision code | Killed |
|---|---|---|
| `eq-flip` (`==`→`!=`) | 15 | 15/15 |
| `ne-flip` (`!=`→`==`) | 1 | 1/1 |
| `ge-to-gt` (`>=`→`>`) | 1 | 1/1 |
| `gt-to-ge` (`>`→`>=`) | 1 | 1/1 |
| `lt-to-le` (`<`→`<=`) | 2 | 2/2 |
| `and-to-or` | 6 | 6/6 |
| `or-to-and` | 9 | 9/9 |
| `le-to-lt`, `true-to-false`, `false-to-true`, `pass-to-fail`, `fail-to-pass` | 0 each | not measured |

`check.py`'s decision region contains no `<=`, no `True`/`False` literal and no
`"pass"`/`"fail"` literal to mutate, so five of the twelve declared classes have
nothing to bite on. Widening the region would not help: the tokens are absent
from the whole file's decision paths, not merely outside the current window. The
gap is real and it is filed as a gap, not as coverage.

What it still does **not** cover:

- only operator-level defects inside `check.py`; no scenario-level or
  fixture-level mutations, and the expected values are never mutated;
- one defect at a time; no combined or adversarial sequences;
- the four inline assertions name reason codes (`POINTER_UNREACHABLE`,
  `NO_DECLARED_SCOPE`, `WINDOW_UNPARSABLE`) as literals: if those names ever
  change meaning, the assertions misfire rather than stay silent. That is the
  trade taken deliberately — a named code is stronger than "the bucket is
  non-empty" — and an external review flagged it as the one place to document.

The corpus stayed at 122 rows. No row was added to chase a mutant score.

### Cross-implementation mutation (the other direction)

`check.py` mutating itself only answers "can our corpus catch our checker".
`mutation_check_cross.py` asks the other question: **can the two implementations
catch each other?** It injects one defect at a time into `checkCase` in
`check.mjs` and runs `crosscheck.py`; a disagreement counts as caught.

- 40 candidate sites in `check.mjs`: **28 caught, 0 survived, 8 invalid
  (syntax), 4 error** (`mutation-cross-report.json`; score 100% of the 28
  scoreable mutants).
- The two sites that survived in the previous revision sit on one JavaScript
  line — the receipt condition
  `receipt.decision === "refuse" && receipt.caseId === c.id && receipt.policyDigest === policy.policyDigest`.
  They survived **because the oracle was too coarse**, not because the defect
  was harmless: a receipt-branch change cannot move the verdict or the first
  code when another check has already failed.
- That gap is now closed. `check.mjs` emits its per-check list, and
  `crosscheck.py` compares it field by field (`check`, `result`, `code`) in
  addition to the verdict, the first code and the hold group. Both mutants are
  killed under that oracle, and the 122 rows still agree per check (0
  disagreements), so the tightening cost nothing in parity.
- Twelve operator classes are declared. Nine of them have at least one site
  here and every one of those sites is killed. The other three — `<=` (`le-to-lt`),
  `true` (`true-to-false`) and `false` (`false-to-true`) — do not occur in the
  decision code of either implementation at all; `operator_coverage.py` proves
  that by counting occurrences rather than asserting it in prose
  (`operator-coverage.json`: 12 declared, 9 covered, 3 absent, 0 gap). A class
  that occurs without a site, or keeps a survivor, is a GAP and exits 1.
- Zero survivors still does not mean full coverage of *behaviour*: this is
  operator-level mutation of two checkers, not scenario-level testing.
- "error" rows are mutants where the mutated JS throws: `crosscheck.py` fails
  loudly, so the drift is noticed, but it is counted separately rather than
  scored as a clean catch.

### Did the rejecting path ever run?

A conformance row that says "pass" is worth nothing if the check could not have
said anything else. `exercise_matrix.py` answers that for every check in
`check.py`: for each of the 122 rows it records which checks passed and which
did not, so a check with zero non-pass observations is visible as
**implemented-but-unexercised** rather than hidden behind a green row
(`exercise-matrix.json`).

- All ten checks that appear in the corpus reach their rejecting outcome at
  least once: 0 unexercised. Non-pass counts range from 6 (`evidence`,
  `signer-binding`) to 48 (`receipt`).
- Nine checks also reject as the **sole** cause of a row (a row where it is
  the only non-pass check), which is what makes the rejection attributable to
  that check rather than to a neighbour: `attenuation` 4, `content` 5,
  `evidence` 4, `lineage` 4, `revocation` 16, `signature` 1,
  `signer-binding` 1, `subject` 1, `window` 4.
- `receipt` is the exception, and structurally so: it is a conditional check
  evaluated only on rows whose decision is `refuse`, so it can never be the
  sole cause — the row already failed elsewhere. Its domain is stated and
  checked instead: 56 rows evaluate it, none of them on an `allow` decision
  (the script exits non-zero if that ever changes), and inside that domain it
  records 8 pass / 48 non-pass.
- This metric is taken from `draft-he-agentproto-verifier-evidence` (EXR-1 /
  CMP-1). Their vectors were **not** run here; only the reporting discipline was
  adopted.
- Exercised is not the same as *discriminating*: this table has no pre-declared
  counterfactual population per check, and it is bounded by this corpus. A
  new vector can change a count.

## Timestamps and signature

`SHA256SUMS` (152 shipped files) carries two independent attestations:

- `SHA256SUMS.sig` — an SSH signature over the manifest, verifiable with
  `allowed_signers` in this directory and a stock `ssh-keygen`. It binds the
  list to the maintainer key that pushes to this branch. It is *self-issued*:
  there is no external identity attestation behind it.
- `SHA256SUMS.ots` — an OpenTimestamps proof. Four public calendars accepted the
  commitment and the attestation is **pending confirmation in the Bitcoin
  blockchain** at the time of writing. `ots info SHA256SUMS.ots` shows the proof;
  `ots upgrade` completes it once a block includes it.

So the chain is: signature says who; timestamp says when; the manifest says
which bytes. None of the three says a third party validated anything.

## Why there is no "certified" wording anywhere in this file

A conformance suite can say what it tested and what it did not. It cannot
certify an implementation, and this one does not: the five states exist
precisely so that "we could not tell" is not reported as "pass".
