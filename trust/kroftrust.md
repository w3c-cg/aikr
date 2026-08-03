# The Knowledge Representation of the Trust Layer Through the Lens of Digital Identity Chains
DRAFT TECHNICAL NOTE

OPEN CONSULTATION STARTS 2 AUGUST 26

CONSULTATION TO CLOSE:  TBA

FEEDBACK BY OPENING AN ISSUE HERE AND PINGING THE AI KR CG Mailing list 

*W3C AI Knowledge Representation Community Group*

---

## Executive Summary

The Trust Layer rests on explicit representation at a critical junction where it intersects with DID and the blockchain.

Several community and work groups chartered work on agent identity, agent trust establishment, and runtime verification of agent claims. Their scopes overlap. Their vocabularies converge, and published founding texts diverge on one engineering property that determines whether any of the proposals will hold under production load, and none of them names it: resolution dependency: where an agent's identity document is fetched from at the moment a counterparty needs to verify a claim.

Three arrangements are in play across the current proposals — resolution from a distributed ledger, resolution from a domain the operator controls, and resolution from a registry a third party maintains. Each carries a different answer to who can make an agent disappear, a different latency profile at the ninety-ninth percentile, and a different failure mode under network partition or governance dispute. Charter text as published does not distinguish among them.

Distributed ledger technology sits in three distinct positions across this landscape. One proposal places public-chain receipts directly in scope as audit anchors. Another borrows ledger vocabulary for an append-only record model and disclaims blockchain and consensus mechanisms explicitly. A third carries no chain reference in its own text at all. Separately, an unaffiliated Zurich operator runs a live W3C VC + DID agent trust layer anchored on an Ethereum layer-two network. A reader confined to charter documents would conclude that ledger infrastructure plays a marginal role in agent identity. Deployment evidence says otherwise.

The concern is not confined to one consortium. Work on agent identity and agent trust is under way at the IETF, the FIDO Alliance, the OpenID Foundation, the Decentralized Identity Foundation, the Linux Foundation, the Ethereum improvement process, NIST, and several security consortia, and the same variable goes unstated across most of them. Part II surveys that landscape. One effort, Ethereum's ERC-8004, answers the question explicitly and answers it as a hybrid, which establishes that the disclosure asked for here is achievable and already shipped.

The knowledge-representation problem is: these charters are formal representations of systems that are still evolving, and the representation omits the variable that governs the represented system's behaviour. What gets modelled is the trust relationship. What gets left unmodelled is the substrate the relationship depends on to hold at runtime. Ontologies built on the first without the second will crosswalk cleanly and interoperate poorly.

---

## Part I — Technical Note

**Subject:** Resolution dependency in agent identity — a question to the groups working on the agentic trust layer

**To (W3C):** AI Agent Protocol CG · Agent Trust Protocol CG · Agent Declaration and Assurance CG · Agent Identity Registry Protocol CG · Semantic Agent Communication CG · AI Agent Memory Interoperability CG (proposed) · Autonomous Agents on the Web CG · Ontology for Agents, Systems and Integration of Services CG · Credentials CG · Decentralized Identifier WG · Verifiable Credentials WG · Federated Identity WG

**Cc (external, for information):** IETF WIMSE WG · FIDO Alliance Agentic Authentication TWG · OpenID Foundation AIIM CG · Decentralized Identity Foundation Trusted AI Agents WG and Identifiers & Discovery WG · Linux Foundation A2A · ERC-8004 maintainers

**From:** W3C AI Knowledge Representation Community Group

---

### 1. Context

Several community groups now hold charters covering agent identity, trust establishment between autonomous agents, and runtime verification of agent claims. Scopes overlap substantially. Only one group in the cluster lists external coordination targets in its founding text.

This note raises a single technical concern that cuts across all of them and invites a short public response from each.

### 2. The concern

Agent trust infrastructure and distributed ledger infrastructure are converging in deployment while remaining separated in charter language.

Ledger anchoring appears in scope for at least one proposed group, framed as public-chain audit receipts supplying verifiability that does not require trusting the operator, with chain selection declared out of scope on grounds of chain agnosticism. A second group disclaims the mechanism expressly: its semantic ledger model is presented as an implementation-independent logical model for ordered, immutable, verifiable records, with the charter stating that no blockchain or consensus mechanism is implied. That same charter maintains an editor role binding conformance and execution-record semantics to DID and VC ecosystems. A third group carries no chain reference at all in its published text, naming only an inspiration source whose work it states does not constrain its deliberations. Meanwhile, and unconnected to any of these groups, a deployed agent trust layer built on the same W3C primitives reports running anchored on an Ethereum layer-two network (Annex A, Annex B).

Method proliferation compounds the problem. Within this cluster alone, the Agent Trust Protocol CG intends to specify did:atp, a quantum-safe method using hybrid Ed25519 and ML-DSA-65 post-quantum signatures; the deployment surveyed in Annex B operates did:moltrust; and the AIP protocol described in Annex C defines two further identifier schemes of its own. New methods are being minted faster than anyone is specifying how they resolve.

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

## Part II — The Landscape Beyond W3C

Agent trust work is distributed across at least a dozen venues, and the consortium's community groups are not the largest of them. This part surveys the external efforts, notes what each says about resolution dependency, and identifies where coordination would repay effort.

### 2.1 IETF

**WIMSE — Workload Identity in Multi System Environments** is the most concrete effort in the adjacent space. Chartered to evolve SPIFFE concepts into standards-track documents covering workload identity across cloud, multi-tenant and cross-trust-domain deployments, its active drafts as of early 2026 include an architecture document, a workload credentials specification, a workload identifier format, a mutual TLS profile and a practices document. The architecture draft names AI agents as a use case, which places agent identity formally within the working group's scope.

WIMSE also marks the boundary of its own claim clearly. It establishes that a given credential belongs to a given workload. It does not express what authority that workload holds, how the authority derived from a human originator, or whether onward delegation is permitted. Identity and authority are treated as separate questions, and WIMSE addresses the first.

An open design question runs alongside: WIMSE primitives were built for static, long-running workloads, while an agent session may be short-lived, context-dependent and capable of spawning sub-agents dynamically. Any mapping from agent identity onto workload identity has to answer that mismatch.

Individual submissions circulating around the group include AIMS (`draft-klrc-aiagent-auth`), which composes WIMSE, SPIFFE and OAuth into a conceptual model; WIMSE applicability for AI agents (`draft-ni-wimse-ai-agent-identity-02`, Huawei, February 2026), which introduces an owner able to bind agent identity to a principal by cryptographic signature; an agentic JWT extension; and a SCIM profile covering provisioning lifecycle. Adjacent IETF groups named in the WIMSE charter include OAuth, SCIM, SCITT and RATS, with liaison to CNCF over SPIFFE/SPIRE and to the OpenID Foundation.

Resolution dependency in this family runs through attestation infrastructure. A SPIFFE verifiable identity document is issued by a registration and attestation service the operator deploys, so the question becomes who runs SPIRE and what happens when it is unreachable. Certificate issuance latency has already been identified as incompatible with ephemeral agent creation.

### 2.2 FIDO Alliance

In April 2026 the FIDO Alliance announced an Agentic Authentication Technical Working Group together with specification work for agent-initiated commerce, drawing on initial contributions of Google's Agent Payments Protocol and Mastercard's Verifiable Intent. The Alliance states it is liaising with other bodies to keep agentic commerce initiatives harmonised.

Two proposals that were previously vendor property now sit with a neutral standards organisation. For a consortium group planning to publish in this space, FIDO has become the venue where the commerce half of the problem will be settled.

### 2.3 Linux Foundation

A2A passed 150 supporting organisations in its first year, including AWS, Cisco, Google, IBM, Microsoft, Salesforce, SAP and ServiceNow. The Agent Payments Protocol carries more than 60 backers across payments and financial services, and the Unified Commerce Protocol interoperates with it through an AP2 mandates extension capturing cryptographic evidence of user consent to purchase.

A2A agent cards carry self-declared identities with no attestation binding, which is the gap the identity efforts elsewhere are attempting to close.

### 2.4 OpenID Foundation

The Artificial Intelligence Identity Management Community Group runs biweekly subgroup meetings and published a whitepaper in October 2025 identifying agent security gaps, which drew substantial trade coverage. AIIM is one of the four coordination targets named by the Agent Identity Registry Protocol CG.

### 2.5 Decentralized Identity Foundation

DIF launched a Trusted AI Agents Working Group in 2025, with Agentic Authority Use Cases as its first work item. Its longer-standing Identifiers and Discovery Working Group maintains the universal resolver and universal registrar driver frameworks, a specification for discovering DIDs from well-known HTTP endpoints, a method with no blockchain dependencies whose verifiable data registry is a peer synchronisation protocol, and a specification for representing DID method traits in machine-readable form.

That last item deserves attention from anyone working on this note's question. A machine-readable trait vocabulary for DID methods is the closest existing artifact to the disclosure being requested, and extending it to cover resolution latency, availability and withdrawal authority would be a smaller undertaking than starting a new vocabulary.

### 2.6 Ethereum — ERC-8004

ERC-8004 gives autonomous agents verifiable identity, portable reputation and independent validation through three on-chain registries, with mainnet launch in January 2026 and reference deployments on Ethereum Sepolia, Base Sepolia, Linea Sepolia and Hedera Testnet.

Its identity design answers this note's question directly, and answers it as a hybrid. The Identity Registry is an ERC-721 contract; each agent mints a token whose URI points to an offchain registration file conventionally hosted at `/.well-known/agent-card.json`, and the token identifier resolves to a CAIP-10 chain-agnostic address plus a domain string, so the same agent can be referenced across chains.

Both resolution paths operate at once, with different withdrawal powers at each layer. A chain governs the registry entry; a domain operator governs the document the entry points to. Losing either breaks verification, and the two fail independently. Whatever one concludes about the merits, the arrangement is stated plainly enough that an implementer can reason about it — which is what the charters surveyed in Part I do not yet permit.

### 2.7 Government and regulators

NIST's Center for AI Standards and Innovation announced its AI Agent Standards Initiative on 17 February 2026, organised around three pillars: industry-led standards development with United States leadership in international bodies including ISO/IEC JTC 1; community-led open-source protocol development co-invested with the National Science Foundation; and fundamental research covering agent security, identity infrastructure and interoperability evaluation methodology. The companion NCCoE concept paper frames the operational deficiency directly, observing that agents are commonly treated as generic service accounts without dedicated identity, authorization or accountability controls.

Singapore's Infocomm Media Development Authority published its Model AI Governance Framework for Agentic AI in January 2026, requiring each agent to carry a verifiable digital identity together with an audit trail recording which agent acted under whose authorisation.

Regulation (EU) 2024/1689 applies Article 14 on human oversight and Article 15 on accuracy, robustness and cybersecurity to autonomous agents in high-risk domains. Following adoption of the Digital Omnibus on AI — endorsed by Parliament on 16 June 2026 and approved by the Council on 29 June 2026 — those Chapter III obligations now apply from 2 December 2027 for standalone Annex III systems and from 2 August 2028 for AI embedded in Annex I regulated products. Article 50 transparency duties were carved out of the deferral and apply from 2 August 2026, with the machine-readable marking requirement under Article 50(2) binding legacy systems from 2 December 2026. The deferral moves European high-risk enforcement behind the Singapore framework and the NIST initiative rather than ahead of them, and it brings the Verifiable Credentials deliverable schedule, which runs to April 2028, into rough alignment with the obligations it would support.

ISO/IEC JTC 1 appears in the NIST pillars as a target venue rather than an active one, which means part of this work is a standards-diplomacy contest as well as a technical one.

### 2.8 Security consortia

The Cloud Security Alliance published an Agentic Trust Framework on 2 February 2026, a zero-trust governance model for autonomous agent deployments that operationalises OWASP Agentic Top 10 mitigations and aligns with CoSAI and the emerging NIST agent identity requirements.

The OWASP Agentic Top 10 for 2026 covers Agent Goal Hijack, Tool Misuse, Identity and Privilege Abuse, Supply Chain Vulnerabilities and Insecure Inter-Agent Communication, with Least Agency as its foundational principle. CoSAI's founding members include Anthropic, Cisco, Google, IBM, Intel, Nvidia and PayPal.

### 2.9 Existing academic taxonomy

Hu (Oxford) and Rong (NYU Shanghai) compare A2A, AP2 and ERC-8004 across six inter-agent trust models — Brief, Claim, Proof, Stake, Reputation and Constraint — evaluated against security, privacy, latency and cost, and Sybil, collusion and whitewashing resistance.

That is the nearest published equivalent to a crosswalk, and it covers protocols the consortium groups do not. Adding resolution dependency as a further dimension would position this contribution as an extension of existing work rather than as a competing vocabulary.

### 2.10 What follows for coordination

Three observations bear on how this note should be received.

The consortium cluster is peripheral by membership. A2A alone counts over 150 supporting organisations. The community groups surveyed in Part I count participants in single and double digits. Any recommendation that depends on the consortium acting alone will underreach.

The same variable is unstated almost everywhere. WIMSE defers authority questions; A2A agent cards carry unattested self-declarations; the OpenID and DIF efforts are at use-case stage. ERC-8004 is the exception that proves the disclosure is possible.

The artifact that would carry the disclosure may already exist. DIF's machine-readable DID method traits specification is the obvious host for resolution-path, latency and withdrawal-authority attributes, and extending it would reach every method in the ecosystem rather than one group's vocabulary.

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

## Annex C — Note on the Agent Identity Protocol (Prakash, 2026)

Sunil Prakash, Indian School of Business. arXiv 2603.24775, 25 March 2026. Cited here because it supplies the measured evidence behind the latency argument in Part I §3 and because its identifier design is one of the few that states a resolution path normatively.

**The measurement.** Compact token verification averages 0.049 ms in Rust and 0.189 ms in Python at a fixed 356 bytes. Chained tokens grow at 340 to 380 bytes per delegation block and verify in 0.745 ms at depth five. Over real HTTP against an MCP server, compact mode adds 0.222 ms to a 0.301 ms unauthenticated baseline. Against live Gemini 2.5 Flash inference in a multi-agent delegation, protocol overhead totals 2.351 ms against 2,749 ms end to end, or 0.086 per cent, rising to 0.127 per cent at the ninety-ninth percentile.

The author attributes the result to verification being purely local, requiring no authorization server round trip, so overhead scales with cryptographic operations instead of network latency. That single sentence locates the cost. Signature arithmetic is nearly free; fetching the document holding the signing key is where the time goes. It is the empirical basis for treating resolution rather than verification as the governing variable.

**The identifier design.** Two schemes and no others. Domain identifiers use `aip:web:<domain>/<path>` and resolve over HTTPS to a well-known endpoint, intended for long-lived agents whose operators hold a domain name. Self-certifying identifiers use `aip:key:ed25519:<multibase>`, encoding the public key so that no resolution step occurs, intended for ephemeral sub-agents spawned for a single task. Identity documents must carry a self-signature over the RFC 8785 canonical form, which detects tampering even where the hosting domain is compromised.

**The comparison.** A seven-property gap analysis across eleven prior approaches scores W3C decentralized identifiers as failing the criterion the author labels absence of blockchain or heavy infrastructure dependency, alongside SPIFFE and UCAN, the latter inheriting the dependency through its identity layer. No surveyed approach satisfies more than four of the seven properties.

**Context worth carrying.** The paper reports a Knostic security scan of approximately 2,000 Model Context Protocol servers in which every one lacked authentication. Whatever the standards bodies settle on will be adopted into a deployed base that currently has none.

**Stated limits.** Benchmarks ran on a single machine over localhost, capturing cryptographic and protocol cost without cross-datacentre networking or sustained load. Completion blocks are self-reported by the executing agent by default. Version one prefers short-lived tokens under an hour to revocation infrastructure. Ed25519 is the only signature algorithm, with no post-quantum path.

---

## Part III — Source Pool

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

### External initiatives (Part II)

| # | Organisation / effort | One-line description | URL |
| --- | --- | --- | --- |
| 17 | IETF WIMSE Working Group | Charter and scope for workload identity across cloud, multi-tenant and cross-trust-domain deployments, naming AI agents as a use case. | <https://datatracker.ietf.org/wg/wimse/about/> |
| 18 | draft-ni-wimse-ai-agent-identity-02 | Huawei submission on WIMSE applicability to agentic AI, introducing an owner who binds agent identity to a principal by signature. | <https://datatracker.ietf.org/doc/draft-ni-wimse-ai-agent-identity/> |
| 19 | draft-klrc-aiagent-auth-00 (AIMS) | Conceptual model composing WIMSE, SPIFFE and OAuth for agent authentication and authorization. | <https://www.ietf.org/archive/id/draft-klrc-aiagent-auth-00.html> |
| 20 | SPIFFE | Workload identity framework whose concepts WIMSE is chartered to standardise; production deployments at large infrastructure operators. | <https://spiffe.io/> |
| 21 | FIDO Alliance agentic initiatives | April 2026 announcement of an Agentic Authentication TWG plus agent-commerce specification work seeded by Google AP2 and Mastercard Verifiable Intent. | <https://fidoalliance.org/fido-alliance-to-develop-standards-for-trusted-ai-agent-interactions/> |
| 22 | Linux Foundation A2A | First-year status: 150+ supporting organisations, AP2 with 60+ payments backers, UCP interoperation via the AP2 mandates extension. | <https://www.linuxfoundation.org/press/a2a-protocol-surpasses-150-organizations-lands-in-major-cloud-platforms-and-sees-enterprise-production-use-in-first-year> |
| 23 | OpenID Foundation AIIM CG | Artificial Intelligence Identity Management Community Group; biweekly subgroups and the October 2025 agent security whitepaper. | <https://openid.net/cg/artificial-intelligence-identity-management-community-group/> |
| 24 | DIF Identifiers and Discovery WG | Universal resolver and registrar frameworks, well-known DID discovery, a chain-free peer method, and machine-readable DID method traits. | <https://identity.foundation/working-groups/identifiers-discovery.html> |
| 25 | ERC-8004 Trustless Agents | Ethereum standard giving agents identity, reputation and validation through three registries; ERC-721 identity token URI pointing to an offchain agent card. | <https://eips.ethereum.org/EIPS/eip-8004> |
| 26 | NIST CAISI AI Agent Standards Initiative | Announced 17 February 2026 on three pillars including ISO/IEC JTC 1 leadership, NSF co-invested open-source protocol work, and identity infrastructure research. | <https://www.nist.gov/caisi/ai-agent-standards-initiative> |
| 27 | NIST NCCoE concept paper | Frames agents as commonly treated like generic service accounts without dedicated identity, authorization or accountability controls. | <https://www.nccoe.nist.gov/projects/software-and-ai-agent-identity-and-authorization> |
| 28 | IMDA Model AI Governance Framework for Agentic AI | Singapore, January 2026; requires a verifiable digital identity per agent plus an audit trail of who authorised what. | <https://www.imda.gov.sg/-/media/imda/files/about/emerging-tech-and-research/artificial-intelligence/mgf-for-agentic-ai.pdf> |
| 29 | Cloud Security Alliance research note | Analysis of the NIST initiative, the CSA Agentic Trust Framework of 2 February 2026, and the OWASP Agentic Top 10 risk categories. | <https://labs.cloudsecurityalliance.org/research/csa-research-note-nist-ai-agent-standards-federal-framework/> |
| 30 | Coalition for Secure AI | Cross-vendor security coalition whose founding members include Anthropic, Cisco, Google, IBM, Intel, Nvidia and PayPal. | <https://www.coalitionforsecureai.org/> |
| 31 | Google Secure AI Framework 2.0 | Agent risk map naming rogue-action and over-permissioned-tool risks with principles of well-defined controllers, limited powers and observable actions. | <https://saif.google/> |
| 32 | Microsoft Entra Agent ID | Vendor agent identity within a single enterprise perimeter. | <https://learn.microsoft.com/en-us/entra/agent-id/> |
| 33 | Hu and Rong, Inter-Agent Trust Models | Comparative study of A2A, AP2 and ERC-8004 across six trust models, evaluated on security, privacy, latency, cost and Sybil resistance. | <https://arxiv.org/pdf/2511.03434> |
| 34 | Agent identity landscape survey (2026) | Reviews roughly 80 sources across IETF, OpenID Foundation, W3C, NIST and regulatory corpora on non-human and workload identity for agents. | <https://arxiv.org/html/2604.23280v1> |
| 35 | Biscuit authorization token specification | Eclipse Foundation token format with Ed25519 chaining and Datalog policy, used as the cryptographic primitive in Annex C. | <https://www.biscuitsec.org/> |
