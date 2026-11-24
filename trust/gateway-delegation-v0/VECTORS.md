# The vector set

102 machine-readable vectors, generated from the grid below and kept in
`fixtures/vectors/`. Each vector states the outcome it must produce:

```json
"expect": { "result": "could-not-determine", "code": "LINEAGE_UNRESOLVED" }
```

The expectations were **not** produced by running `check.py`. They were written
with the vector and then checked against both implementations. A disagreement
fails `check.py --selftest` and `crosscheck.py`, so a checker that drifts cannot
rewrite its own verdicts.

## Why both curated cases and vectors

The 18 curated cases in `fixtures/cases/` are the ones with names and prose
(D01–D18) — they exist to be read. The vectors exist to be *run* in volume: they
walk the parameter space around each invariant so that an implementation cannot
pass by handling one shape per class.

## Grid

| Invariant | Vectors | What the parameters walk |
|---|---|---|
| I1 subject binding | 8 | equal, other agent, case variation, absent id, empty id, missing mandate subject, peer-ahead-of-id, relay peer |
| I2 validity window | 16 | inside, both boundaries, one second either side, inverted window, unparsable ends, naive and offset timestamps, zero-length window, distant window |
| I3 signature result | 6 | ok, bad, empty, null, boolean, capitalised |
| I4 attenuation | 12 | subset, equal, one and two extras, empty grant, empty declaration, absent declaration, duplicates, case variation |
| I5 content mediation | 8 | clean, instruction, role claim, opaque, opaque plus instruction, absent payload, empty carriers |
| I6 revocation freshness | 16 | fresh, at the bound, one second past, 25 hours, revoked, unreachable, unknown status, absent status, absent check time, future check time |
| I7 revocation effect timing | 7 | effect in the future (1 s, 1 h, distant), effective now, effective past, unparsable effect, effect at issue time |
| I8 evidence pointer | 4 | reachable, unreachable, absent, value outside the known set |
| I9 signer key binding | 4 | equal, other key, only one fingerprint declared, neither declared |
| I10 lineage | 5 | no citation, resolved, unresolved, empty chain, null citation |
| I11 receipt on refusal | 6 | allow (not applicable), bound receipt, no receipt, receipt for another policy, for another case, for another decision |
| I1–I11 combinations | 10 | two defects in one request, to pin the published check order and that fail outranks could-not-determine |

Distribution: **pass 30 · could-not-determine 25 · fail 47**. The asymmetry is
deliberate — a set that mostly returns pass would not tell implementations apart.

## Running them

```
python check.py --vectors          # the vector table alone
python check.py                    # curated cases plus vectors, 120 rows
python check.py --selftest         # includes "vector set matches its stated expectations"
node check.mjs                     # the same 120 rows from the JavaScript implementation
python crosscheck.py               # both implementations, row by row; exit 1 on any disagreement
```

## What a vector does not prove

A vector fixes inputs and an expected verdict under this policy. It says nothing
about cryptographic correctness, network identity, or the truth of any record.
An implementation can pass all 102 and still be wrong about something this set
does not describe; the set is a floor, not a certificate.
