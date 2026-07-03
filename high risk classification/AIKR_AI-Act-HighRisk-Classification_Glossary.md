# AI Act High-Risk Classification Guidelines — Glossary & Resource Notes  v 1   July 1 2026

*W3C AIKR CG  Consultation  Opens 1 July 2026:  Based on source: D[raft Commission guidelines on the classification of high-risk AI systems under Article 6 AI Act (2026),](https://digital-strategy.ec.europa.eu/en/consultations/targeted-consultation-draft-guidelines-classification-high-risk-artificial-intelligence-systems)  

THE CG is going to submit comments and recommendations to the Target Consultation open until 23 July*  
*AND*  
*Compile a public vocabulary*

*AI KR CG Participants please send comments on the Glossary Terms \*such as modification of definitions, corrections, alternatives to the public mailing list, or privately to the Chair, or request edit permission so that they may be collated and included on behalf of participants. The final draft will be circulated to the mailing list for approval*   

	*REQUEST EDIT ACCESS TO:*

1.  *ENTER COMMENTS THAT YOU WOULD LIKE SUBMITTED TO THE CONSULTATION  (say, before 20th July)*

2. *ANNOTATE HERE OR DISSCUSS ON THE LIST THE TERMS AND DEFINITIONS THAT WILL CONSTITUTE THE PROPOSED COMMUNITY STANDARD TO BE INCLUDED IN THE NEXT CG REPORT*  
3. 

---

## 0\. A note on the source set

The Target Consultation is open Until 23 July

The Annexes  on the web page download as the same file, which is a DRAFT with several empty slots. Have informed the Commission

---

## 1\. Summary of the Guidelines (created by AI KR CG )

**Resource A — General Principles for Classification of High-Risk AI Systems.** This document is the umbrella chapter of the guidelines. It establishes that Article 6 AI Act creates two independent routes to high-risk status — the product-safety route (Article 6(1)/Annex I) and the use-case route (Article 6(2)/Annex III) — and then lays down principles common to both: a system must first meet the Article 3(1) definition of "AI system" before classification questions arise; and the "intended purpose" declared by the provider (in instructions for use, technical documentation, and promotional material) is the primary anchor for classification, with vague or inconsistent use-limitation language treated as ineffective. It also fixes the compliance timeline (Article 6(2) obligations from 2 December 2027, Article 6(1) obligations from 2 August 2028, under the AI Omnibus postponement) and describes the review mechanism (annual monitoring of Annex III, delegated-act powers to amend Annex III or Article 6(3)). This is the constitutional/definitional layer beneath the other resource.

**Resource B — Article 6(1) and Annex I: Product-Safety Route to High-Risk Classification.** This document operationalises the first of the two routes described in Resource A. It explains that Annex I lists *Union harmonisation legislation* (not products directly), and that an AI system is high-risk under this route only if it satisfies two cumulative conditions: (i) it is itself a regulated product, or a "safety component" of one, within the meaning of the AI Act's autonomous Article 3(14) definition (assessed either by whether the system has an intended *safety function*, or by whether its *failure or malfunctioning* would endanger health, safety, or property), and (ii) the product is required to undergo *third-party conformity assessment* under that sectoral legislation. It works through worked examples (lifts, machinery, toys, vehicles, gas appliances, agriculture) and the Decision 768/2008/EC conformity-assessment module structure (A–H) to show how the two conditions interact, and closes with the AI Act's compliance-burden-reduction mechanisms (integrating AI risk assessment into existing sectoral quality-management systems).

**How the two align.** Resource A is the general/definitional layer; Resource B is a specific application of one of the two classification routes it sets up. Read together they form a single decision tree: "Is it an AI system?" → "What is its intended purpose?" → "Route 1 (Annex I product safety) or Route 2 (Annex III use case)?" → for Route 1, "safety component \+ third-party conformity assessment?" Resource B presupposes and cross-references Resource A's definitions (AI system, intended purpose) rather than restating them.

ANNEX III Downloads  same as ANNEX II as of 1 July 2026

---

## 2\. Alignment with the wider AI governance ecosystem

These guidelines sit at the intersection of two regulatory traditions that the AI Act deliberately does not merge:

- **Product-safety law (New Legislative Framework).** Article 6(1)/Annex I does not create new risk categories; it *inherits* the risk classification already made by sectoral product legislation (Machinery Regulation, Toys Safety Regulation, Medical Devices Regulation, etc.) and the Blue Guide's conformity-assessment-module logic (Decision 768/2008/EC). This is a **subsidiarity/non-duplication design choice**: rather than building a parallel AI risk taxonomy for regulated products, the AI Act attaches itself to conformity-assessment stringency as a proxy for risk. For AIKR CG's interoperability work, this is a good illustration of a *risk classification system that is itself a function of another external standard*, which has implications for how "high-risk" is modelled as a class in agentic-AI ontologies — it is not a first-order property of the AI system but a derived property conditioned on sectoral law.  
- **Fundamental-rights/use-case law (Article 6(2)/Annex III, not in the uploaded text).** The parallel route classifies by *domain of use* (biometrics, employment, education, law enforcement, etc.) rather than by product-safety status, and follows a different timeline and (per Article 6(3)) allows provider self-exemption in narrower circumstances. The general-principles document explicitly separates these two logics while unifying them under shared upstream tests (AI-system definition, intended purpose).  
- **Relation to standards infrastructure.** Article 40 AI Act (referenced in Resource B, para 61\) requires consistency between AI Act harmonised standards and existing sectoral harmonised standards — directly relevant to AIKR CG's SDO landscape mapping, since it means CEN-CENELEC JTC 21 AI Act standards must interoperate with sector-specific standards bodies rather than superseding them.  
- **Soft-law status.** Both documents are explicitly non-binding stakeholder-consultation drafts (Recital-style disclaimers, "final interpretation rests with the CJEU"). For a knowledge-representation vocabulary, this means any class built from these documents should carry a provenance/status annotation (`draft guideline`, not `binding norm`) distinguishing it from the Regulation text itself.

---

## 3\. Glossary

Format: **Term** — *novel synthesised definition* (source) — SKOS-style relations.

Definitions below are original paraphrases for glossary use, not verbatim extracts from the guidelines.

### 3.1 Foundational / cross-cutting concepts

**AI system** — A machine-based system, operating with some degree of autonomy and capable of adapting after deployment, that infers from input how to produce outputs (predictions, content, recommendations, decisions) capable of influencing a physical or virtual environment. (Resource A, restating Art. 3(1) AI Act) — *broader:* machine-based system; *narrower:* general-purpose AI system, safety-component AI system; *related:* intended purpose, autonomy, adaptiveness.

**Intended purpose** — The scope of use for an AI system as fixed by its provider through instructions for use, technical documentation, and promotional/sales materials; the reference point against which classification and downstream obligations are assessed, and against which "reasonably foreseeable misuse" is defined by exclusion. (Resource A) — *related:* reasonably foreseeable misuse, provider, high-risk classification; *narrower:* declared safety function.

**Reasonably foreseeable misuse** — Use of an AI system falling outside its declared intended purpose but plausible given the system's functionalities, context, and marketing; conceptually the residual category left once intended purpose is fixed. (Resource A) — *related:* intended purpose; *broader:* misuse.

**High-risk AI system** — An AI system classified as such under Article 6 AI Act via one of two independent, non-overlapping routes: the product-safety route (Art. 6(1)/Annex I) or the use-case route (Art. 6(2)/Annex III). (Resource A) — *narrower:* Annex I high-risk system, Annex III high-risk system; *related:* third-party conformity assessment, safety component.

**Classification route (dual-track model)** — The AI Act's structural device of running two independent tests for high-risk status — one keyed to regulated-product safety law, one keyed to fundamental-rights-sensitive domains of use — rather than a single unified risk test. (Resources A & B, synthesised) — *related:* Article 6(1), Article 6(2).

**Substantial modification** — A change to a high-risk AI system, made after it has been placed on the market or put into service, that is significant enough to trigger provider obligations for the party making the change, without necessarily altering the system's high-risk status. (Resource A) — *related:* provider obligations, Article 25 AI Act.

**Provider-obligation transfer trigger** — The set of three conditions under Article 25(1) AI Act under which a distributor, importer, or deployer becomes legally a "provider": rebranding a high-risk system under its own name, substantially modifying a high-risk system while it remains high-risk, or modifying the purpose of a non-high-risk (including general-purpose) system such that it becomes high-risk. (Resource A) — *related:* substantial modification, provider, deployer, distributor.

### 3.2 Product-safety route (Article 6(1) / Annex I)

**Regulated product** — A product falling within the material scope of one of the pieces of Union harmonisation legislation listed in Annex I AI Act (e.g. machinery, toys, medical devices, radio equipment, lifts, pressure equipment). (Resource B) — *broader:* product under Union harmonisation legislation; *related:* safety component, third-party conformity assessment.

**Safety component (autonomous AI Act definition)** — A component of a product or of an AI system that either fulfils a safety function for that product/system, or whose failure or malfunctioning would endanger the health, safety, or property of persons — defined independently of any "safety component" definition used in sectoral product legislation, so as to apply uniformly across all Annex I sectors. (Resource B, Art. 3(14) AI Act) — *narrower:* safety-function component, failure-risk component; *related:* safety function, failure or malfunctioning, endangerment.

**Safety function** — An intended purpose, fixed by the provider, of preventing or mitigating risk to the health or safety of persons or to property; assessed by intent/documentation rather than by outcome. Distinguished from functions aimed at optimisation, efficiency, comfort, or convenience, which do not qualify however safety-adjacent the product context. (Resource B) — *narrower:* preventive function, mitigation function; *related:* safety component, intended purpose.

**Preventive function** *(sub-type of safety function)* — A safety function oriented to stopping a hazard before it materialises: monitoring/detection of hazardous conditions, detection of maintenance need, prevention of physical harm, or supervision of another safety-performing system. (Resource B) — *broader:* safety function.

**Mitigation function** *(sub-type of safety function)* — A safety function oriented to limiting harm once a hazardous condition exists: controlling or limiting physical harm, triggering a safe-stop or similar consequence-limiting action, or controlling another safety-performing system. (Resource B) — *broader:* safety function.

**Failure or malfunctioning (as classification trigger)** — The second, consequence-based route to "safety component" status: a system qualifies not because it was designed for safety, but because its incorrect outputs, loss of availability, drift, latency errors, or misclassification could — in the specific product context — endanger health, safety, or property, regardless of the provider's declared intended purpose. (Resource B) — *related:* safety component, endangerment; *contrasts with:* safety function (intent-based test).

**Endangerment** — An increase in hazard to the health, safety, or property of persons, as distinct from reputational harm, purely financial loss, minor service degradation, or inconvenience — the qualifying threshold of harm for the failure/malfunctioning test. (Resource B) — *related:* failure or malfunctioning, harm to health, harm to property.

**Harm to health** — Illness, injury, temporary or permanent impairment of a body structure or function, chronic disease, or psychological trauma significantly affecting ordinary task performance — the health-side content of "endangerment." (Resource B) — *broader:* endangerment.

**Third-party conformity assessment** — The procedural requirement, set by the relevant Union harmonisation legislation (not by the AI Act itself), that a product's compliance be verified by an external notified body rather than solely by manufacturer self-declaration; presence of this requirement is the second cumulative condition for Article 6(1) high-risk status. (Resource B) — *related:* conformity assessment module, notified body, regulated product.

**Conformity assessment module (A–H)** — The harmonised structure of compliance-demonstration procedures set by Decision 768/2008/EC and used across NLF legislation, ranging from Module A (manufacturer self-declaration, low complexity/low risk) through modules requiring notified-body involvement in design and/or production phases (B, C, D–H and sub-variants); module complexity is meant to scale with product risk and production complexity. (Resource B) — *narrower:* Module A, Module B, Module C, notified-body-required modules; *related:* third-party conformity assessment, Blue Guide.

**Notified body** — An accredited third-party conformity-assessment body whose involvement (in the design phase, production phase, or both, depending on the module) is required by most conformity-assessment modules other than Module A; its required involvement is the operative signal used by Article 6(1) to identify high-risk products. (Resource B) — *related:* conformity assessment module, third-party conformity assessment.

**Union harmonisation legislation (Annex I)** — The closed, exhaustively-listed set of EU product-safety instruments (Section A: New Legislative Framework acts; Section B: other harmonisation acts) that Annex I AI Act references; the AI Act does not itself expand the material scope of any of these acts. (Resource B) — *related:* New Legislative Framework, Blue Guide, regulated product.

**New Legislative Framework (NLF)** — The EU's general product-safety governance architecture (built on Decision 768/2008/EC and the Blue Guide) that most Annex I Section A instruments follow, providing the shared vocabulary (conformity assessment, notified body, harmonised standard) that Article 6(1) AI Act draws on rather than reinventing. (Resource B) — *related:* Blue Guide, conformity assessment module.

**Blue Guide** — The Commission's non-binding interpretive guide to NLF-based EU product rules, used in Resource B as the interpretive backdrop for conformity-assessment-module selection and the "protection of the public interest" rationale. (Resource B) — *related:* New Legislative Framework, conformity assessment module.

**Harmonised standard (as gatekeeper for self-assessment)** — A standard published in the EU Official Journal whose application is, for certain products (e.g. under the Toys Safety Regulation, Machinery Regulation, Radio Equipment Regulation), a precondition for a manufacturer being allowed to use Module A (internal control) instead of third-party assessment; its role illustrates that "internal control possible" is not the same as "not high-risk" under the AI Act. (Resource B) — *related:* conformity assessment module, third-party conformity assessment.

**Compliance-burden minimisation mechanism** — The set of AI Act provisions (Art. 8(2), 9(10), 17(3), 40\) allowing economic operators to fold AI-specific risk assessment into pre-existing sectoral risk- and quality-management systems rather than running a duplicate AI Act compliance process, and requiring consistency between AI Act harmonised standards and sectoral ones. (Resource B) — *related:* Union harmonisation legislation, harmonised standard.

**Sectoral risk inheritance principle** — The interpretive principle (Recital 51 AI Act) that the AI Act does not itself determine or alter a product's risk profile, but builds on and inherits the risk classification already established by the applicable sectoral product-safety legislation. (Resource B, synthesised) — *related:* regulated product, third-party conformity assessment.

### 3.3 Governance / procedural apparatus

**AI Board** — The European Artificial Intelligence Board, consulted on the guidelines' drafting and involved in the ongoing collection of practical classification use cases. (Resource A) — *related:* AI Office, delegated act.

**AI Office** — The Commission body responsible for providing ongoing support to operators and market surveillance authorities on high-risk classification, and for collecting further practical use cases via the AI Act Service Desk and regulatory sandboxes. (Resource A) — *related:* AI Act Service Desk, regulatory sandbox.

**AI Act Service Desk / Single Information Platform** — The Commission's designated channel for classification questions and for presenting the guidelines and use-case examples to operators in a searchable, area-filterable format. (Resource A) — *related:* AI Office.

**Regulatory sandbox** — A controlled testing environment for AI systems, to be established by Member States by 2 August 2026 under the AI Act, referenced in Resource A as one of the mechanisms feeding the ongoing review of high-risk use cases. (Resource A) — *related:* AI Office, annual monitoring instrument.

**Delegated act (Annex III amendment power)** — The Commission's power under Article 7 AI Act to add, amend, or remove high-risk use cases in Annex III, or to modify the Article 6(3) self-exemption conditions, subject to defined statutory conditions — the AI Act's built-in future-proofing mechanism for the use-case route. (Resource A) — *related:* annual monitoring instrument, Article 6(2).

**Annual monitoring instrument** — The Article 112(1) AI Act mechanism requiring yearly evaluation and review of the Annex III high-risk use-case list to keep it responsive to emerging risks and market developments. (Resource A) — *related:* delegated act, AI Board.

### 3.4 Agentic representation & verification (AIKR CG extensions)

*These terms extend the legal vocabulary above toward agent interoperability. They are CG synthesis grounded in the group's in-flight work and cited literature, not extracts from the guidelines; per §4, each carries `status: draft / CG-extension`.*

**Derived classification** — A risk class that is not an intrinsic, first-order property of an AI system but is *derived* from external law, context, and intended purpose (cf. §2). For agentic systems it must therefore be represented as a resolvable, signed attribute that travels with the agent, rather than a static label asserted in prose. (AIKR CG synthesis, extending §2) — *broader:* high-risk AI system; *related:* intended purpose, sectoral risk inheritance principle, classification persistence.

**Evidentiary record** — A content-addressed, independently-verifiable record of an agent's action — *commitment* (authority relied on), *decision* (authority, context, and evidence evaluated), *receipt* (outcome) — that makes Article 12 (record-keeping) and Article 14 (human oversight) obligations checkable by any party without trusting the operator's logs. Carries a belief-state reference (`belief_state_ref`) binding *what was thought* at the moment of action, on the principle of **admissibility, not truth**. (W3C AI Agent Protocol CG: issues #34/#36, PRs #40/#41) — *broader:* record-keeping obligation; *related:* third-party conformity assessment, classification persistence.

**Classification persistence** — Whether, and how, a derived classification and the obligations it triggers survive the lifecycle events agentic systems routinely undergo — copying, fine-tuning, forking, checkpoint-restore — and which resulting instance carries them. The guidelines treat classification as a one-time determination; agentic deployment makes persistence across these events an open question. (AIKR CG synthesis; cf. Parfitian fission) — *related:* substantial modification, provider-obligation transfer trigger, speaks-for authority.

**Speaks-for authority** — The delegation relation (after Abadi–Lampson, 1993) deciding which instance may act *as* a classified system after a fork or restore — distinct from, and not reducible to, the metaphysical question of which instance *is* the original (an empty question for copyable agents). It separates "who is accountable / holds the credential" from "which is the real one." (AIKR CG synthesis; Abadi, Burrows, Lampson, Plotkin, *A Calculus for Access Control in Distributed Systems*, ACM TOPLAS 1993) — *related:* classification persistence, provider, deployer.

---

## 4\. Suggested SKOS integration notes for AIKR CG

- These terms map naturally onto a **"regulatory classification" facet** distinct from  existing agent-interoperability categories — worth checking whether the locked 8-category taxonomy has (or needs) a governance/compliance category, or whether these should be cross-referenced as `related` terms into existing categories (e.g. *safety component* → agent capability/function category; *third-party conformity assessment* → trust/verification category).  
- **`skos:broader`/`skos:narrower`** pairs above are drafted at one level of depth only; deeper nesting (e.g. Module A/B/C as narrower than *conformity assessment module*) can be expanded if the vocabulary needs module-level granularity.  
- Recommend a `provenance` or `status` annotation property (e.g. `aikr:sourceStatus = "draft/non-binding"`) on any concept sourced from this document set, since both resources are explicitly stakeholder-consultation drafts, not adopted Commission guidelines.  
- Terms specific to the Annex III/Article 6(2) use-case route are **not yet covered** — flagging as a gap if/when the corresponding chapter is obtained, since Resource A only references it structurally.

