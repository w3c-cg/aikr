# Note on the DIF Delegated Authority Evaluations

This note maps the DIF Delegated Authority Evaluations draft of 17 November 2026 to the ongoing AI KR CG trust work, led by the knowledge representation of trust note ([kroftrust.md](https://github.com/w3c-cg/aikr/blob/main/trust/kroftrust.md)), and to the AI KR CG landscape crosswalks, including the Agent Trust Protocols and Specifications Explorer and the cross-protocol use cases.

For cross-referencing (all drafts):
- Draft report on the knowledge representation of trust: https://w3c-cg.github.io/aikr/trust/kroftrust.html
- Agent Trust Protocols and Specifications Explorer, mapping ARIA, did:atp and other agent trust and identity specifications by coverage and maturity: https://w3c-cg.github.io/aikr/trust/trustinitiativeexplorer.html
- W3C AI KR Trust Record visualiser, with its Mappings tab showing which protocol fields match each part of the record: https://w3c-cg.github.io/aikr/trust/AI_Agent_Trust_Record.html#mappings
- W3C AI KR Trust Record checker: [link to be added]
- Case library of cross-protocol use cases: https://github.com/w3c-cg/aikr/blob/main/trust/trustusecases.md
- Trust KR task force, listing everyone who has contributed: https://github.com/w3c-cg/aikr/blob/main/trust/trust-kr-taskforce.md

## Overlap in brief (comments invited)

The two bodies of work overlap in part and cover different ground. The DIF report evaluates delegation and authorization specifications (OAuth, AAuth, zCaps, UCANs, KYA-OS, Cedar, AuthZEN, dSD-JWT). The AI KR CG explorer covers agent trust and identity protocols such as ARIA and did:atp. AuthZEN is the only specification in both.

Shared ground:
- Attenuated delegation (DIF criterion 1) corresponds to the AI KR authority-continuity model, where scope may narrow but not widen without explicit authorisation.
- Accountability of the agent as distinct from its operator (criterion 2) corresponds to the W3C AI KR Trust Record parties: author, operator, authoriser, owner and funder.
- DIF's advice to reject caveats the verifier cannot evaluate corresponds to the AI KR `onUnknown` relying-party policy.
- DIF's fail-closed revocation checks with a freshness verdict correspond to the AI KR three-valued evidence results (pass, fail, could-not-determine) and `stalenessBound`.
- DIF's four-layer delegation stack (identity, certificate chain, policy and caveats, signed presentation) maps onto four of the Trust Record field groups.

AI KR work that goes further: DIF finds revocation online-only in every surveyed mechanism, with no defined semantics under network partition. The AI KR resolution-dependency terms (`coupling`, `stalenessBound`, `onUnknown`) offer a way to state how a verifier behaves in that case. The evidence scale for specifications and the DNS/DID anchoring work have no counterpart in the DIF report.

DIF work that goes further: confused-deputy resistance, proof of possession, and limits on re-delegation and chain depth, none yet treated in the AI KR trust work. Delegation-chain privacy is open on both sides.

The overlap is enough for an exchange in both directions: AI KR input on the DIF future-work gaps on revocation and policy exchange, and the DIF criteria to fill the AI KR gaps. The detailed mapping follows below.

**Comments are invited** from the Trust KR task force, the DIF report's editors and contributors, and the ARIA and ATP groups. Is the mapping right? Is anything missing or misread? Please open an issue on [w3c-cg/aikr](https://github.com/w3c-cg/aikr/issues) with "DIF note" in the title, or post to public-aikr@w3.org with [trust-dif] in the subject line.

Status: working note for the Trust KR task force, open for comments. Prepared 20 November 2026.

Report: [Delegated Authority Evaluations](https://identity.foundation/delegated-authority-evaluations/), Decentralized Identity Foundation (DIF). Editors: Dmitri Zagidulin (Interop Alliance) and Juan Caballero (learningProof UG). Status given on the page: Working Group Consensus Draft, v1.0-rc1, 17 November 2026, pending DIF Steering Committee approval. Verdicts may change before the report is approved.

## What the report is

A qualitative evaluation of authorization and access control specifications, read through the lens of agentic permissions and delegation. Each specification receives a Yes, Partial or No verdict per criterion, with narrative reasoning. The report states that it does not itself specify a protocol, and it describes itself as synoptic, not exhaustive.

Companion documents: the Problem Space Report, the Threat Model, the Governance of Delegated Authority report, and an agentic-delegation user-story walk-through (video).

## Specifications evaluated

OAuth 2.0 (with RFC 9700) and the OAuth 2.1 draft; AAuth (draft-hardt-oauth-aauth-protocol); the certificate capability family (zCaps, UCANs, KYA-OS); W3C Verifiable Credentials as a way to model chained delegation; Cedar and Janssen Cedarling; AuthZEN; with dSD-JWT and AuthZed/SpiceDB in an appendix.

## Criteria

Seven required criteria, plus proof of possession as a nice-to-have:

1. Attenuated delegation
2. Accountability (distinguishing the agent from its principal or operator)
3. Confused-deputy resistance
4. Representability of authorization policies (functional, re-delegation, advisory and disclosure-governance rules)
5. Chainability
6. Cross-organizational, locally verifiable execution
7. Self-revocability
8. Proof of possession (nice-to-have)

## Merged scorecard, as published

Y = Yes, P = Partial, N = No.

| Criterion | OAuth | AAuth | zCaps | UCANs | KYA-OS | Cedar | AuthZEN | dSD-JWT |
|---|---|---|---|---|---|---|---|---|
| 1 Attenuated | P | P | Y | Y | Y | P | N | N |
| 2 Accountable | Y | Y | P | P | Y | Y | P | P |
| 3 Confused deputy | P | Y* | Y | Y | Y | N | N | P |
| 4 Policies | P | P | P | P | P | Y | P | N |
| 5 Chainable | P | Y | Y | Y | Y | N | N | Y |
| 6 Cross-org / local | Y | Y | Y | Y | P | P | N | Y |
| 7 Self-revocable | P | P | Y | Y | P | P | P | N |
| 8 Proof of possession | Optional | Y | Y | Y | Y | N | N | Y |

\* AAuth is Yes in three of its four modes; the identity-based mode is ambient authority.

W3C Verifiable Credentials receive no per-criterion verdicts. The report finds that a VC has no parent, chain or attenuation rule, so chaining must be modelled in the payload, and it places VCs at the root of a chain, binding the operator to the first delegation.

## Main findings

- The specifications fall into three families: certificate capabilities (zCaps, UCANs, KYA-OS), server-mediated authorization (OAuth, AAuth) and policy decision systems (Cedar, AuthZEN).
- The capability family is the only one the report considers viable as the backbone of the authority flow: it alone meets the chain criteria offline and holder-side.
- No specification is complete: each has at least one Partial or No among criteria 1 to 7.
- Shared gaps: no specification ships a vocabulary for delegation-control policy (e.g. "do not delegate further"); revocation is online-only in every surveyed mechanism, with no defined semantics under network partition; delegation-chain privacy is left as future work.
- Recommended direction: compose a delegation stack from four layers (identity as entry point, certificate chain for the authority flow, policy and caveats for restrictions, signed presentation for possession). The report sees the near-term work as composition, with no need for a competing specification. AuthZEN alone should not be the basis for access decisions in a delegation stack, since it is ambient authority.

Gaps listed for future work, in the order the report gives: a standard policy and caveat vocabulary for delegation control (time windows, re-delegation and depth limits); an advisory tier for requests recorded but not enforced; agent-versus-operator semantics and identity binding that survive cross-organizational, multi-hop delegation; offline and decentralized revocation under network partition; cross-organizational policy exchange with agreed semantics.

## Relevance to the trust work

**Proposed mapping of the DIF criteria to the W3C AI KR Trust Record field groups** (for discussion, not from the report):

| DIF criterion | W3C AI KR Trust Record field group |
|---|---|
| 1 Attenuated delegation | Mandate and authority |
| 2 Accountability (agent vs operator) | Parties |
| 3 Confused-deputy resistance | Mandate and authority, Policy |
| 4 Representability of policies | Policy |
| 5 Chainability | Mandate and authority |
| 6 Cross-org, locally verifiable | Interface and keys, Evidence |
| 7 Self-revocability | Lifecycle |
| 8 Proof of possession | Interface and keys |

**Links to [trustusecases.md](https://github.com/w3c-cg/aikr/blob/main/trust/trustusecases.md):**

- UC-01 (action exceeds authority) tests criterion 1.
- UC-02 (revocation with cached evidence) tests criterion 7. The report recommends fail-closed revocation checks with a freshness verdict.
- UC-05 (pseudonymous or pairwise identifier) matches the report's recommendation of ephemeral or pairwise identifiers per delegation, with identity mapping held out of band for auditors.
- UC-07 (copied or replayed credential) tests criterion 8. The report recommends a separate per-request proof whose key matches the leaf delegatee.
- UC-09 (hiring agent) touches criterion 2 and the agent-versus-operator gap the report lists for future work.

**Differences from the AIKR explorer and use cases:**

- The report covers authorization and delegation specifications; the explorer covers agent trust and identity protocols. Overlap is limited to AuthZEN.
- ARIA and did:atp, both in the explorer, are not among the evaluated specifications.
- The report is a qualitative review by its editors. The explorer adds an evidence scale (documented, author-published, independently reproduced); the use cases evaluate one scenario across protocols.

## Mapping to the AIKR trust work

Proposed for discussion. The AIKR side is taken from the draft report on the knowledge representation of trust ([kroftrust.html](https://w3c-cg.github.io/aikr/trust/kroftrust.html)), the W3C AI KR Trust Record, the explorer and trustusecases.md. Status: **aligned** (both cover it), **AIKR adds** (AIKR covers ground the DIF report does not score), **gap** (the DIF report raises it, the AIKR trust work does not yet treat it).

### DIF criteria

| DIF criterion | AIKR artefact and terms | Status |
|---|---|---|
| 1 Attenuated delegation | Authority-continuity model: scope may narrow but not widen without explicit authorisation, with four proposed cases. W3C AI KR Trust Record: Mandate and authority. UC-01. | Aligned. The DIF per-hop attenuation invariant could be added to the authority-continuity cases. |
| 2 Accountability (agent vs operator) | W3C AI KR Trust Record parties: author, operator, authoriser, owner, funder. KRT `krt:issuingPrincipal`, `krt:controllingPrincipal`. Explorer finding that few specifications separate developer, deployer, owner and funder. UC-09. | Aligned; AIKR adds owner and funder roles. Principal ranges in KRT still open (issue #19). |
| 3 Confused-deputy resistance | No dedicated treatment. Closest: the trust decision's authority and enforcement-location dimensions. | Gap. |
| 4 Representability of policies | Relying-party `onUnknown` policy; verifier-set staleness bounds where publishers declare none; oversight records (observed, checked, decided, released), PR #15. | Partly aligned. DIF's advisory tier (recorded, not enforced) may correspond to the "observed" oversight record; to be checked. |
| 5 Chainability | Per-hop verification in delegation chains, with compounding latency and the chain-depth formula 1 − 0.99^d. | AIKR adds: the availability cost of verifying a chain, which the DIF scorecard does not measure. |
| 6 Cross-org, locally verifiable | Resolution dependency (where an identity document is fetched from at verification time); `coupling`; integrity mode (content-addressed integrity vs location-bound availability); DNS/DID note. | AIKR adds: what local verification depends on. A specification can score Yes here and still fetch its documents over DNS and the WebPKI. |
| 7 Self-revocability | `stalenessBound` (longest window a revoked or superseded artefact can still verify), issue #8 on superseded artefacts; key and evidence states; UC-02. | Aligned, and AIKR offers a frame for DIF's open problem (next table). |
| 8 Proof of possession | Not defined in the trust note. Key publisher field (who publishes the key set a verifier trusts); key-to-domain binding checks; UC-07. | Gap for the mechanism; the use case is in place. |

### DIF findings, recommendations and future-work gaps

| DIF item | AIKR counterpart | Status |
|---|---|---|
| Revocation is online-only; no semantics under network partition (future-work gap 4) | Resolution dependency as a PACELC position: coupled vs decoupled verification paths, `stalenessBound`, `onUnknown`, `coupling`. | AIKR adds: a vocabulary for stating how a verifier behaves when it cannot reach the revocation source. Worth offering to DIF. |
| Use fail-closed revocation checks with a freshness verdict | Three-valued evidence results (pass, fail, could-not-determine) across the key and evidence state cases; `onUnknown`; `stalenessBound`. | Aligned. AIKR's "could-not-determine" state makes the freshness verdict explicit. |
| Reject caveats the verifier cannot evaluate | `onUnknown` relying-party policy. | Aligned. |
| Cross-organizational policy exchange with agreed semantics (gap 5) | Comparison semantics: term-level crosswalks fail behaviourally; canonical-form version and declared semantics; vocabulary crosswalk. | AIKR adds: evidence that agreed terms are not enough without declared comparison semantics. |
| Agent-vs-operator semantics across multi-hop delegation (gap 3) | W3C AI KR Trust Record parties; KRT principal properties (issue #19). | Aligned, open on both sides. |
| Standard caveat vocabulary: time windows, re-delegation and depth limits (gap 1) | Authority-continuity model covers narrowing; no vocabulary for re-delegation or depth limits. | Gap. |
| Delegation-chain privacy left as future work | Not treated. UC-05 covers pairwise identifiers, not chain privacy. | Gap on both sides. |
| Ephemeral or pairwise identifiers per delegation | UC-05; did:atp pairwise identifiers in the explorer. | Aligned. |
| Four-layer stack: identity, certificate chain, policy and caveats, signed presentation | W3C AI KR Trust Record field groups: Identity; Mandate and authority; Policy; Interface and keys. | Aligned. The W3C AI KR Trust Record also carries Parties, Lifecycle and Evidence as their own groups. |

### AIKR work with no counterpart in the DIF report

- Resolution dependency and anchoring path (ledger, DNS, DID), including the DNS/DID note and the root KSK rollover.
- The evidence scale for specifications (documented, author-published, independently reproduced).
- Notes on Base L2, "Trust Without Trusting" and the Agent Identity Protocol.
- Trust in non-agentic AI (trustinai(non_agentic).md).

## Suggested actions for the task force

1. Add the report to the explorer's corollary initiatives, with its status and date, and update the DIF entry in the trust note's landscape section.
2. Consider adding the DIF criteria as a view in the explorer, using the mappings above once agreed.
3. Close the gaps on the AIKR side: add confused-deputy resistance and proof of possession to the trust decision or the W3C AI KR Trust Record, and add re-delegation and depth limits to the authority-continuity cases.
4. Offer the AIKR resolution-dependency terms (`stalenessBound`, `onUnknown`, `coupling`) and comparison semantics to DIF as input on its future-work gaps on revocation under partition and cross-organizational policy exchange.
5. Invite the report's editors to comment on the mapping and on trustusecases.md.
6. Invite the ARIA and ATP groups to self-assess against the seven DIF criteria, so their entries can be read next to the published scorecard.

Comments: open an issue on [w3c-cg/aikr](https://github.com/w3c-cg/aikr/issues) with the file name in the title.
