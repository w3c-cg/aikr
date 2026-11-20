# Note on the DIF Delegated Authority Evaluations

This note maps the [DIF Delegated Authority Evaluations draft](https://identity.foundation/delegated-authority-evaluations/) of 17 November 2026 (v1.0-rc1, Decentralized Identity Foundation, Trusted AI Agents Working Group) to the ongoing AI KR CG trust work, led by the knowledge representation of trust note ([kroftrust.md](https://github.com/w3c-cg/aikr/blob/main/trust/kroftrust.md)), and to the AI KR CG landscape crosswalks, including the Agent Trust Protocols and Specifications Explorer and the cross-protocol use cases.

For cross-referencing (all drafts):
- Draft report on the knowledge representation of trust: https://w3c-cg.github.io/aikr/trust/kroftrust.html
- Agent Trust Protocols and Specifications Explorer, mapping ARIA, did:atp and other agent trust and identity specifications by coverage and maturity: https://w3c-cg.github.io/aikr/trust/trustinitiativeexplorer.html
- W3C AI KR Trust Record visualiser, with its Mappings tab showing which protocol fields match each part of the record: https://w3c-cg.github.io/aikr/trust/AI_Agent_Trust_Record.html#mappings
- W3C AI KR Trust Record checker: [link to be added]
- Case library of cross-protocol use cases: https://github.com/w3c-cg/aikr/blob/main/trust/trustusecases.md
- Trust KR task force, listing everyone who has contributed: https://github.com/w3c-cg/aikr/blob/main/trust/trust-kr-taskforce.md

## Contents

- [Overlap in brief (comments invited)](#overlap-in-brief-comments-invited)
- [What the report is](#what-the-report-is)
- [Specifications evaluated](#specifications-evaluated)
- [Criteria](#criteria)
- [Merged scorecard, as published](#merged-scorecard-as-published)
- [Main findings](#main-findings)
- [Relevance to the trust work](#relevance-to-the-trust-work)
- [Mapping to the AIKR trust work](#mapping-to-the-aikr-trust-work)
  - [DIF criteria](#dif-criteria)
  - [DIF findings, recommendations and future-work gaps](#dif-findings-recommendations-and-future-work-gaps)
  - [AIKR work with no counterpart in the DIF report](#aikr-work-with-no-counterpart-in-the-dif-report)
- [Suggested actions for the task force](#suggested-actions-for-the-task-force)

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

**People in both.** Members of the AI KR CG, and of other W3C groups the AI KR CG shares its trust work with, take part in the DIF work on delegated authority:

- Nicola Gallo, an AI KR CG participant, co-chairs the DIF Trusted AI Agents Working Group, the group listed as producing the delegated authority reports. Sources: [AI KR CG participants](https://www.w3.org/groups/cg/aikr/participants/); [DIF Trusted AI Agents WG](https://identity.foundation/working-groups/trusted-agents.html); [LF Decentralized Trust announcement naming the chairs](https://www.lfdecentralizedtrust.org/blog/toip-and-dif-announce-three-new-working-groups-for-trust-in-the-age-of-ai).
- Victor Lu, an AI KR CG and ATP CG participant, is an author of the companion Governance of Delegated Authority report. Sources: [AI KR CG participants](https://www.w3.org/groups/cg/aikr/participants/); [ATP CG participants](https://www.w3.org/groups/cg/atp/participants/); [Governance of Delegated Authority report](https://identity.foundation/governance-of-delegated-authority-report/).

Alan Karp (SitePassword) is linked to both through Victor Lu: he contributed to the evaluation draft, contributed to the companion threat model, and edits the Governance of Delegated Authority report that Victor Lu co-authors. DIF describes his access management use cases as a key conceptual foundation for the Trusted AI Agents WG approach. He does not appear in the AI KR, ATP or ARIA CG participant lists. Sources: [evaluation draft](https://identity.foundation/delegated-authority-evaluations/); [Governance of Delegated Authority report](https://identity.foundation/governance-of-delegated-authority-report/); [threat model](https://identity.foundation/delegated-authority-threat-model/); [DIF blog, Authorising Autonomous Agents at Scale](https://blog.identity.foundation/building-ai-trust-at-scale-4/).

None of the editors or named contributors of the evaluation draft itself appears in the AI KR CG participant list ([editors and contributors](https://identity.foundation/delegated-authority-evaluations/)). The comparison covers named authors and chairs only, since the DIF working group's membership is not public, and it matches names, not confirmed identities.

**Comments are invited** from the Trust KR task force, the DIF report's editors and contributors (Alan Karp's view on the case library would be especially welcome, given his access management use cases), and the ARIA and ATP groups. Is the mapping right? Is anything missing or misread? Please open an issue on [w3c-cg/aikr](https://github.com/w3c-cg/aikr/issues) with "DIF note" in the title, or post to public-aikr@w3.org with [trust-dif] in the subject line.

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

## Comments received

### From an implementation of a gateway conformance harness (21 November 2026)

Contributed by Xinghua Zhao, from work on a conformance harness and an A2A gateway adapter. Offered as implementation evidence, not as a verdict on the note; take what is useful and discard the rest.

1. **Criterion 1 (attenuation) needs a runtime record, not only a model.** The authority-continuity model says scope may narrow but not widen. In the gateway the useful artefact turned out to be a per-request decision record: which scope was claimed, which scope was effective, and on what basis. When the caller declares no scope, the basis is recorded as `transport-peer` rather than silently granting. Suggestion: add "effective scope basis must be recorded per request" to the attenuation cases.

2. **Criterion 3 (confused deputy) is content-mediated as well as policy-mediated.** The adapter had to reject inline instruction-override, role spoofing, tool spoofing and opaque encodings before forwarding, because a deputy can be confused by the payload while holding a valid mandate. The scorecard reads criterion 3 as a policy property; a content-level row would make that gap visible. This one concerns the DIF scorecard rather than the mapping, and has been sent to the report's editors as well.

3. **Revocation under partition: a three-valued verdict is enough to start.** DIF lists "no defined semantics under network partition" as future-work gap 4. The minimum usable form is pass / fail / could-not-determine, plus a bound on how old the last successful check may be. The harness exposes exactly that (state and clause in the error data, 403 on any disabled or unknown state), and it is testable from outside without reading the code.

4. **"Locally verifiable" can hide a resolution dependency.** Criterion 6 scores Yes for mechanisms that still fetch identity documents over DNS and the WebPKI at verification time. Suggest one column, "what must be reachable at verification time". This also concerns the DIF scorecard and has been sent to the editors.

5. **Evidence scale: the level exists; what is missing is the record.** Correction accepted — the explorer already carries independently reproduced as its third level. The narrower suggestion is that each claim at that level record *who* executed the run, *at which commit or artefact hash*, and *from which vantage point*, since our first external run was valuable only because the hash matched and the commit was pinned.

6. **On the four-layer stack:** composition looks like the near-term work. One addition from practice: the policy-and-caveats layer needs a vocabulary before it needs a format. The harness encodes delegation limits as enumerated caveat names from a closed set, because free-text caveats are unevaluable by the relying party — the same point DIF makes about rejecting caveats the verifier cannot evaluate.

Reproduction link for the implementation: <https://github.com/zhaoxinghua09-cell/uibc-core>

Comments: open an issue on [w3c-cg/aikr](https://github.com/w3c-cg/aikr/issues) with the file name in the title.
