# Gateway delegation decisions: expected results, v0

*Draft for discussion. A small, runnable test set for the runtime side of the trust work: what a gateway should decide when an agent acts under a delegated mandate.*

## Purpose

A delegated-authority evaluation can be read two ways. The first is about the mandate: who issued it, what scope it names, whether it chains to a pinned anchor. The second is about the moment of use: what the gateway actually admits when a request arrives, and on what basis. This set covers the second. Each case fixes the inputs, states the check that decides it, and gives the result a checker is expected to reach, so implementations can compare behaviour against the same inputs rather than against prose.

Results are three-valued at the decision layer and split at the reporting layer. **pass**, **fail**, and a hold that names its side: **record-unresolved** when the record, or what it points at, cannot be resolved (missing, unreachable, stale, not yet effective, or a citation that does not walk), and **check-incomplete** when the check itself could not be completed on the inputs supplied (unparsable window, no declared scope, opaque content, no key binding). Nothing is ever folded into pass or into fail. The decision follows the result: pass gives **allow**, fail gives **refuse**, and both kinds of hold give **hold**.

## Origin

On 20 November 2026 the AI KR CG chair opened `DIFdelegateauth.md` for comments and asked participants to put their comments in the note. Six comments were added in #35 (https://github.com/w3c-cg/aikr/issues/35), all drawn from implementation work on a gateway and an A2A adapter. Three of them name gaps that this set tries to make testable:

- comment 1: the attenuation criterion needs a per-request record of which scope was claimed, which was effective, and on what basis;
- comment 2: the confused-deputy criterion is content-mediated as well as policy-mediated — a deputy can be misled by the payload while holding a perfectly valid mandate;
- comment 3: revocation needs a three-valued verdict under partition, with a bound on how old the last successful check may be.

The set also carries the point that came up in the chair's correction on comment 5: what must be *reachable at verification time* is part of the record, not an afterthought. Case D12 is that point as a row.

## The table

Every case is evaluated at a pinned instant, 2026-11-23T00:00:00Z. The revocation freshness bound is 24 hours. The grant in every mandate names the agent, two tools (`tool:search`, `tool:summarise`) and a validity window from 2026-11-01 to 2026-12-01.

| Case | Situation | Check that decides | Result | Decision | Code | Paired with |
|---|---|---|---|---|---|---|
| D01 | Positive control: mandate valid, declared scope inside the grant, revocation fresh, pointer reachable. | All seven | pass | allow | — | — |
| D02 | Attenuation under delegation: declared scope adds `tool:billing`, which the grant does not name. | Attenuation | fail | refuse | `SCOPE_WIDENED` | D01 |
| D03 | No scope declared: the caller claims nothing, the gateway records a transport-peer basis. | Attenuation | check-incomplete | hold | `NO_DECLARED_SCOPE` | D01 |
| D04 | Subject mismatch: a different agent presents the mandate of `agent:gw-agent`. | Subject | fail | refuse | `SUBJECT_MISMATCH` | D01 |
| D05 | Expired mandate: the grant ended on 2026-11-20, before the evaluation instant. | Window | fail | refuse | `MANDATE_EXPIRED` | D01 |
| D06 | Confused deputy by content: a valid mandate carries an inline instruction in the payload. | Content | fail | refuse | `CONTENT_OVERRIDE` | D01 |
| D07 | Role spoofing in content: the payload asserts `claimedRole: owner`. | Content | fail | refuse | `ROLE_SPOOF` | D06 |
| D08 | Opaque content: the gateway cannot inspect the payload it is asked to forward. | Content | check-incomplete | hold | `OPAQUE_CONTENT` | D01 |
| D09 | Revoked before the evaluation instant (effective 2026-11-01). | Revocation | fail | refuse | `REVOKED` | D11 |
| D10 | Revocation source unreachable at evaluation time. | Revocation | record-unresolved | hold | `SOURCE_UNREACHABLE` | D01 |
| D11 | Stale revocation check: last successful lookup on 2026-11-20, beyond the 24 hour bound. | Revocation | record-unresolved | hold | `STALE_REVOCATION` | D09 |
| D12 | Verification-time reachability: the record points at evidence that cannot be reached. | Evidence pointer | record-unresolved | hold | `POINTER_UNREACHABLE` | D01 |
| D13 | Bound edge: the revocation check is 25 hours old at the evaluation instant, one hour outside the 24 hour bound. | Revocation | record-unresolved | hold | `STALE_REVOCATION` | D11 |
| D14 | Revocation recorded with `effectiveFrom` in the future: the record exists, its effect does not. | Revocation | record-unresolved | hold | `REVOCATION_NOT_YET_EFFECTIVE` | D09 |
| D15 | Mandate with no `signature` field at all — absent, not merely wrong. | Signature | fail | refuse | `MANDATE_UNSIGNED` | D01 |
| D16 | Revoked mandate whose refusal carries no receipt: the decision cannot be accounted for afterwards. | Receipt on refusal | fail | refuse | `REVOKED` (+ `RECEIPT_MISSING_ON_REFUSE`) | D09 |
| D17 | Mandate signed by a key that is not the subject's key: the grant is attributable to someone else. | Signer key binding | fail | refuse | `SIGNER_KEY_NOT_BOUND` | D01 |
| D18 | Mandate cites a predecessor by digest that does not resolve in the chain supplied with the case. | Lineage | record-unresolved | hold | `LINEAGE_UNRESOLVED` | D15 |

Nine fails, eight holds (six `record-unresolved`, two `check-incomplete`), one pass. The asymmetry is deliberate: most real requests are not clean, and a set that mostly returns pass would not tell implementations apart.

Two files exist so the table can be checked without reading prose:
`REPRODUCTION.md` (commands, interpreter, exit codes, observed output, the
second-machine run and the integrity check) and `EVIDENCE-BOARD.html`
(a single offline page whose row count and tallies are re-computed from
the embedded payload when opened, and which says so if they disagree; rebuild
with `make_board.py`).

`AER1-CROSSWALK.md` reads AER-1's five anchor outcomes with this decision map
and this package's rows with AER-1's five outcomes, side by side, and records
the one state AER-1 has that this package does not (`absent`). It is generated
by `make_aer1_crosswalk.py`, which fetches AER-1's published vector file and
checks it against the digest in AER-1's own corpus index; the third-party bytes
are fetched, not vendored.


### Invariant coverage

Each case is tagged with the invariant it exercises, so coverage can be compared with sets that organise themselves by invariant rather than by scenario. The eleven here are I1–I11; a class with no case is a class this set does not test, and is listed as such rather than inferred.

| Invariant | Statement | Cases |
|---|---|---|
| I1 | the mandate names the agent that presents it | D01, D04 |
| I2 | the evaluation instant is inside the validity window | D01, D05 |
| I3 | the mandate carries a signature result | D01, D15 |
| I4 | declared scope never exceeds the grant | D01, D02, D03 |
| I5 | the payload is inspected before forwarding | D01, D06, D07, D08 |
| I6 | revocation status is fresh and effective | D01, D09, D10, D11, D13, D16 |
| I7 | a revocation recorded with a future effect is not yet an effect | D14 |
| I8 | what the record points at is reachable at verification time | D01, D12 |
| I9 | the signing key is bound to the subject | D17 |
| I10 | a cited predecessor resolves in the supplied chain | D18 |
| I11 | every refusal carries a receipt binding decision, case and policy | D16 |

Coverage is eleven of eleven classes with eighteen cases. That is coverage, not volume: a set organised by invariant can execute a class with one case, and a class with one case can be passed by a checker that only handles that shape.

### Why D08 is a hold and not a refusal

The payload is not inspected, so nothing is known about it. A policy is free to refuse opaque content outright, and many gateways will; but that refusal is a policy choice, not a finding. The set records what the evidence supports — an unknown — and leaves the choice to the policy. `policy.json` states the choice this set was run with.

### Why D03 is a hold

An undeclared scope is not evidence of a narrower grant. Recording the basis as `transport-peer` is the fix to comment 1, but recording a basis is not the same as establishing a scope. The row exists so that a gateway which treats "no declared scope" as "full granted scope" is caught.

## The vector set, and a second implementation

The eighteen cases above are the ones with names and prose. Alongside them sits a
vector set of **104 generated rows** in `fixtures/vectors/`, one file per vector,
each stating the outcome it must produce:

    "expect": { "result": "record-unresolved", "code": "LINEAGE_UNRESOLVED" }

Those expectations were written with the vectors, not produced by running the
checker, so a checker that drifts fails the selftest instead of redefining the
answer. That claim is checkable by reading `gen_vectors.py`: every vector's
`expect` is a literal argument to `add()`, and no line in that file calls the
checker. Every invariant class carries at least one passing vector as well as
its defect rows (I1 2/8 pass, I2 9/16, I3 1/6, I4 5/12, I5 4/8, I6 4/16,
I7 1/8, I8 1/4, I9 1/4, I10 2/5, I11 1/6, combinations 1/11), so a checker that
holds or refuses a whole class without discriminating is visible rather than
flattered. `VECTORS.md` documents the grid and the distribution (pass 32 ·
record-unresolved 18 · check-incomplete 7 · fail 47).

`check.mjs` is a second implementation, in JavaScript, written against the same
published check order and code table. `crosscheck.py` runs both over the curated
cases and the vectors and compares every row — verdict, first code, and which
side each hold is on; on the current tree that is 122 rows with zero
disagreements. **What that does and does not buy:** it rules out transcription
error, per-language date and string handling, and any single-implementation
artefact; it does **not** rule out a misreading shared by both, because both
were written by the same hand. The two ways this package limits that risk are
different in kind: the permissive-checker differential (a deliberately weaker
reader must disagree on 13 of 18 cases) and the vector expectations being
literals rather than outputs. Anything past that needs a third party to derive
expectations independently, which is what a review is for, and the honest
statement is that no such independent derivation exists yet.

## Checks and how results combine

The reference checker runs these checks in order and records each one's result:

1. **subject** — the request's agent is the mandate's subject (`SUBJECT_MISMATCH`).
2. **window** — the evaluation instant is inside the mandate's validity window (`MANDATE_EXPIRED`, `MANDATE_NOT_YET_VALID`, `WINDOW_UNPARSABLE`).
3. **signature** — the mandate is signed and was verified at issue time (`MANDATE_UNSIGNED`). This set does not test signature algorithms; the field is a stand-in for a verification result reached elsewhere, and is stated as such rather than implied.
4. **attenuation** — every declared scope item is inside the grant (`SCOPE_WIDENED`, `NO_DECLARED_SCOPE`).
5. **content** — the payload is inspected before forwarding (`CONTENT_OVERRIDE`, `ROLE_SPOOF`, `OPAQUE_CONTENT`).
6. **revocation** — status is known, current within the bound, effective at the evaluation instant, and not revoked (`REVOKED`, `SOURCE_UNREACHABLE`, `STALE_REVOCATION`, `REVOCATION_UNKNOWN`, `REVOCATION_NOT_YET_EFFECTIVE`). A record whose own `effectiveFrom` is later than the evaluation instant is record-unresolved, not a refusal: the gateway cannot decide on an effect that has not begun.
7. **evidence pointer** — what the record points at is reachable at verification time (`POINTER_UNREACHABLE`).
8. **signer key binding** — the key that signed the mandate is the key bound to the subject (`SIGNER_KEY_NOT_BOUND`, `SIGNER_KEY_UNSPECIFIED`). A mandate that declares no fingerprint at all is an unknown, not a pass: nothing ties the signature to the subject.
9. **lineage** — a cited predecessor resolves inside the chain supplied with the case (`LINEAGE_UNRESOLVED`). A citation that exists but cannot be walked is an unknown.
10. **receipt on refusal** — when the result is a refusal, the case must carry a receipt binding the decision, the case id and the policy digest (`RECEIPT_MISSING_ON_REFUSE`). A refusal nobody can attribute to a policy afterwards is itself a defect; the primary failing code stays first so the reason for the refusal is not buried.

Any fail gives fail. Otherwise any record-unresolved gives record-unresolved; a check-incomplete is reported only when nothing on the record side is unresolved. Only if all ten pass is the result pass. The row also carries a split listing (`unknown.record` and `unknown.checker`), so a consumer that reads only the result still learns which side it is on, and one that reads the split learns why. A hold is not a refusal, and a refusal is not a finding of malice: the decision map is in `policy.json` so a reader can see which policy this set was evaluated under.

## How to run

```
python3 check.py                  # curated cases plus vectors, 122 rows
python3 check.py --vectors        # the vector table alone
python3 check.py --json out.json  # machine-readable results
python3 check.py --selftest       # nine checks on the set itself
node check.mjs                    # the same rows, second implementation
python3 crosscheck.py             # both implementations, row by row
python3 policy_digest.py --check  # the digest the receipts bind to
python3 make_board.py             # rebuild the board from the checker's results
python3 make_review_packet.py     # rebuild the packet this was reviewed on
python3 make_aer1_crosswalk.py    # refetch AER-1's vectors and rebuild the crosswalk
```

No dependencies beyond the Python standard library, no network, no credentials. `SHA256SUMS` carries a digest for every file in this directory except itself, so a reader can check that what they run is what was reviewed. `--selftest` verifies nine things:

1. `expected.json` matches the checker on all eighteen curated cases;
2. a deliberately permissive checker — content ignored, unknown folded into pass, staleness ignored, signer key and lineage unread — is caught on thirteen of the eighteen (`D03, D05, D06, D07, D08, D10, D11, D12, D13, D14, D15, D17, D18`);
3. changing one fixture moves its result (D02 with an in-grant scope collapses to pass), which shows the table is computed from the fixtures rather than asserted;
4. widening the revocation bound from 24 to 25 hours changes D13 from `record-unresolved` to `pass`, so a silently loosened bound is visible rather than absorbed;
5. removing a refusal's receipt makes the receipt check fail, and adding a bound receipt clears it (D16), so the receipt requirement is not decorative;
6. adding the cited digest to D18's chain clears its unresolved verdict, so an empty-but-present citation cannot pass as a walked chain;
7. the policy digest is recomputed from `policy.json` itself and must match the stored value, so a receipt cannot bind to a policy that nobody can reproduce;
8. a hold names its side: a record-only case gives `record-unresolved`, a checker-only case gives `check-incomplete`, and a case with one of each reports both in `unknown.record` and `unknown.checker` while the result row stays on `record-unresolved`;
9. all 104 vectors match the outcomes they state, with the distribution printed — a vector set that only restates the checker's output would pass this item vacuously, which is why the expectations live in the vector files and not in `expected.json`.

## Boundaries

This set is eighteen curated cases plus 104 vectors, all synthetic, not a certification and not a conformance suite for any product. It says nothing about cryptographic correctness, network identity, or the truth of any statement a record points at. It does not test performance, concurrency, or multi-hop chains; a chain case would need a separate set. The mandate signature field stands in for a verification result so that the runtime checks can be tested in isolation.

Where a policy has a choice, `policy.json` records the choice made here, including the D08 choice and the argument for it (`notes.opaqueContentIsAPolicyChoice`). A different policy may legitimately decide D08 differently; the check result would still be check-incomplete, and the decision would differ.

`EXTERNAL-AI-REVIEW.md` records the external review this revision was put through before publication: the two briefs, the two raw replies, and what was changed because of them, including the one finding that was declined and why. It is not an endorsement and does not establish that the claims are true; it establishes that two readers briefed in opposite directions could not find the packet self-contradictory from the text alone.

## Implementation context

The six comments in #35 come from an implementation that runs a clause-level gateway conformance matrix over 43 clauses (34 required) of T/ISC 0174-2026: at commit `da0dc9be5b38f7c0515d5f4fec6e2fe64f1aef5a` on 2026-11-23 the matrix reports 21 pass, 22 partial, 0 missing, with all 37 probes exercised. "Partial" there means implemented but not fully evidenced at clause level, and is reported as partial rather than rounded up. That matrix is clause coverage in a vendor's own repository; it is not conformance to this fixture set, and no such claim is made here.

## Corrections

Corrections are welcome as an issue on this repository with the file name in the title, or as a pull request. Cases where two implementations disagree are the most useful: a disagreement either fixes a row or shows where the policy boundary sits.
