# Key and evidence states: expected results, v0

*Draft for discussion. A small, runnable test set for the trust work item, building on a proposal by Nicholas Templeman on public-aikr.*

## Purpose

When a relying party checks a signed statement, the answer is not always yes or no. The key may be an old one that was valid when it signed, the lookup that told the verifier about the key may be out of date, the source may be unreachable, or the source may publish no revocation status at all. This set gives one row per such state, with fixed inputs and the result a checker is expected to reach, so implementations can compare their behaviour against the same inputs rather than against prose. The core point is that results are three-valued: **pass**, **fail** and **could-not-determine**. A check that could not be completed is never folded into pass, and never into fail.

## Origin

On 11 October 2026, replying to Paola Di Maio's note on the root KSK rollover ([ksk.md](../ksk.md)), Nicholas Templeman proposed:

> "A useful bounded contribution would be a small trust-state vocabulary and fixture table covering an old key within its stated historical interval, a stale current lookup, a successor key without an established lineage, a revoked key, and an unavailable validation source. Each row should identify the method, source, as-of time, lineage evidence and resulting uncertainty."

Source: <https://lists.w3.org/Archives/Public/public-aikr/2026Oct/0002.html>

This set is one attempt at that table, tracked as item 2 under "New work" in issue #16. Each of Templeman's five states is a row below. Three rows are added: a positive control, revocation status that cannot be known, and a signing time that is only self-asserted. The second table carries his columns (method, source, as-of time, lineage evidence, resulting uncertainty).

## The table

Every case is evaluated at a pinned instant, 2026-10-11T00:00:00Z. The staleness bound is 24 hours. Decision follows result: pass gives admit, fail gives refuse, could-not-determine gives hold (the policy's stated action on unknown).

| Case | Situation | Inputs | Check attempted | Result | Decision | Why |
|---|---|---|---|---|---|---|
| C01 | Positive control | Statement signed by current key k-2026, timestamped 2026-10-10. History fetched one hour before evaluation. Lineage from k-2025 to k-2026 present. Revocation list present and empty. | All eight checks | pass | admit | Every check completed and passed. The key is valid and unrevoked at the evaluation instant (`OK_CURRENT`). |
| C02 | Old key, signature made inside its historical interval | Statement signed by k-2025, timestamped 2026-02-01. k-2025 is valid from 2025-01-01 until 2026-04-01. | Key interval at the attested signing time | pass | admit | The signature was made while the key was valid. The pass is historical (`OK_HISTORICAL`): it says the key was valid then, not that it is current. |
| C03 | Same old key, signature made after its interval | Statement signed by k-2025, timestamped 2026-05-01. | Key interval at the attested signing time | fail | refuse | `KEY_OUTSIDE_VALIDITY`. Paired control: C02. |
| C04 | Stale lookup | As C01, but the history was fetched on 2026-10-06, five days before evaluation, against a 24 hour bound. | Freshness of the lookup | could-not-determine | hold | `STALE_LOOKUP`. Every other check passes on the data held, but the data may be out of date (a revocation published since would not be seen). Paired control: C01. |
| C05 | Successor key with no lineage | Statement signed by k-x. The source lists k-x as successor of k-2025, but no lineage statement signed by k-2025 exists. | Signed lineage from the pinned anchor to the signing key | fail | refuse | `NO_LINEAGE`. Fail because `policy.json` sets `lineageComplete: true`: the source is assumed to publish all lineage, so absence is a definite no. See the note below and C11. Paired control: C01, where k-2026 has a lineage statement. |
| C06 | Revoked key, signature made before revocation | k-2026 revoked with effect from 2026-09-01. Statement timestamped 2026-08-15. | Revocation at the attested signing time | pass | admit | The revocation does not reach back before its stated effective time (`OK_HISTORICAL`). |
| C07 | Revoked key, signature made after revocation | Same revocation. Statement timestamped 2026-10-10. | Revocation at the attested signing time | fail | refuse | `KEY_REVOKED`. Paired controls: C06, and C01 (same statement, no revocation). |
| C08 | Validation source unavailable | The lookup timed out. No history document. | Reach the source | could-not-determine | hold | `SOURCE_UNAVAILABLE`. No key material, so nothing else can be checked. The statement may be fine. Paired control: C01. |
| C09 | Revocation status unknowable | The history carries keys and lineage, but the source publishes no revocation list. | Revocation status | could-not-determine | hold | `NO_STATUS_SOURCE`. An empty list says nothing is revoked; an absent list says nothing at all. Paired control: C01 (empty list). |
| C10 | Old key, signing time only self-asserted | Statement signed by k-2025, payload says `signedAt` 2026-02-01, no timestamp token. | Key interval | could-not-determine | hold | `SIGNING_TIME_UNATTESTED`. Without an attested time the signature is judged at the evaluation instant, when k-2025 is outside its interval. A self-asserted date is never used: whoever holds a retired key can write any date. Paired control: C02. |
| C11 | Successor key with no lineage, completeness not assumed | As C05, but under `policy-open.json`, which sets `lineageComplete: false`. | Signed lineage from the pinned anchor to the signing key | could-not-determine | hold | `LINEAGE_NOT_ESTABLISHED`. Without the completeness assumption, a missing lineage statement is not evidence: one can still be appended later, and the history is not signed as a whole. Paired with C05. |

**C05 and C11: fail or could-not-determine.** The checker asks one question: is the signing key linked to the pinned anchor by lineage statements, each signed by its predecessor inside the predecessor's interval? Whether a missing lineage statement is a definite no depends on one assumption: that the source publishes all lineage for the identifier. The policy now states it as `lineageComplete`. With it (C05), absence is a definite no, so the result is fail. Without it (C11), absence is not evidence, because a lineage statement can still be appended and the history is not signed as a whole, so the result is could-not-determine. In both, the outcome means continuity was not established; neither is evidence that a different party controls k-x, and nothing is admitted either way. Michael Blake made this point on PR #25: of the fails in the set, NO_LINEAGE is the only one that rests on the completeness of an unsigned document rather than on something signed or computed. A profile should say which reading it takes.

### Fixture details, in Templeman's columns

Method and source are the same for every case: an HTTPS GET of a key history document from `https://keys.example/subject-a/history.json` (synthetic). The anchor k-2025 and the timestamp authority key are pinned in `fixtures/policy.json`.

| Case | As-of (lookup fetched at) | Signing time and its source | Lineage evidence | Uncertainty left |
|---|---|---|---|---|
| C01 | 2026-10-10T23:00Z | 2026-10-10T12:00Z, timestamp token | k-2025 to k-2026, signed by k-2025 on 2026-03-01 | None within the set's scope |
| C02 | 2026-10-10T23:00Z | 2026-02-01T12:00Z, timestamp token | Anchor key, none needed | Whether k-2025 is current (it is not; the pass is historical) |
| C03 | 2026-10-10T23:00Z | 2026-05-01T12:00Z, timestamp token | Anchor key, none needed | None |
| C04 | 2026-10-06T00:00Z | 2026-10-10T12:00Z, timestamp token | As C01 | Anything published after 2026-10-06 |
| C05 | 2026-10-10T23:00Z | 2026-10-10T12:00Z, timestamp token | None; unsigned listing only | Who controls k-x |
| C06 | 2026-10-10T23:00Z | 2026-08-15T12:00Z, timestamp token | As C01 | Whether compromise began before the stated effective time |
| C07 | 2026-10-10T23:00Z | 2026-10-10T12:00Z, timestamp token | As C01 | None |
| C08 | attempted 2026-10-10T23:00Z | not reached | not reached | Everything |
| C09 | 2026-10-10T23:00Z | 2026-10-10T12:00Z, timestamp token | As C01 | Revocation of k-2026 and of k-2025 |
| C10 | 2026-10-10T23:00Z | Self-asserted only | Anchor key, none needed | When the signature was made |
| C11 | 2026-10-10T23:00Z | 2026-10-10T12:00Z, timestamp token | None; unsigned listing only, completeness not assumed | Whether a lineage statement exists elsewhere |

## Checks and how results combine

The checker runs these checks in order and records each one's result:

1. **source**: the lookup reached the source.
2. **history-digest**: the history document matches the SHA-256 recorded in the lookup record.
3. **freshness**: evaluation instant minus fetched-at is within the staleness bound.
4. **lineage**: the signing key is the pinned anchor, or is linked to it by lineage statements, each signed by the predecessor, timestamped inside the predecessor's interval, and not made after the predecessor's revocation. The unsigned key listing in the history is never trusted for key material.
5. **signature**: Ed25519 over the JCS bytes of the payload verifies under the resolved key.
6. **signing-time**: a timestamp token from the pinned authority, over the digest of the signed statement. Absent means the statement is judged at the evaluation instant.
7. **interval**: the key's validity interval contains the signing time.
8. **revocation**: no verified revocation entry for the key takes effect at or before the signing time.

The case result is **fail** if any check failed, otherwise **could-not-determine** if any check could not be completed, otherwise **pass**. A fail outranks could-not-determine because each fail here rests on evidence that later data cannot reverse: signature arithmetic, a signed revocation, a signed and closed interval. This assumes key histories are append-only. The one exception is `NO_LINEAGE`, which rests on the source's completeness; it is a fail only when the policy asserts `lineageComplete`, and `LINEAGE_NOT_ESTABLISHED` (could-not-determine) otherwise. A pass is reported as `OK_CURRENT` when the key is also valid and unrevoked at the evaluation instant, and `OK_HISTORICAL` when it is not.

Reason codes: `OK_CURRENT`, `OK_HISTORICAL`, `KEY_OUTSIDE_VALIDITY`, `KEY_REVOKED`, `NO_LINEAGE`, `BAD_LINEAGE`, `LINEAGE_OUTSIDE_INTERVAL`, `BAD_SIGNATURE`, `BAD_TIMESTAMP`, `HISTORY_DIGEST_MISMATCH` (all fail or pass); `STALE_LOOKUP`, `SOURCE_UNAVAILABLE`, `NO_STATUS_SOURCE`, `REVOCATION_UNVERIFIABLE`, `SIGNING_TIME_UNATTESTED`, `LINEAGE_NOT_ESTABLISHED` (all could-not-determine).

## Mutation controls

Each negative case is paired with a passing control. The mutation controls make that pairing executable: each takes a passing input, changes one thing, and the result must flip. Where a mutation edits the history document, the recorded digest is updated, as if a fresh source served the changed document, except in M11.

| Id | Base | Change | Expected |
|---|---|---|---|
| M01 | C01 | Flip one byte of the statement signature | fail, `BAD_SIGNATURE` |
| M02 | C01 | Move the evaluation instant three days later | could-not-determine, `STALE_LOOKUP` |
| M03 | C01 | Drop the lineage statement for k-2026 | fail, `NO_LINEAGE` |
| M04 | C01 | Flip one byte of the lineage signature | fail, `BAD_LINEAGE` |
| M05 | C02 | Close the anchor interval before the signing time | fail, `KEY_OUTSIDE_VALIDITY` |
| M06 | C02 | Move the timestamp token's time by one second, without re-signing | fail, `BAD_TIMESTAMP` |
| M07 | C02 | Remove the timestamp token | could-not-determine, `SIGNING_TIME_UNATTESTED` |
| M08 | C06 | Move the revocation's effective time without re-signing | could-not-determine, `REVOCATION_UNVERIFIABLE` |
| M09 | C01 | Make the validation source unavailable | could-not-determine, `SOURCE_UNAVAILABLE` |
| M10 | C01 | Remove the revocation list from the source | could-not-determine, `NO_STATUS_SOURCE` |
| M11 | C01 | Alter the history without updating the recorded digest | fail, `HISTORY_DIGEST_MISMATCH` |

M08 is a choice worth discussing: a revocation entry that does not verify is neither honoured nor ignored. Ignoring it would let anyone who strips a valid signature turn revoked into not revoked, and honouring it would let anyone revoke anything, so the result is could-not-determine.

## Running it

Python 3.12 or later, with `cryptography` and `rfc8785` (tested with cryptography 50.0.2 and rfc8785 0.1.4).

```
python3 -m venv .venv && . .venv/bin/activate
pip install cryptography rfc8785
python check.py          # add -v to print every check for every case
```

`check.py` first confirms the fixtures match `SHA256SUMS`, then runs the eleven cases and eleven mutation controls against `expected.json`. It exits 0 only if everything matches.

To confirm the fixtures are reproducible, regenerate them and compare:

```
python generate.py
shasum -a 256 -c SHA256SUMS      # or: sha256sum -c SHA256SUMS
git diff --exit-code fixtures SHA256SUMS
```

`expected.json` is written by hand and is not produced by either script, so the checker is tested against expectations rather than against itself. An implementation in another language can ignore `check.py` and compare its own results with `expected.json` directly.

## Fixture format

- **Signed object**: `{"payload": {...}, "sig": {"alg": "Ed25519", "kid": "...", "value": "<base64url>"}}`. `value` is an Ed25519 signature over the RFC 8785 (JCS) bytes of `payload`. Public keys are raw 32-byte Ed25519 keys, base64url without padding.
- **Timestamp token**: a signed object from the timestamp authority `tsa-1`, attached as `timestamp`, whose payload is `{"type": "timestamp", "digest": "sha256:<hex>", "time": "..."}`. The digest is SHA-256 of the JCS bytes of `{"payload", "sig"}` of the object it stamps, so it binds the signature too.
- **Key history** (`fixtures/history/`): `keys` (an unsigned listing), `lineage` (signed by the predecessor and timestamped), and `revocations` (signed by the revoked key, with `effectiveFrom`). `complete.json` has an empty revocation list, `revoked.json` revokes k-2026, and `no-status.json` has no revocation list.
- **Statements** (`fixtures/statements/`): signed objects. The payload's `signedAt` is self-asserted and the checker never reads it.
- **Cases** (`fixtures/cases/`): the evaluation instant, the policy, the statement, and a lookup record with method, source, fetched-at, status, and the document's path and SHA-256.
- **Policy** (`fixtures/policy.json`): the identifier, the pinned anchor key with its interval, the pinned timestamp authority key, the staleness bound, the action on unknown, and `lineageComplete`. `fixtures/policy-open.json` is the same with `lineageComplete: false` (used by C11).

Keys are derived from published seed strings in `generate.py`, and Ed25519 signatures are deterministic, so regeneration is byte-identical. These are test keys and protect nothing. Times are UTC. Identifiers are ASCII, no number exceeds 2^53, and no Unicode normalization is applied, so the comparison cases in §4.1 of [kroftrust.md](../kroftrust.md) do not arise in these fixtures.

## Mapping to KRT

Where a row or field corresponds to a term in [krt.ttl](../krt.ttl):

| This set | KRT | Fit |
|---|---|---|
| Result pass / fail / could-not-determine | `krt:outcome` with `krt:Yes` / `krt:No` / `krt:Unknown` | Clean. R0 already requires exactly one of the three. |
| Decision admit / refuse / hold | `krt:actionTaken` "proceed" / "refuse" / "pause" | Close. KRT values are free strings; hold is nearest to pause. |
| Policy action on unknown | `krt:onUnknown` on `krt:TrustPolicy` | Clean. |
| Staleness bound | `krt:stalenessBound` | Partial. KRT defines it on the path as the longest window in which a revoked item can still pass; here the relying party uses it as the maximum lookup age. The two are the same quantity seen from either side. Ankur Chrungoo's point in #8, that it should cover superseded items as well as revoked ones, applies to C02 and C03. |
| Key validity interval | `krt:validFrom`, `krt:validUntil` | Partial. KRT attaches these to an artefact; it has no class for a key. |
| Revocation entry | `krt:Revocation`, `krt:revokes` | Clean for the entry. No clean mapping for `effectiveFrom`, the time a revocation takes effect as distinct from when it was issued. R7 would also require `coversDerivedData` and a staleness bound on the revocation, which these fixtures do not carry. |
| Lineage statement | none | No clean mapping. `krt:derivedFrom` is for mandates. "Anchor succession" is proposed for KRT in ksk.md and the trust glossary but is not yet in krt.ttl. |
| Lookup record (source, fetched-at, status) | `krt:VerificationPath` with `krt:topology krt:OperatorDomain`, `krt:coupling krt:Coupled` | Partial. No property for fetched-at or for the path's status at a given time. |
| History digest in the lookup record | `krt:integrityMode krt:ContentAddressed`, `krt:contentHash` | Clean. |
| Timestamp authority | `krt:anchoredIn` | Close: a service recording an artefact's existence in time. |
| What a pass establishes | `krt:KeyControl` | Partial. A pass says a key valid for the identifier signed these bytes at that time. It does not reach `krt:AuthorityToAct`. |

## What this set does and does not establish

It establishes that a checker agreeing with `expected.json` keeps could-not-determine separate from pass and fail; uses attested signing time and never self-asserted time; tells "was valid then" from "still valid"; tells an empty revocation list from an absent one; refuses a successor key that has no signed lineage; and catches each mutation above.

It does not establish any of the following.

- **Real methods.** No DNSSEC, DANE or DID method is implemented. The source, the history format and the timestamp authority are synthetic. Mapping these rows onto a DNSSEC chain or a DID method is separate work, as Templeman noted.
- **Authority.** As Templeman put it, no key or digest check would grant execution authority. A pass here is about a key and some bytes. Authority continuity is a separate question (group D, and the cases in #22).
- **Who holds the name.** Key continuity says nothing about whether the party behind an identifier changed, the continuity-of-holding point summarised in ksk.md.
- **A source that withholds.** The history document is not signed as a whole. A source that serves a document with a revocation entry removed is not detected. That needs a signed or append-only source.
- **Compromise before the stated time.** C06 relies on the revocation's stated effective time. If compromise began earlier, the pass is wrong, and nothing in the inputs can show it.
- **The timestamp authority.** It is pinned and trusted. Its own key history, freshness and revocation are not tested.
- **Longer chains.** Only one lineage link is exercised. The checker follows longer chains, but no case tests one.
- **Normative force.** The rules here (fail outranks could-not-determine, untimed signatures judged at the evaluation instant, an unverifiable revocation gives could-not-determine) are one profile's choices, written down so they can be disputed. Corrections and alternative readings are welcome.

## Files

- `README.md`: this file.
- `expected.json`: case and mutation id to `{result, decision, reason}`.
- `check.py`: reference checker.
- `generate.py`: rebuilds `fixtures/` and `SHA256SUMS`.
- `SHA256SUMS`: digests of every fixture file.
- `fixtures/`: policy, key histories, statements, cases.
