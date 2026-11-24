# Trust KR Task Force

*Draft mission statement, proposed to the W3C AI Knowledge Representation Community Group in November 2026. Proposed start date effective asap.
To be discussed and agreed by CG participants on public-aikr.*

*Part of the AI KR CG trust work. Main document: [The Knowledge Representation of the Trust Layer](kroftrust.md). Trust record visualiser: [W3C AI KR Trust Record](https://w3c-cg.github.io/aikr/trust/AI_Agent_Trust_Record.html). Case library: [trustusecases.md](trustusecases.md). Mapping to the DIF delegated authority work: [DIFdelegateauth.md](DIFdelegateauth.md).*

## Mission

Produce a human-readable representation of the dimensions of trust in AI systems, covering AI in general, machine learning models, large language models and AI agents, so that a person relying on such a system, an auditor or a regulator can see what a trust judgement rests on and which parts of it nobody has checked.

## Goal

- Name and define the dimensions of trust, starting from the work already in this folder: the technical note, the KRT ontology, the trust record and visualiser, the use cases, the test material and the notes on trust anchors.
- Cover each kind of system in scope: AI in general, machine learning models, large language models and AI agents. Most of the material in this folder was written for agents; mark which dimensions carry over to the other kinds of system and add the ones they need.
- Present each dimension in plain language, readable without a technical background, and trace it to the machine-readable terms in KRT.
- Connect and align with other W3C Community Groups and organisations working on AI, machine learning, large language models, agents, identity, protocols and trust, to harmonise schemas.
- Feed the result into the Community Group report on the trust layer ([draft](https://w3c-cg.github.io/aikr/trust/kroftrust.html)).

## Process

- Each work item has one or more co-leads from among the contributors. A co-lead curates the issues and files for that item in this folder.
- Work happens in the open, through issues and pull requests on [w3c-cg/aikr](https://github.com/w3c-cg/aikr) and posts to public-aikr@w3.org with `[trust-kr]` in the subject.
- Contributors are AI KR CG participants with their GitHub and W3C accounts linked, so the IPR check passes.
- Decisions are taken by consensus on the list, and the chair merges after a review period.

## Communication

About once a quarter, the task force sends a short note to the AI KR CG list: what was done, what is open, and which decisions the CG needs to take.

## Coordination

Larry Lewis volunteered to co-lead and coordinate the task force at the AI KR CG group call of 17 November 2026, and agreed to work with the contributors who had already expressed interest. Draft minutes of the call, for approval: [Google Doc](https://docs.google.com/document/d/1I6VeIVD3EPbw-q5jgQtlfDU3bYRDgBXLJ7yP1MV4uAQ/edit?usp=sharing), circulated on [public-aikr on 18 November 2026](https://lists.w3.org/Archives/Public/public-aikr/2026Nov/0050.html)   Nicholas Templeman also agreed to co-lead and coordinate the task force with an email to Larry and Paola.
Larry and Nicholas will maintain the Taskforce repo https://github.com/w3c-cg/aikr-trust  from 24th November onwards.

## Invited co-leads

Everyone below has contributed to the trust work and is invited to co-lead. To take up a work item, reply on the list or write to the chair to agree its scope.

| Contributor | Contribution to the trust work |
| --- | --- |
| Isaac Mao | Integrity and availability axis, and evidence resolution (§3.1 of the note, PR #7) |
| Amey Parle | Comparison semantics (§4.1 and `comparison-semantics.md`, PR #11) |
| Ankur Chrungoo | Typed integrity and staleness attributes (issue #8) and resolution dependency as a PACELC position (§3.2, PR #14) |
| Kenne Ives | Key and evidence states (PR #25), evidence resolution (issue #10), tracker of open items (issue #16), test vectors for the trust record |
| Nicholas Templeman | Proposal for the trust-state vocabulary and fixture table (public-aikr) |
| Michael Blake | Review of the key and evidence states, deployment evidence from agent-payment discovery (issue #12), fixes to the DNS and DID note (issue #26) |
| Nicola Gallo | Authority continuity: formal model and proposed cases (PR #22). Also co-chairs the DIF Trusted AI Agents Working Group (see [related contributions elsewhere](#related-contributions-elsewhere)) |
| Evgenii Arsentev | Pointer to the Agent Conformance reporting format (PR #13) |
| Andreas Ehstand | Oversight records in KRT (PR #15, open) |
| Sean (LexLint) | Corrections to KRT (issue #19) and review of the oversight records |
| Lars Kroehl | Correction to Annex B on did:moltrust resolution (issue #9) |
| Yanfeng Liu | Answers to the six questions of the note (issue #5), review of the trust record for audit and accountability |
| Larry Lewis | Co-lead and coordinator of the task force (volunteered at the AI KR CG call of 17 November 2026, see [coordination](#coordination)); review of the trust record model |
| Francesco Marinoni Moretto | Commerce identity rows and the Key publisher field of the trust record (issue #28) |
| bigblackcoder same as Larry Lewis of ATP (GitHub) | Review of the DNS and DID note (issue #27) and the ATP demonstration package (issue #29) |

## Related contributions elsewhere

AI KR CG participants who are making related trust contributions in other groups, proposed for inclusion in the task force by extension. Inclusion is pending their agreement; each is invited to reply on the list or write to the chair to agree scope. Names are matched against public participant lists and author credits, not confirmed identities.

| Name | Related contribution | Possible area in the task force | Source |
| --- | --- | --- | --- |
| Nicola Gallo (already listed above) | Co-chair, DIF Trusted AI Agents Working Group, the group producing the delegated authority reports and the evaluation draft | Alignment with DIF on delegated authority and authorization | [DIF Trusted AI Agents WG](https://identity.foundation/working-groups/trusted-agents.html); [LF Decentralized Trust announcement](https://www.lfdecentralizedtrust.org/blog/toip-and-dif-announce-three-new-working-groups-for-trust-in-the-age-of-ai) |
| Victor Lu | Author, DIF Governance of Delegated Authority report; also an ATP CG participant | Governance of delegated authority, oversight records | [Governance of Delegated Authority report](https://identity.foundation/governance-of-delegated-authority-report/); [AI KR CG participants](https://www.w3.org/groups/cg/aikr/participants/) |

### Contributors in related W3C trust groups, invited by extension

| Name | Related contribution | Possible area in the task force | Source |
| --- | --- | --- | --- |
| Alan Karp | Contributor, DIF Delegated Authority Evaluations draft and threat model; editor, DIF Governance of Delegated Authority report; active on the W3C AI Agent Protocol CG and Credentials CG lists | Delegated authority, access management use cases, review of [trustusecases.md](trustusecases.md) | [Evaluation draft](https://identity.foundation/delegated-authority-evaluations/); [Governance report](https://identity.foundation/governance-of-delegated-authority-report/) |

Mapping of the DIF work to the AI KR trust work: [DIFdelegateauth.md](DIFdelegateauth.md)

## Handover notes

Open items passed to the task force when it starts work.

- **ATP demonstration package ([issue #29](https://github.com/w3c-cg/aikr/issues/29)).** A 22-scenario assessment harness for the trust record, published for independent rerun. All 22 scenarios passed when run by the contributor. List it in the Implementation reports table of the [visualiser specification](https://w3c-cg.github.io/aikr/trust/trustvisualiser.html), with status "Run by the contributor", and change the status to "Independently rerun" once someone else reruns it.
- **Key and evidence states ([PR #25](https://github.com/w3c-cg/aikr/pull/25)).** The contributor reports that all eleven cases and eleven mutation controls match `expected.json`. Consider citing the result in the report and inviting runs in other languages.
- **Contributor names.** Confirm whether the GitHub account bigblackcoder (issues #27 and #29) belongs to Larry Lewis, and if so merge the two entries in the co-lead table and in the report.
- **Corrections to the technical note.** Annex B on did:moltrust resolution ([issue #9](https://github.com/w3c-cg/aikr/issues/9)); source pool numbers 17 to 19 used twice.
- **Pending contributions.** English summary of the Agent Community answers ([issue #5](https://github.com/w3c-cg/aikr/issues/5)); oversight records in KRT ([PR #15](https://github.com/w3c-cg/aikr/pull/15)); comments on KRT ([#19](https://github.com/w3c-cg/aikr/issues/19)), the DNS and DID note ([#26](https://github.com/w3c-cg/aikr/issues/26), [#27](https://github.com/w3c-cg/aikr/issues/27)) and the trust record ([#28](https://github.com/w3c-cg/aikr/issues/28)).
- **Housekeeping.** `aria2.html` duplicates `aria.html`; the visualiser page has no link back to the technical note.

### Open items from the DIF Delegated Authority Evaluations note

Proposed in [DIFdelegateauth.md](DIFdelegateauth.md), which maps the [DIF Delegated Authority Evaluations draft](https://identity.foundation/delegated-authority-evaluations/) (17 November 2026) to the AI KR trust work. Open for co-leads to take up.

- [ ] Add the DIF report to the explorer's corollary initiatives, with its status and date, and update the DIF entry in the landscape section of the trust note.
- [ ] Consider adding the DIF criteria as a view in the explorer, using the mappings in the note once agreed.
- [ ] Close the gaps on the AI KR side: add confused-deputy resistance and proof of possession to the trust decision or the W3C AI KR Trust Record, and add re-delegation and depth limits to the authority-continuity cases.
- [ ] Offer the AI KR resolution-dependency terms (`stalenessBound`, `onUnknown`, `coupling`) and comparison semantics to DIF as input on its future-work gaps on revocation under partition and cross-organizational policy exchange.
- [ ] Invite the DIF report's editors and contributors to comment on the mapping and on [trustusecases.md](trustusecases.md).
- [ ] Invite the ARIA and ATP groups to self-assess against the seven DIF criteria, so their entries can be read next to the published DIF scorecard.
