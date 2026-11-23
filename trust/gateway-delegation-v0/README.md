# Gateway delegation decisions: expected results, v0

*Draft for discussion. A small, runnable test set for the runtime side of the trust work: what a gateway should decide when an agent acts under a delegated mandate.*

## Purpose

A delegated-authority evaluation can be read two ways. The first is about the mandate: who issued it, what scope it names, whether it chains to a pinned anchor. The second is about the moment of use: what the gateway actually admits when a request arrives, and on what basis. This set covers the second. Each case fixes the inputs, states the check that decides it, and gives the result a checker is expected to reach, so implementations can compare behaviour against the same inputs rather than against prose.

Results are three-valued: **pass**, **fail** and **could-not-determine**. A check that could not be completed is never folded into pass, and never into fail. The decision follows the result: pass gives **allow**, fail gives **refuse**, could-not-determine gives **hold**.

## Origin

On 20 November 2026 the AI KR CG chair opened `DIFdelegateauth.md` for comments and asked participants to put their comments in the note. Six comments were added in #35, all drawn from implementation work on a gateway and an A2A adapter. Three of them name gaps that this set tries to make testable:

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
| D03 | No scope declared: the caller claims nothing, the gateway records a transport-peer basis. | Attenuation | could-not-determine | hold | `NO_DECLARED_SCOPE` | D01 |
| D04 | Subject mismatch: a different agent presents the mandate of `agent:gw-agent`. | Subject | fail | refuse | `SUBJECT_MISMATCH` | D01 |
| D05 | Expired mandate: the grant ended on 2026-11-20, before the evaluation instant. | Window | fail | refuse | `MANDATE_EXPIRED` | D01 |
| D06 | Confused deputy by content: a valid mandate carries an inline instruction in the payload. | Content | fail | refuse | `CONTENT_OVERRIDE` | D01 |
| D07 | Role spoofing in content: the payload asserts `claimedRole: owner`. | Content | fail | refuse | `ROLE_SPOOF` | D06 |
| D08 | Opaque content: the gateway cannot inspect the payload it is asked to forward. | Content | could-not-determine | hold | `OPAQUE_CONTENT` | D01 |
| D09 | Revoked before the evaluation instant (effective 2026-11-01). | Revocation | fail | refuse | `REVOKED` | D11 |
| D10 | Revocation source unreachable at evaluation time. | Revocation | could-not-determine | hold | `SOURCE_UNREACHABLE` | D01 |
| D11 | Stale revocation check: last successful lookup on 2026-11-20, beyond the 24 hour bound. | Revocation | could-not-determine | hold | `STALE_REVOCATION` | D09 |
| D12 | Verification-time reachability: the record points at evidence that cannot be reached. | Evidence pointer | could-not-determine | hold | `POINTER_UNREACHABLE` | D01 |

Six fails, five could-not-determine, one pass. The asymmetry is deliberate: most real requests are not clean, and a set that mostly returns pass would not tell implementations apart.

### Why D08 is a hold and not a refusal

The payload is not inspected, so nothing is known about it. A policy is free to refuse opaque content outright, and many gateways will; but that refusal is a policy choice, not a finding. The set records what the evidence supports — an unknown — and leaves the choice to the policy. `policy.json` states the choice this set was run with.

### Why D03 is a hold

An undeclared scope is not evidence of a narrower grant. Recording the basis as `transport-peer` is the fix to comment 1, but recording a basis is not the same as establishing a scope. The row exists so that a gateway which treats "no declared scope" as "full granted scope" is caught.

## Checks and how results combine

The reference checker runs these checks in order and records each one's result:

1. **subject** — the request's agent is the mandate's subject (`SUBJECT_MISMATCH`).
2. **window** — the evaluation instant is inside the mandate's validity window (`MANDATE_EXPIRED`, `MANDATE_NOT_YET_VALID`, `WINDOW_UNPARSABLE`).
3. **signature** — the mandate is signed and was verified at issue time (`MANDATE_UNSIGNED`). This set does not test signature algorithms; the field is a stand-in for a verification result reached elsewhere, and is stated as such rather than implied.
4. **attenuation** — every declared scope item is inside the grant (`SCOPE_WIDENED`, `NO_DECLARED_SCOPE`).
5. **content** — the payload is inspected before forwarding (`CONTENT_OVERRIDE`, `ROLE_SPOOF`, `OPAQUE_CONTENT`).
6. **revocation** — status is known, current within the bound, and not revoked (`REVOKED`, `SOURCE_UNREACHABLE`, `STALE_REVOCATION`, `REVOCATION_UNKNOWN`).
7. **evidence pointer** — what the record points at is reachable at verification time (`POINTER_UNREACHABLE`).

Any fail gives fail. Otherwise any could-not-determine gives could-not-determine. Only if all seven pass is the result pass. A hold is not a refusal, and a refusal is not a finding of malice: the decision map is in `policy.json` so a reader can see which policy this set was evaluated under.

## How to run

```
python3 check.py                  # the table above
python3 check.py --json out.json  # machine-readable results
python3 check.py --selftest       # three checks on the set itself
```

No dependencies beyond the Python standard library, no network, no credentials. `SHA256SUMS` carries a digest for every file in this directory except itself, so a reader can check that what they run is what was reviewed. `--selftest` verifies three things:

1. `expected.json` matches the checker on all twelve cases;
2. a deliberately permissive checker — content ignored, unknown folded into pass, staleness ignored — is caught on eight of the twelve (`D03, D05, D06, D07, D08, D10, D11, D12`);
3. changing one fixture moves its result (D02 with an in-grant scope collapses to pass), which shows the table is computed from the fixtures rather than asserted.

## Boundaries

This set is twelve synthetic cases, not a certification and not a conformance suite for any product. It says nothing about cryptographic correctness, network identity, or the truth of any statement a record points at. It does not test performance, concurrency, or multi-hop chains; a chain case would need a separate set. The mandate signature field stands in for a verification result so that the runtime checks can be tested in isolation.

Where a policy has a choice, `policy.json` records the choice made here. A different policy may legitimately decide D08 differently; the check result would still be could-not-determine, and the decision would differ.

## Implementation context

The six comments in #35 come from an implementation that runs a clause-level gateway conformance matrix over 43 clauses (34 required) of T/ISC 0174-2026: at commit `da0dc9be5b38f7c0515d5f4fec6e2fe64f1aef5a` on 2026-11-23 the matrix reports 21 pass, 22 partial, 0 missing, with all 37 probes exercised. "Partial" there means implemented but not fully evidenced at clause level, and is reported as partial rather than rounded up. That matrix is clause coverage in a vendor's own repository; it is not conformance to this fixture set, and no such claim is made here.

## Corrections

Corrections are welcome as an issue on this repository with the file name in the title, or as a pull request. Cases where two implementations disagree are the most useful: a disagreement either fixes a row or shows where the policy boundary sits.
