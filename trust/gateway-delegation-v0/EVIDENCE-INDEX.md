# Evidence index

One page for a reader who wants to check this package without reading the whole
tree. Every row points at the artifact that carries the claim, and at what a
reader can run to reproduce it. Claims that are **not** established are listed
under "What this package does not establish", not softened into the rows above.

Reviewed commit: `3b683a1d38440dbfa6ab54328df42a5ac4083bd1` (the head of this PR).
The earlier reviewed commit `bf2f149` remains reachable on the same branch; the
facts below are stated for `3b683a1` unless noted.

| Claim | Carrier | How a reader checks it |
|---|---|---|
| 122 rows (18 cases + 104 vectors), each with a stated expected outcome | `expected.json`, `fixtures/vectors/`, `CONFORMANCE.md` | `python3 check.py --selftest` |
| Our two implementations agree on every row | `crosscheck.py`, `parity-report.json` | `python3 crosscheck.py --json /tmp/p.json` → `disagreements: 0` |
| The policy did not drift while the package changed | `policy.json`, `policy_digest.py` | `python3 policy_digest.py --check` |
| Shipped bytes are pinned | `SHA256SUMS` (152 lines) | `sha256sum -c SHA256SUMS` |
| The manifest came from this key | `SHA256SUMS.sig`, `allowed_signers` | `ssh-keygen -Y verify -f allowed_signers -I zhaoxinghua09-cell -n file -s SHA256SUMS.sig < SHA256SUMS` |
| The vector set is versioned as a unit | `fixtures/vectors/vectors-v1.manifest`, `check_vectors_manifest.py` | `python3 check_vectors_manifest.py` |
| Mutation coverage, first implementation | `mutation-report.json` | `python3 mutation_check.py` — 37 sites, 37 killed, 0 survived; the 12 declared operator classes are reconciled in `operator-coverage.json` |
| Operator class coverage | `operator-coverage.json`, `operator_coverage.py` | `python3 operator_coverage.py` — 12 declared, 9 covered (all killed), 3 absent by construction (`<=`, `true`, `false` occur 0 times), 0 gap |
| Mutation coverage, second implementation | `mutation-cross-report.json`, `mutation_check_cross.py` | `python3 mutation_check_cross.py` — 40 sites, **28 killed, 0 survived**, 8 invalid, 4 error (the two survivors reported earlier disappeared once the oracle compared per-check results, not just the verdict) |
| Every check that runs reaches its rejecting path | `exercise-matrix.json`, `exercise_matrix.py` | `python3 exercise_matrix.py` — 10 checks, 0 unexercised, 9 with sole-cause rows; the exception is stated rather than hidden: `receipt` only evaluates on `refuse` rows (56 of them, 8 pass / 48 non-pass) and the script exits 1 if it ever runs on an `allow` row |
| The suite runs on every push | `.github/workflows/conformance.yml` (8 jobs) | fork Actions run for `3b683a1`: all 7 completed/success at `3b683a1` (8 jobs from the exercise-matrix commit onward) |

## Outside runs on record

| Date | Who | Head | Result | Record |
|---|---|---|---|---|
| 2026-11-27 | `zambodotdev` (no role in this repository) | `365a052` | 143/143 `sha256sum -c`, `check.py` 122 rows, `crosscheck` 0 divergences | PR #43 comment `#issuecomment-7230440157` |
| 2026-11-28 | `zambodotdev` | `3b683a1` | 149/149 `sha256sum -c`; **signature verify: Good**; policy digest unchanged; 122 rows same distribution; mutation 35/35 and 40 (26 killed, 2 survived — the then-current oracle) reproduced site for site; 7 CI jobs success | PR #43 comment `#issuecomment-7238629003` |

These are third-party **reruns of our two implementations**, not entries
produced by an independent implementation. The conformance intake table in
`CONFORMANCE.md` is still empty, and that empty row is the honest state.

## What this package does not establish

- **No independent implementation has produced a row.** `CONFORMANCE.md` §"What
  to send" is the intake; until someone fills it, parity is with our two
  implementations only.
- **The signature is self-asserted.** It binds the manifest to
  `zhaoxinghua09-cell`; there is no outside identity, no transparency log, and
  no endorsement. A verifier confirms "this key produced this manifest", nothing
  more.
- **`SHA256SUMS.ots` is still pending.** Four calendars accepted it; no Bitcoin
  block-header attestation exists yet, so `ots verify` exits non-zero by design
  at this stage.
- **Mutation survivors are real.** Both live sites are one line in `check.mjs`
  (the receipt condition on decision, caseId and policyDigest): the judge does
  not compare per-field sub-checks, so a defect there survives. Recorded, not
  averaged away.
- **The CI recompute is ours.** Seven green jobs on our fork are evidence that
  the suite runs unattended, not that a second organisation recomputed it.

