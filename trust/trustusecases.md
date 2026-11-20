# Cross-protocol use cases for agent trust (tentative draft)

Status: tentative draft for discussion by the Trust KR task force. Not a CG Report, and no consensus is implied. New use cases are invited: see [How to contribute](#how-to-contribute).

Purpose: one shared scenario, evaluated against each agent trust protocol, so readers can see what each protocol checks, what evidence it records, and what it leaves to the application. Every scenario uses the same template, so results can be compared side by side and linked to the coverage matrix in the [Agent Trust Protocols and Specifications Explorer](https://w3c-cg.github.io/aikr/trust/trustinitiativeexplorer.html) and the field groups of the [AI Agent Trust Record](https://w3c-cg.github.io/aikr/trust/AI_Agent_Trust_Record.html).

Sources: the scenarios come from use cases proposed on the public-aikr and public-agent-identity lists by Larry Lewis (ATP CG chair) and from the ARIA CG discussion led by Adolfo Grego Micha (ARIA CG chair). The source of each scenario is given under it. The pre-filled protocol cells repeat only what the protocol's own authors stated in those posts. They have not been checked against the specifications and should be confirmed or corrected by the protocol owners.

## How to read and fill a scenario

Each scenario records:

- **Scenario**: what happens
- **Expected decision**: what a conforming verifier should conclude
- **Evidence to record**: what the decision must rest on
- **Trust Record field groups**: Identity, Interface and keys, Mandate and authority, Policy, Parties, Lifecycle, Evidence
- **Protocol evaluation**: one row per protocol, with what the protocol does, what it leaves to the application, and an evidence level

Evidence levels follow the explorer:
1 = described in the specification text only; 2 = results published by the protocol authors; 3 = independently reproduced.
"Stated by authors" means the cell repeats a claim made on a mailing list, not yet checked against the specification or a test.

Protocol owners: please replace "to be completed" with your own entry, cite the section of your specification, and give a test or fixture link where one exists.

---

## UC-01 Action exceeds the agent's authority

Source: Larry Lewis, "Re: DNS vs DID in the Trust Layer", public-aikr / public-agent-identity, 11 Nov 2026.

- **Scenario**: a valid agent credential is presented, but the requested action exceeds the authority it grants.
- **Expected decision**: refuse the action, and do not treat the credential as invalid.
- **Evidence to record**: the credential, the authority it grants, the action requested, the rule that refused it.
- **Field groups**: Mandate and authority, Policy.

| Protocol | What the protocol does | Left to the application | Evidence level |
|---|---|---|---|
| ARIA 1.0 / ARIA AP | Scopes express declared capabilities. The recipient checks the required scope and applies its own rules on permitted resources, amounts or actions. Scope names use three segments, e.g. `payments:transfer:create`. | The recipient's own limits on resources and amounts. | Stated by authors (Adolfo, 19 Nov) |
| ATP (did:atp, mandates) | Draft work on portable, bounded and revocable authorization mandates. Runtime policy profiles evaluate proposed actions before execution. | To be completed | Stated by authors (Larry, 17 Nov) |
| Other protocols | To be completed | | |

## UC-02 Revocation while cached evidence remains

Source: Larry Lewis, 11 Nov 2026 (as above).

- **Scenario**: a credential or authorization is revoked, while the verifier still holds evidence fetched before the revocation.
- **Expected decision**: refuse the action once revocation is known. Make clear how fresh the status evidence must be.
- **Evidence to record**: status source, time of the status check, freshness rule applied.
- **Field groups**: Lifecycle, Evidence.

| Protocol | What the protocol does | Left to the application | Evidence level |
|---|---|---|---|
| ARIA 1.0 / ARIA AP | Status checks run against the specific credential, not only the agent's DID. Any change to a credential (e.g. its scope) revokes it and issues a new one. aria.bar/verify shows each credential's status with issue and revocation times. | Caching and freshness policy: to be confirmed. | Stated by authors (Adolfo, 13 and 19 Nov) |
| ATP | Credential lifecycle specifications. The authors state that the integrations do not yet establish production-grade mandate revocation. | To be completed | Stated by authors (Larry, 17 Nov) |
| Other protocols | To be completed | | |

## UC-03 Unknown issuer, substituted key or unavailable status

Source: Larry Lewis, 11 Nov 2026 (as above). Related questions on the issuer-key discovery path are in [DNS_and_DIDTrustforAgents.md](https://github.com/w3c-cg/aikr/blob/main/trust/DNS_and_DIDTrustforAgents.md).

- **Scenario**: the verifier meets an issuer it does not know, a key that has been substituted, or a status service that does not respond.
- **Expected decision**: refuse, and record which of the three conditions applied. A correct signature under the wrong key is not a pass.
- **Evidence to record**: how the issuer key was obtained and from where, which trust anchor was used, the status query result.
- **Field groups**: Interface and keys, Identity, Evidence.

| Protocol | What the protocol does | Left to the application | Evidence level |
|---|---|---|---|
| ARIA 1.0 / ARIA AP | The SDK trusts no issuer automatically. Trusted issuers and keys are configured explicitly. A demonstration issuer key set has been published with a fingerprint. Credentials carry a composite signature: both ML-DSA-65 and Ed25519 must verify. | Choosing which issuers to trust. | Stated by authors (Adolfo, 19 Nov) |
| ATP | To be completed | | |
| Other protocols | To be completed | | |

## UC-04 Human approval missing, expired or bound to another action

Source: Larry Lewis, 11 Nov 2026 (as above).

- **Scenario**: an operation requires human approval, but the approval is missing, has expired, or was given for a different action.
- **Expected decision**: refuse the action.
- **Evidence to record**: the approval, who gave it, when, and for which action.
- **Field groups**: Mandate and authority, Parties, Policy.

| Protocol | What the protocol does | Left to the application | Evidence level |
|---|---|---|---|
| ARIA 1.0 / ARIA AP | When a scope is listed in `hitlRequired`, ARIA AP refuses the attempt unless the application supplies matching, unexpired approval evidence from its trusted approval system. | Proving that an authorized human approved. ARIA AP 1.0 defines no interoperable signed approval format and no pending-approval workflow. The receipt carries no proof of approval. | Stated by authors (Adolfo, 19 Nov) |
| ATP | In the authors' local testing of the Claude Code integration, ATP enforced approval requirements and recorded signed audit entries. | To be completed | Stated by authors (Larry, 17 Nov) |
| Other protocols | To be completed | | |

## UC-05 Pseudonymous or pairwise identifier

Source: Larry Lewis, "Re: call for co chairs for the AI KR CG", 18 Nov 2026, task force plan item 3.

- **Scenario**: an agent acts under a pseudonymous or pairwise identifier, without exposing the human or organisation behind it.
- **Expected decision**: accept only if trust evidence and authorization stay bound to the right subject and context.
- **Evidence to record**: the identifier, how it is derived, what binds it to the evidence presented.
- **Field groups**: Identity, Parties.

| Protocol | What the protocol does | Left to the application | Evidence level |
|---|---|---|---|
| ARIA 1.0 / ARIA AP | Distinguishes the agent's stable DID from the identifier of each individual credential. Support for pairwise identifiers: to be confirmed. | To be completed | Stated by authors (Adolfo, 19 Nov) |
| ATP (did:atp) | Pairwise identifiers. An independent implementer reproduced 11 of 11 identifier and pairwise-derivation test vectors. The authors note this does not cover DID resolution, DID Document verification, signatures or request binding. | To be completed | 3 for identifier syntax, fingerprints and pairwise derivation (w3c-cg/atp issue #8). Otherwise to be completed |
| Other protocols | To be completed | | |

## UC-06 Credential renewal and key change

Source: Larry Lewis, 18 Nov 2026 (DNS/DID comparison item); Adolfo Grego Micha, 13 Nov 2026.

- **Scenario**: a credential expires and is renewed, or a key is rotated, and a verifier must link the new credential to the old one.
- **Expected decision**: accept the renewed credential only if its link to the previous one can be verified, and treat any change of authority as a new grant.
- **Evidence to record**: the previous credential, the link between the two, and what changed.
- **Field groups**: Lifecycle, Interface and keys.

| Protocol | What the protocol does | Left to the application | Evidence level |
|---|---|---|---|
| ARIA 1.0 / ARIA AP | `previousCredentialId` links renewals. A renewal is linked to the previous credential only when the scopes are unchanged; any other change revokes the credential and issues a new one. | To be completed | Stated by authors (Adolfo, 13 and 19 Nov) |
| ATP | To be completed | | |
| Other protocols | To be completed | | |

## UC-07 Copied or replayed credential

Source: Adolfo Grego Micha, "Updates after Nov 17th meeting", public-agent-identity, 19 Nov 2026.

- **Scenario**: someone who copied a credential, or knows its URL, submits a request with it.
- **Expected decision**: refuse, because the sender cannot prove possession of the private key.
- **Evidence to record**: the challenge, the request signature, what the signature binds (destination, operation, credential, content).
- **Field groups**: Interface and keys, Evidence.

| Protocol | What the protocol does | Left to the application | Evidence level |
|---|---|---|---|
| ARIA AP | The agent first verifies the recipient, then signs its HTTP request under an RFC 9421 profile using a one-time challenge. The signature binds destination, operation, credential and, where applicable, content. These request signatures use Ed25519 and are not post-quantum. | To be completed | Stated by authors (Adolfo, 19 Nov) |
| ATP | The authors state that request binding is not yet covered by the independent did:atp validation. | To be completed | To be completed |
| Other protocols | To be completed | | |

## UC-08 Admitted, executed or disputed later

Source: Adolfo Grego Micha, 19 Nov 2026 (as above).

- **Scenario**: an operation is admitted, and later a third party needs to establish whether it was executed and under what authority.
- **Expected decision**: distinguish "admitted for processing", "completed" and "rejected", and say what a receipt does and does not prove.
- **Evidence to record**: signed receipt, its link to the request, the credential in force, any independent timestamp.
- **Field groups**: Evidence, Lifecycle, Parties.

| Protocol | What the protocol does | Left to the application | Evidence level |
|---|---|---|---|
| ARIA AP | One signed receipt format, `aria-ap-receipt/1`, signed by the recipient and linked to the request, distinguishing accepted, completed and rejected. A third party can later verify the receipt with the necessary evidence. The authors note this does not prove the effect occurred outside the recipient's system, gives no independent timestamp and is not a complete authorization history. | Durable storage, retrieval and avoiding duplicate effects. TLF and agent.bar keep no central transaction archive. | Stated by authors (Adolfo, 19 Nov) |
| ATP | Signed audit entries recorded in the authors' integration testing. | To be completed | Stated by authors (Larry, 17 Nov) |
| Other protocols | To be completed | | |

## UC-09 Hiring agent acting for an organisation

Source: ARIA CG hiring use case thread, "Introduction and a hiring use case for the registry", public-agent-identity, Oct–Nov 2026, with contributions from Prasanna Bableshwar, Xinghua (Steven) Zhao, Yanfeng Liu, Raphael La Touche and Dick Brooks. The working text is the v0.2 Registry Write-up, linked in Adolfo's post of 19 Nov. This draft has not been checked against that document.

- **Scenario**: an agent takes part in a hiring process for an organisation. Later, someone needs to know which operator and accountable organisation stood behind it, and whether its credential was in force when it acted.
- **Expected decision**: answer "what was in force at the time of the action", not only "what is in force now".
- **Evidence to record**: operator and accountable organisation, the credential at the time of the action, and the revocation state with its evaluation time. The thread proposes five revocation states: recorded, not recorded, query failed, cross-federation unsynchronised, undetermined. It also asks for a timestamp and evidence pointer on each value, and for revocation events to be signed and append-only.
- **Field groups**: Parties, Lifecycle, Evidence.

| Protocol | What the protocol does | Left to the application | Evidence level |
|---|---|---|---|
| ARIA 1.0 / ARIA AP | Credential status, with issue and revocation times, is shown at aria.bar/verify. The full lifecycle ledger is private to each account; users can be added to an account with view permissions for audit. | To be completed | Stated by authors (Adolfo, 13 Nov) |
| ATP | To be completed | | |
| Other protocols | To be completed | | |

---

## Open questions for the task force

- Which other protocols from the explorer should be evaluated first (e.g. WIMSE, AuthZEN, Web Bot Auth)?
- Should each scenario get a machine-readable fixture in the repository, building on the existing key and evidence state fixtures?
- Who confirms each protocol row: the protocol owners, an independent reviewer, or both?

## How to contribute

New use cases are welcome. To propose one, open an issue on [w3c-cg/aikr](https://github.com/w3c-cg/aikr/issues) with "trustusecases.md: new use case" in the title, and describe the scenario, the expected decision and the evidence it rests on. It will be added with the next free ID.

To complete or correct an existing entry, open an issue with the scenario ID (e.g. UC-04) and the protocol name in the title, or post to public-aikr@w3.org with [trust-usecases] in the subject line.
