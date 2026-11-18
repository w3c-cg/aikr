# Trust in AI (non-agentic)

*Work to be done. Open for contributions from AI KR CG participants. Open for Consultation

*Part of the AI KR CG trust work. Main document: [The Knowledge Representation of the Trust Layer](kroftrust.md). Task force: [Trust KR Task Force](trust-kr-taskforce.md).*

## Purpose

Knowledge representation for trust (KRT) in the AI KR CG covers trust in AI in general: AI systems, machine learning models, large language models and AI agents. Most of the trust folder so far addresses the agentic layer, where agents act for a principal and verify one another's identity and authority at runtime. This file is the place for trust in AI systems that do not act as agents: a model used directly, a classifier inside a product, an LLM answering a person, a system whose outputs people rely on without any delegation of authority.

## Contributions we would like to see

- **Cases.** Documented incidents or worked scenarios in which someone relied on a model, its data, its evaluation results or its outputs, and the basis for that reliance was missing, wrong or impossible to check. Cite the source for each case.
- **Dimensions of trust.** Proposals for what a trust judgement about a non-agentic system rests on, each named, defined in plain language and illustrated with a case.
- **Vocabulary.** Terms with definitions and sources, including terms that mean different things in agentic and non-agentic use.
- **Readings of KRT.** Comments on the [KRT skeleton](https://w3c-cg.github.io/aikr/trust/krt.html) for systems that are not agents: which classes and properties carry over as they are, which need a different reading, and what is missing.
- **Mappings.** Alignment between KRT and existing model documentation and evaluation schemas, model cards among them.
- **Reuse of the trust-layer note.** Views on which sections of [kroftrust.md](kroftrust.md) hold outside the agentic layer. Integrity and availability of artefacts (§3.1), staleness bounds (§3.2), comparison semantics (§4.1), evidence resolution (issue [#10](https://github.com/w3c-cg/aikr/issues/10)), oversight records (PR [#15](https://github.com/w3c-cg/aikr/pull/15)) and key and evidence states (PR [#25](https://github.com/w3c-cg/aikr/pull/25)) are candidates.
- **Related work.** Pointers to groups, standards and published research on trust in models and their outputs, so that this work aligns with them and does not duplicate them.

## Earlier CG work to build on

Listed in the [AIKR CG artefact inventory](https://w3c-cg.github.io/aikr/inventory/): the model of systemic bias (2020), feedback to NIST on explainability principles (2020), the eGovernance guideline for trustworthy AI systems (2020), the W3CAIKRCG model cards on Hugging Face (2024), reliability engineering terms for trustworthy AI (2025), the digital forensics model card specification (2026) and the AI Act high-risk classification glossary (2026).

## How to contribute

- Open an [issue](https://github.com/w3c-cg/aikr/issues) or a pull request against this file in the `trust/` folder.
- Or post to public-aikr@w3.org with `[trust-kr]` in the subject.
- Contributors need their GitHub and W3C accounts linked so the IPR check passes.
- Contributions are acknowledged by name in this file and in the Trust KR task force table.

Anyone who wants to lead this work item is invited to contact the chair to agree its scope.TBC
