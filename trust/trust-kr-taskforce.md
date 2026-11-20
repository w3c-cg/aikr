# Trust KR Task Force

*Draft mission statement, proposed to the W3C AI Knowledge Representation Community Group in November 2026. Proposed start date effective asap.
To be discussed and agreed by CG participants on public-aikr.*

*Part of the AI KR CG trust work. Main document: [The Knowledge Representation of the Trust Layer](kroftrust.md). Trust record visualiser: [AI Agent Trust Record](https://w3c-cg.github.io/aikr/trust/AI_Agent_Trust_Record.html).*

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
| Nicola Gallo | Authority continuity: formal model and proposed cases (PR #22) |
| Evgenii Arsentev | Pointer to the Agent Conformance reporting format (PR #13) |
| Andreas Ehstand | Oversight records in KRT (PR #15, open) |
| Sean (LexLint) | Corrections to KRT (issue #19) and review of the oversight records |
| Lars Kroehl | Correction to Annex B on did:moltrust resolution (issue #9) |
| Yanfeng Liu | Answers to the six questions of the note (issue #5), review of the trust record for audit and accountability |
| Larry Lewis | Review of the trust record model |
| Francesco Marinoni Moretto | Commerce identity rows and the Key publisher field of the trust record (issue #28) |
| bigblackcoder (GitHub) | Review of the DNS and DID note (issue #27) and the ATP demonstration package (issue #29) |
| Prasanna Bableshwar | Hiring use case (UC-09) in `trustusecases.md`, from the ARIA CG hiring thread and the v0.2 Registry Write-up |

## Handover notes

Open items passed to the task force when it starts work.

- **ATP demonstration package ([issue #29](https://github.com/w3c-cg/aikr/issues/29)).** A 22-scenario assessment harness for the trust record, published for independent rerun. All 22 scenarios passed when run by the contributor. List it in the Implementation reports table of the [visualiser specification](https://w3c-cg.github.io/aikr/trust/trustvisualiser.html), with status "Run by the contributor", and change the status to "Independently rerun" once someone else reruns it.
- **Key and evidence states ([PR #25](https://github.com/w3c-cg/aikr/pull/25)).** The contributor reports that all eleven cases and eleven mutation controls match `expected.json`. Consider citing the result in the report and inviting runs in other languages.
- **Contributor names.** Confirm whether the GitHub account bigblackcoder (issues #27 and #29) belongs to Larry Lewis, and if so merge the two entries in the co-lead table and in the report.
- **Corrections to the technical note.** Annex B on did:moltrust resolution ([issue #9](https://github.com/w3c-cg/aikr/issues/9)); source pool numbers 17 to 19 used twice.
- **Pending contributions.** English summary of the Agent Community answers ([issue #5](https://github.com/w3c-cg/aikr/issues/5)); oversight records in KRT ([PR #15](https://github.com/w3c-cg/aikr/pull/15)); comments on KRT ([#19](https://github.com/w3c-cg/aikr/issues/19)), the DNS and DID note ([#26](https://github.com/w3c-cg/aikr/issues/26), [#27](https://github.com/w3c-cg/aikr/issues/27)) and the trust record ([#28](https://github.com/w3c-cg/aikr/issues/28)).
- **Housekeeping.** `aria2.html` duplicates `aria.html`; the visualiser page has no link back to the technical note.
