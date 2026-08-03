# The Knowledge Representation of the Trust Layer Through the Lens of Digital Identity Chains
TECHNICAL NOTE DRAFT

STATUS:  SEEKING FEEDBACK *Open Consultation 2 Aug 2026  *date of close TBA

*W3C AI Knowledge Representation Community Group*

---

## Executive Summary

Several community and work groups chartered work on agent identity, agent trust establishment, and runtime verification of agent claims. Their scopes overlap. Their vocabularies converge. Their published founding texts diverge on one engineering property that determines whether any of the proposals will hold under production load, and none of them names it.

That property is **resolution dependency**: where an agent's identity document is fetched from at the moment a counterparty needs to verify a claim.

Three arrangements are in play across the current proposals — resolution from a distributed ledger, resolution from a domain the operator controls, and resolution from a registry a third party maintains. Each carries a different answer to who can make an agent disappear, a different latency profile at the ninety-ninth percentile, and a different failure mode under network partition or governance dispute. Charter text as published does not distinguish among them.

Distributed ledger technology sits in three distinct positions across this landscape. One proposal places public-chain receipts directly in scope as audit anchors. Another borrows ledger vocabulary for an append-only record model and disclaims blockchain and consensus mechanisms explicitly. A third carries no chain reference in its own text at all. Separately, an unaffiliated Zurich operator runs a live W3C VC + DID agent trust layer anchored on an Ethereum layer-two network. A reader confined to charter documents would conclude that ledger infrastructure plays a marginal role in agent identity. Deployment evidence says otherwise.

The knowledge-representation problem is: these charters are formal representations of systems that are still evolving, and the representation omits the variable that governs the represented system's behaviour. What gets modelled is the trust relationship. What gets left unmodelled is the substrate the relationship depends on to hold at runtime. Ontologies built on the first without the second will crosswalk cleanly and interoperate poorly.

---

## Part I — Technical Note

**Subject:** Resolution dependency in agent identity — a question to the groups working on the agentic trust layer

**To:** AI Agent Protocol CG · Agent Trust Protocol CG · Agent Declaration and Assurance CG · Agent Identity Registry Protocol CG · Semantic Agent Communication CG · AI Agent Memory Interoperability CG (proposed) · Credentials CG · Decentralized Identifier WG · Verifiable Credentials WG · Federated Identity WG

**From:** W3C AI Knowledge Representation Community Group

---

### 1. Context

Several community groups now hold charters covering agent identity, trust establishment between autonomous agents, and runtime verification of agent claims. Scopes overlap substantially. Only one group in the cluster lists external coordination targets in its founding text.

This note raises a single technical concern that cuts across all of them and invites a short public response from each.

### 2. The concern

Agent trust infrastructure and distributed ledger infrastructure are converging in deployment while remaining separated in charter language.

Ledger anchoring appears in scope for at least one proposed group, framed as public-chain audit receipts supplying verifiability that does not require trusting the operator, with chain selection declared out of scope on grounds of chain agnosticism. A second group disclaims the mechanism expressly: its semantic ledger model is presented as an implementation-independent logical model for ordered, immutable, verifiable records, with the charter stating that no blockchain or consensus mechanism is implied. That same charter maintains an editor role binding conformance and execution-record semantics to DID and VC ecosystems. A third group carries no chain reference at all in its published text, naming only an inspiration source whose work it states does not constrain its deliberations. Meanwhile, and unconnected to any of these groups, a deployed agent trust layer built on the same W3C primitives reports running anchored on an Ethereum layer-two network (Annex A, Annex B).

Reading the charters alone yields no reliable picture of which proposals depend on a chain and which do not.

### 3. Why resolution dependency is the governing variable

Decentralized identifiers are specified as decoupled from centralised registries, identity providers and certificate authorities. That specification describes what a DID is independent **of**. It stays silent on what a DID is dependent **on**. The specification concedes as much in its own terminology, noting that many DID methods, though not all, make use of distributed ledger technology or another form of decentralized network.

Deployment practice has filled the silence. A substantial share of registered DID methods rely on ledger infrastructure to resolve. Every identity check therefore inherits the latency, availability and governance characteristics of whatever network sits beneath the method — properties that appear nowhere in the credential, the presentation, or the charter that specifies either.

Per-session authentication absorbs that inheritance without difficulty. Human login happens once and tolerates a resolution delay measured in seconds. Agent delegation behaves differently. When an agent calls a second agent, which invokes a tool, which reaches a third-party service, credential verification recurs at every hop. Recent work on delegation protocols spanning MCP and A2A identifies ledger-dependent resolution as incompatible with the throughput these call chains demand, an objection that has so far drawn little response from the groups whose designs it touches.

Single-network anchoring compounds the exposure. A deployment paper from outside this cluster concedes the point without hedging: binding a judgement to one ledger inherits that ledger's mortality and politics, since any chain can halt, censor, reorganise or fork. Availability failure and governance capture arrive through the same door.

**Anchoring and resolution are separate dependencies.** A system may resolve identity documents by one path while anchoring proof records, revocations or specification artifacts by another, and the two carry different timescales and different failure modes. Annex A sets out a live case where the anchoring layer finalises on a multi-day challenge window while verification requires an answer in single-digit milliseconds. A representation that collapses the two into a single notion of substrate will misdescribe both.

### 4. The knowledge-representation dimension

Each charter in this cluster functions as a formal representation of a system that has yet to be built. Representations of this kind are judged on what they commit their implementers to. Where a charter names identity, delegation, capability description and conformance, it commits to modelling those. Where it leaves resolution dependency unstated, implementers are free to choose substrates with incompatible operational characteristics while remaining conformant to the same document.

Two consequences follow for anyone building crosswalks across these groups. First, term-level alignment will succeed while behavioural alignment fails: `agent identity` maps cleanly from one vocabulary to another and tells a reader nothing about whether verification completes in four milliseconds or four hundred. Second, security properties described in charter prose are unwarranted until the substrate is pinned, because the assurance a credential offers is bounded by the availability of the thing that resolves it.

A knowledge representation adequate to this layer therefore needs resolution dependency and anchoring dependency as distinct modelled properties, each carrying its own availability, latency and governance attributes, rather than a single undifferentiated notion of where trust data lives.

An ontology of the agentic trust layer that omits resolution dependency describes a trust relationship without describing the conditions under which the relationship holds.

### 5. The ask

Each group is invited to state, briefly and publicly:

1. **Resolution path.** What resolution path does your proposal assume, and is that assumption recorded anywhere normative?
2. **Anchoring path.** Where a proposal anchors records, revocations or specification artifacts, is that substrate the same one identity documents resolve from, and if not, what is it?
3. **Latency budget.** What verification latency budget does your design target for agent-to-agent delegation, and has it been measured under realistic call-chain depth?
4. **Degradation.** What happens to identity verification when the resolution layer is unavailable, partitioned, or subject to governance dispute?
5. **Ledger justification.** Where a chain is involved, which properties does it supply that a domain-hosted or registry-hosted identity document cannot, and who controls transaction ordering on that chain?
6. **Coordination.** Which other groups in the distribution list above have you coordinated with, and on what deliverable?

Responses will be collated and circulated back to all groups on the list. Replies to the AIKR CG list, or to your own list with a cross-post.

---

## Annex A — Note on Base L2

Base is an Ethereum layer-two network built by Coinbase on Optimism's OP Stack, live on mainnet since August 2023. It is an optimistic rollup: transactions execute off Ethereum, compressed batch data is posted back to mainnet, and each batch is treated as valid unless challenged within a defined dispute window. Since the Dencun upgrade, batches can be posted as EIP-4844 blobs, which cut costs substantially. Fault proofs went live in 2024, moving the chain to OP Stack stage 1 and enabling exits that do not depend on Coinbase. Settlement finality is inherited from Ethereum.

It appears in this note because it is the anchoring substrate beneath at least one deployed agent trust layer built on W3C primitives (Annex B), which makes its operational properties a live dependency for that deployment rather than a background detail.

Three properties bear on resolution dependency.

**Ordering authority is held by one company.** Base operates its own sequencer, and that sequencer is controlled by Coinbase. The sequencer orders transactions and submits batch data to Ethereum. Coinbase has committed publicly to decentralising it through its participation in the Superchain, the network of OP Stack chains sharing a bridge, a governance framework and a coordinated upgrade path under the Optimism Collective. That commitment remains a roadmap item. The applications and transactions on the chain are decentralised; the ordering layer is not.

For an identity layer this is the load-bearing fact. Settlement security inherited from Ethereum protects against invalid state transitions. It does not address who decides whether a given transaction is included, or when. A party able to delay or omit an anchoring transaction can delay or omit the publication of an identity record, a revocation, or a violation report, and on this chain that party is singular, identifiable, and subject to the jurisdiction of a single regulator.

**Finality latency and verification latency differ by orders of magnitude.** A seven-day challenge window allows anyone to submit a fraud proof against an invalid state transition, after which the state root finalises on Ethereum. Agent-to-agent delegation, by contrast, needs a verification answer inside a single-digit millisecond budget at every hop of a call chain. A design that treats an anchored record as authoritative must therefore be explicit about which of the two timescales a verifier is waiting on, and current charter language provides no vocabulary for stating the difference.

**Chain-level risk is inherited whole.** A rollup can halt, censor, reorganise or fork, and a system anchoring its most consequential signal to one chain inherits each of those possibilities along with the chain's governance politics. This is not a claim about Base specifically; it applies to any single-network anchoring choice, and it is the argument the MolTrust paper itself makes (Annex B).

None of this argues against ledger anchoring. It argues that a specification naming a chain has named a governance dependency, and that the dependency belongs in normative text where implementers and auditors can see it.

---

## Annex B — Note on "Trust Without Trusting" (Kroehl, 2026)

Lars Kersten Kroehl, MolTrust / CryptoKRI GmbH, Zurich. Preprint dated 14 June 2026, arXiv 2605.06738, continuing an earlier deployment paper by the same author. The work is unaffiliated with any W3C community group named in this note; it is cited here because it is the most candid published account of what a deployed agent trust layer built on W3C primitives actually depends on.

**What it argues.** The paper sets verification aside as substantially solved: any party holding an issuer's key checks a signed credential with no central service, and in an open agent world that covers most of what trust requires. Its subject sits one layer above. Boundaries appear only where a closed space draws one, when a marketplace, platform or consortium sets house rules. Whoever draws the boundary acquires authority over it and may exercise that authority opaquely. The question posed is how a party who distrusts a boundary owner checks that the owner applied its own published admission rules, without handing the check to a new trusted party.

**The mechanism.** The Combined Evidence Protocol combines five conditions about the relying-party population — an elapsed timelock with public veto window, a minimum count of Sybil-qualified parties, distribution across a minimum number of independent clusters, a per-actor voting-weight cap and a per-cluster cap — into a single predicate holding only when all five hold at once. Condition data is published to permanent decentralised storage and anchored as a merkle-root and data-URI pair, so the evidence becomes a deterministic function any party recomputes. The move is borrowed from optimistic rollups, where correctness rests on any verifier's ability to recompute and challenge a published claim. Cluster independence is derived from the endorsement graph by reciprocal-Jaccard analysis instead of from declared organisational categories, on the reasoning that an adversary controls its own labels for free. Keyed commitments plus cryptographic erasure reconcile permanent anchoring against the right to erasure under GDPR Article 17.

**Why it belongs in this note.** Three points align directly with the concern raised above.

First, it names our variable and treats it as a governance question. Three candidate certifiers of network-wide evidence are rejected in turn: a named person, whose testimony lasts only as long as they do; a single running instance, which recreates the single point of failure decentralized identity was meant to remove; and a single chain, because anchoring a judgement to one ledger inherits that ledger's mortality and politics, since it can halt, censor, reorganise or fork.

Second, its remedy is a resolution-path decision stated in normative terms. Multi-chain anchoring of the commitment tuple exists precisely so a determination survives the failure or censorship of any one network. That is the disclosure this note asks the chartered and incubating groups to make, offered voluntarily by an operator with a commercial incentive to stay quiet about it.

Third, it separates layers the charters conflate, distinguishing a verifier-independent evidence layer from a reference registry run by a single organisation, and says so under its own subheading.

**The tension, which sharpens rather than weakens the argument.** The paper documents an exposure its own deployment currently carries. Multi-chain anchoring is listed as an open Gate-2 prerequisite alongside a DID-bound relying-party registry with cluster attribution. Everything live — agent registrations, credential issuances, confirmed violations, and the technical specification itself at a named Base block — sits on one chain, whose sequencer is operated by one company (Annex A). An author who understands the exposure precisely, writes it down, and ships single-chain anyway because the alternative is unbuilt is the strongest available evidence for this note's central claim. Charters that never name the variable will produce implementers who never register that a choice was made.

**One further precision.** Base is the anchoring layer for proof records and audit artifacts. The paper names `did:moltrust` as its reference identifier method and treats any Ed25519 or secp256k1 capable method as conformant, but does not state how `did:moltrust` resolves. The most candid document in this literature therefore still leaves resolution dependency unspecified for its own DID method — which is the gap this note asks each group to close.

**Stated limits.** The registry operates at bootstrap scale, on the order of dozens of agents and endorsements, against an external benchmark of 69,000 bots on a single marketplace; adversarial-scale validation is marked pending. Sybil thresholds are described as operational heuristics rather than formally optimal. The zero-knowledge verification phase is designed and unbuilt, with the demonstrable mechanism running under permissioned data-processing agreements. Treasury governance and weak subjectivity for late joiners are listed as open problems. The paper states each of these itself.

---

## Part II — Source Pool

### Primary standards texts

| # | Resource | One-line description | URL |
| --- | --- | --- | --- |
| 1 | Decentralized Identifiers (DIDs) v1.1 | Candidate Recommendation Snapshot dated 5 March 2026; the normative source for the decoupling language this note turns on, and for the "many, but not all" DLT hedge. | <https://www.w3.org/TR/did-1.1/> |
| 2 | Verifiable Credentials WG charter (2026) | Rechartering that adds Confidence Method and the VC HTTP API, both bearing directly on runtime agent verification. | <https://w3c.github.io/vc-charter-2026/> |
| 3 | Federated Identity WG charter | Defines the browser-mediated Digital Credentials API, the one place in this landscape where presentation is deliberately format- and protocol-agnostic. | <https://www.w3.org/2025/02/wg-fedid.html> |
| 4 | Decentralized Identifier WG charter (draft) | Covers DID maintenance plus consensus-building on resolution and DID URL dereferencing, where the resolution question formally lives. | <https://w3c.github.io/did-wg-charter/> |

### Community group charters (fragmentation evidence)

| # | Resource | One-line description | URL |
| --- | --- | --- | --- |
| 5 | Agent Identity Registry Protocol CG | Verifiable credentials binding agents to controlling organisations for cross-organisational trust negotiation; the only group in the cluster listing external coordination targets. Names TrustLayer Foundation A.C. as an inspiration source, unconnected to item 10. | <https://www.w3.org/community/agent-identity/> |
| 6 | Agent Trust Protocol CG | Formed at the invitation of the AI Agent Protocol CG chairs, covering identity proof, trust establishment and privacy of the humans agents represent. | <https://www.w3.org/community/atp/> |
| 7 | Semantic Agent Communication CG charter | Contains the explicit blockchain disclaimer alongside a Conformance and Semantic Ledger Editor role bound to DID/VC ecosystems. | <https://w3c-cg.github.io/s-agent-comm/> |
| 8 | AI Agent Memory Interoperability CG proposal | Places public-chain receipts in scope as audit anchors while declaring the protocol chain-agnostic; also crosswalks NIST AI RMF, ISO/IEC 42001 and the EU AI Act. | <https://www.w3.org/community/blog/2026/05/18/proposed-group-ai-agent-memory-interoperability-community-group-community-group/> |
| 9 | Agent Network Protocol white paper | The AI Agent Protocol CG's own document, arguing for self-hosted DID documents on the agent's domain and a federated architecture modelled on email. | <https://w3c-cg.github.io/ai-agent-protocol/> |

### Literature

| # | Resource | One-line description | URL |
| --- | --- | --- | --- |
| 10 | Trust Without Trusting: A Recomputable Trust Protocol for Autonomous Agents | Kroehl / MolTrust (Zurich). Reports a live VC + DID agent layer anchored on Base L2 and states plainly why binding a judgement to one ledger inherits that ledger's mortality and politics. Unaffiliated with any group in this note. See Annex B. | <https://arxiv.org/html/2605.06738> |
| 11 | AIP: Agent Identity Protocol for Verifiable Delegation Across MCP and A2A | Source of the throughput objection, with a gap analysis across eleven categories of prior identity work and measured sub-millisecond local verification. | <https://arxiv.org/pdf/2603.24775> |
| 12 | AI Agents with Decentralized Identifiers and Verifiable Credentials | Prototype multi-agent system using ledger-anchored DIDs, whose evaluation exposes limits when an LLM alone controls the security procedures. | <https://arxiv.org/abs/2511.02841> |
| 13 | Autonomous Agents on Blockchains: Standards, Execution Models, and Trust Boundaries | Scoping survey covering agentic wallets, MPC and threshold signing, and policy-bypass risk in agent-driven transactions. | <https://arxiv.org/pdf/2601.04583> |
| 14 | From Cloud-Native to Trust-Native: A Protocol for Verifiable Multi-Agent Systems | Argues for treating identity, policy and action as one composable architecture, with a critique of post-hoc blockchain auditing of model outputs. | <https://arxiv.org/pdf/2507.22077> |
| 15 | Are We There Yet? A Study of Decentralized Identity Applications | Empirical survey of decentralized identity deployments and the interoperability shortfall between DID method implementations. | <https://arxiv.org/pdf/2503.15964> |
| 16 | AESP: A Human-Sovereign Economic Protocol for AI Agents with Privacy-Preserving Settlement | Useful chiefly for its bibliography, which maps the autonomous-economic-agent literature back to 2020. | <https://arxiv.org/pdf/2603.00318> |

### Substrate references (Annex A)

| # | Resource | One-line description | URL |
| --- | --- | --- | --- |
| 17 | Decentralizing Base with the OP Stack and Optimism | Coinbase's own statement of the Superchain sequencing roadmap and the stated intent to progress toward higher decentralisation. | <https://blog.base.org/decentralizing-base-with-the-op-stack-and-optimism> |
| 18 | Introducing Base: Coinbase's L2 Network | Coinbase support documentation confirming the chain is incubated inside Coinbase with progressive decentralisation planned over time. | <https://help.coinbase.com/en/coinbase/other-topics/other/base> |
| 19 | Base explainer (optimistic rollup mechanics, sequencer control, challenge window) | Third-party technical summary covering batch posting to Ethereum L1, the seven-day fraud-proof window, stage 1 status, and Coinbase control of the sequencer. | <https://eco.com/support/en/articles/10370738-what-is-base-coinbase-s-ethereum-l2-explained> |
