# Notes for an independent reviewer

This file exists so that a reviewer — a person, or a model that did not write
this package — can start from what is claimed and what would falsify it, rather
than from the README's own account of itself.

## What you are being asked

Do not check whether the prose is well written. Check whether the claims hold
when you run the thing yourself, and say where they do not.

## Claims, and how to break each one

| Claim | How to falsify it |
|---|---|
| The checker reproduces `expected.json` on the 18 curated cases | Edit one fixture's inputs, run `python check.py --selftest`; if the expectation still passes, the table is asserted rather than computed |
| All 102 vectors match the outcomes they state | Change one vector's `expect` block to something wrong and run `--selftest`; it must fail. If it passes for any vector, expectations were filled in from a run |
| A permissive checker is caught | Read `permissive_check` in `check.py`, satisfy yourself it is genuinely weaker, then run `--selftest` and count the disagreeing rows yourself |
| The 24 h revocation bound cannot be widened silently | Change `revocationFreshnessBoundSeconds` to 90000 and run `--selftest`; D13 must flip and the selftest must fail |
| Two implementations agree | Delete or edit `check.mjs` and run `python crosscheck.py`; it must fail, not report agreement |
| `SHA256SUMS` covers what you run | Alter one byte of one file, run `sha256sum -c SHA256SUMS`, and see it fail |
| The board does not lie | Open `EVIDENCE-BOARD.html` offline; then change a row count in `expected.json`, rebuild with `python _build_board.py` (if present) or hand-edit the payload, and confirm the page turns red |

## Questions worth putting to the package

1. Does `could-not-determine` ever get folded into `pass` anywhere in the code?
2. When two defects are present, is the reported first code the earlier check in
   the published order, and is that order stated anywhere a reader can see?
3. Is any check implemented twice with slightly different semantics between
   `check.py` and `check.mjs`? Compare the two by reading, not by trusting the
   cross-check output.
4. Does any vector's `about` text describe a different situation from its inputs?
5. Does `policy.json` state a choice wherever the outcome is a policy choice
   rather than a finding (D08 is the obvious one)?

## What this package does not claim, and where a reviewer should stop

- No cryptographic verification: `signature: "ok"` is a stand-in for a result
  reached elsewhere, and says so.
- No network identity, no multi-hop delegate chains, no concurrency, no
  performance.
- No conformance to any product, no endorsement by any organisation.
- Passing 120 rows is a floor, not a certificate.

If a reviewer finds a claim stronger than the evidence above, that finding is
more useful than any confirmation.
