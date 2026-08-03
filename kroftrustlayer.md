# The Knowledge Representation of the Trust Layer Through the Lens of Digital Identity Chains

*W3C AI Knowledge Representation Community Group · Epistemic Systems Lab*

---

## Executive Summary

A cluster of W3C community groups has recently chartered work on agent identity, agent trust establishment, and runtime verification of agent claims. Their scopes overlap heavily. Their vocabularies converge. Their published founding texts diverge on one engineering property that determines whether any of the proposals will hold under production load, and none of them names it.

That property is **resolution dependency**: where an agent's identity document is fetched from at the moment a counterparty needs to verify a claim.

Three arrangements are in play across the current proposals — resolution from a distributed ledger, resolution from a domain the operator controls, and resolution from a registry a third party maintains. Each carries a different answer to who can make an agent disappear, a different latency profile at the ninety-ninth percentile, and a different failure mode under network partition or governance dispute. Charter text as published does not distinguish among them.

Distributed ledger technology sits in three distinct positions across this landscape. One proposal places public-chain receipts directly in scope as audit anchors. Another borrows ledger vocabulary for an append-only record model and disclaims blockchain and consensus mechanisms explicitly. A third carries no chain reference in its own text while the deployment that inspired it runs on an L2 network. A reader confined to charter documents would conclude that ledger infrastructure plays a marginal role in agent identity. Deployment evidence says otherwise.

The knowledge-representation problem is this: these charters are formal representations of systems that do not yet exist, and the representation omits the variable that governs the represented system's behaviour. What gets modelled is the trust relationship. What gets left unmodelled is the substrate the relationship depends on to hold at runtime. Ontologies built on the first without the second will crosswalk cleanly and interoperate poorly.

**Two deliverables follow.** [Part I](#part-i-technical-note) is a technical note addressed to the groups working in this space, ending in five questions each is invited to answer publicly. [Part II](#part-ii-editorial) is an editorial treatment of the same argument for the wire. [Part III](#part-iii-source-pool) lists the source pool.

**Related coverage.** This note extends the argument developed in [Digital identity trust anchors rest on operators no register names in words](https://global.factiva.com/redir/default.aspx?p=sta&ep=AE&an=CWRE000020260802em8200001&fid=301096886&cat=a&aid=9ZZZ038900&ns=65&fn=content-wire&ft=g&vl=ev&jid=FSP3da1fd7d-306a-4863-95a7-45c1a3a55e3a) (DID Press, 2 August 2026, 3,417 words, Document CWRE000020260802em8200001), which established that trust anchors in deployed digital identity systems terminate in operator control rather than in any registry of record. The present note applies that finding to the agent layer, where the anchor is consulted per call rather than per session.

---

<a id="part-i-technical-note"></a>

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

Ledger anchoring appears in scope for at least one proposed group, framed as public-chain audit receipts supplying verifiability that does not require trusting the operator, with chain selection declared out of scope on grounds of chain agnosticism. A second group disclaims the mechanism expressly: its semantic ledger model is presented as an implementation-independent logical model for ordered, immutable, verifiable records, with the charter stating that no blockchain or consensus mechanism is implied. That same charter maintains an editor role binding conformance and execution-record semantics to DID and VC ecosystems. A third group carries no chain reference at all in its published text; the deployment named as its inspiration source reports running a VC + DID trust layer anchored on an L2 network.

Reading the charters alone yields no reliable picture of which proposals depend on a chain and which do not.

### 3. Why resolution dependency is the governing variable

Decentralized identifiers are specified as decoupled from centralised registries, identity providers and certificate authorities. That specification describes what a DID is independent **of**. It stays silent on what a DID is dependent **on**.

Deployment practice has filled the silence. A substantial share of registered DID methods rely on ledger infrastructure to resolve. Every identity check therefore inherits the latency, availability and governance characteristics of whatever network sits beneath the method — properties that appear nowhere in the credential, the presentation, or the charter that specifies either.

Per-session authentication absorbs that inheritance without difficulty. Human login happens once and tolerates a resolution delay measured in seconds. Agent delegation behaves differently. When an agent calls a second agent, which invokes a tool, which reaches a third-party service, credential verification recurs at every hop. Recent work on delegation protocols spanning MCP and A2A identifies ledger-dependent resolution as incompatible with the throughput these call chains demand, an objection that has so far drawn little response from the groups whose designs it touches.

Single-network anchoring compounds the exposure. A deployment paper from one of the lineages represented in this cluster concedes the point without hedging: binding a judgement to one ledger inherits that ledger's mortality and politics, since any chain can halt, censor, reorganise or fork. Availability failure and governance capture arrive through the same door.

### 4. The knowledge-representation dimension

Each charter in this cluster functions as a formal representation of a system that has yet to be built. Representations of this kind are judged on what they commit their implementers to. Where a charter names identity, delegation, capability description and conformance, it commits to modelling those. Where it leaves resolution dependency unstated, implementers are free to choose substrates with incompatible operational characteristics while remaining conformant to the same document.

Two consequences follow for anyone building crosswalks across these groups. First, term-level alignment will succeed while behavioural alignment fails: `agent identity` maps cleanly from one vocabulary to another and tells a reader nothing about whether verification completes in four milliseconds or four hundred. Second, security properties described in charter prose are unwarranted until the substrate is pinned, because the assurance a credential offers is bounded by the availability of the thing that resolves it.

An ontology of the agentic trust layer that omits resolution dependency describes a trust relationship without describing the conditions under which the relationship holds.

### 5. The ask

Each group is invited to state, briefly and publicly:

1. **Resolution path.** What resolution path does your proposal assume, and is that assumption recorded anywhere normative?
2. **Latency budget.** What verification latency budget does your design target for agent-to-agent delegation, and has it been measured under realistic call-chain depth?
3. **Degradation.** What happens to identity verification when the resolution layer is unavailable, partitioned, or subject to governance dispute?
4. **Ledger justification.** Where a chain is involved, which properties does it supply that a domain-hosted or registry-hosted identity document cannot?
5. **Coordination.** Which other groups in the distribution list above have you coordinated with, and on what deliverable?

Responses will be collated and circulated back to all groups on the list. Replies to the AIKR CG list, or to your own list with a cross-post.

---

<a id="part-ii-editorial"></a>

## Part II — Editorial (wire version)

### Agent trust charters leave resolution dependency unspecified

A cluster of W3C community groups has chartered work on agent identity. Each proposes a way for an autonomous agent to prove who it is and who answers for it. Read side by side, their founding texts share vocabulary and diverge on the one engineering property that decides whether any of the proposals will hold under load.

Distributed ledger technology occupies three positions across these documents. A memory-interoperability proposal places public-chain receipts in scope as audit anchors, offering verifiability that avoids trusting the operator, while declaring chain selection itself outside its remit. A semantic-communication charter borrows ledger vocabulary for an append-only record model and then states plainly that no blockchain or consensus mechanism is implied, even as it maintains an editor role tying execution-record semantics to DID and VC ecosystems. A third group, working on agent identity registries, carries no chain reference in its own text; the deployment it names as inspiration reports running on an L2 network. Anyone reading only the charters would conclude that ledger infrastructure plays a marginal role here.

Deployment evidence points the other way, and the gap matters because of where verification sits in an agentic transaction.

Decentralized identifiers were specified to operate independently of centralised registries, identity providers and certificate authorities. That framing describes what a DID is decoupled from and says nothing about what it is coupled to. Most registered DID methods resolve through ledger infrastructure, which means every identity check inherits the uptime, latency and governance of the network underneath — properties that appear in no credential, no presentation and no charter.

Per-session authentication absorbs this comfortably. A person logs in once and waits a moment. Agent delegation behaves differently. An agent calls a second agent, which invokes a tool, which reaches a third-party service, and credential verification recurs at every hop rather than once at the boundary. Work on delegation protocols spanning MCP and A2A identifies ledger-dependent resolution as incompatible with the throughput these chains demand. Groups whose designs the objection touches have largely stayed quiet on it.

Anchoring to a single network compounds the exposure. A deployment paper from the registry lineage concedes the point directly: binding a judgement to one ledger inherits that ledger's mortality and politics, since a chain can halt, censor, reorganise or fork. Availability failure and governance capture come through the same door, and a protocol designed for neutrality acquires a dependency on a specific network's continued willingness to serve.

Three arrangements are live in current proposals. An agent's identity document may resolve from a chain, from a domain its operator controls, or from a registry a third party runs. Each supplies a different answer to who can make an agent vanish. Each carries a different tail-latency profile. Each fails differently during a partition. Charter text as published does not distinguish among them, which leaves implementers free to pick substrates with incompatible operational characteristics while claiming conformance to the same specification.

Consequences reach past engineering. Where an agent transacts on behalf of a person or a firm, the party able to withhold resolution holds an effective off-switch. Prior reporting established that trust anchors in deployed digital identity systems terminate in operator control rather than in any register of record. Agent delegation raises the stakes on that finding: what was consulted once per session is now consulted once per call, and whoever controls the resolution endpoint controls the agent's ability to act at all.

For groups building vocabularies and crosswalks, the omission produces a specific failure. Term-level alignment will succeed. An `agent identity` concept in one vocabulary maps cleanly onto its counterpart in another, and the mapping conveys nothing about whether verification completes in four milliseconds or four hundred. Behavioural alignment fails silently, and it fails at exactly the point where a subscriber, a regulator or an auditor would want it to hold.

Regulators reading these charters face a related difficulty. Assurance language describing cryptographic verification of agent claims reads as a security guarantee. Guarantees of that kind are conditional on the resolver answering. A charter that omits the resolver describes an assurance it has not committed to delivering.

Naming resolution dependency as a required disclosure would cost each group a paragraph. Publishing a measured latency budget for agent-to-agent delegation at realistic call-chain depth would cost considerably more, and would tell prospective adopters something the present documents cannot. Until one or the other appears, an implementer evaluating this landscape is choosing among proposals whose most consequential engineering decision has been left to the implementation.

*(≈1,050 words as drafted; expand to feed length during NITF assembly with the deployment-paper detail and the DID method survey figures.)*

---

<a id="part-iii-source-pool"></a>

## Part III — Source Pool

### Primary standards texts

| # | Resource | One-line description | URL |
|---|---|---|---|
| 1 | Decentralized Identifiers (DIDs) v1.1 | Candidate Recommendation Snapshot dated 5 March 2026; the normative source for the decoupling language this note turns on. | https://www.w3.org/TR/did-1.1/ |
| 2 | Verifiable Credentials WG charter (2026) | Rechartering that adds Confidence Method and the VC HTTP API, both bearing directly on runtime agent verification. | https://w3c.github.io/vc-charter-2026/ |
| 3 | Federated Identity WG charter | Defines the browser-mediated Digital Credentials API, the one place in this landscape where presentation is deliberately format- and protocol-agnostic. | https://www.w3.org/2025/02/wg-fedid.html |
| 4 | Decentralized Identifier WG charter (draft) | Covers DID maintenance plus consensus-building on resolution and DID URL dereferencing, where the resolution question formally lives. | https://w3c.github.io/did-wg-charter/ |

### Community group charters (fragmentation evidence)

| # | Resource | One-line description | URL |
|---|---|---|---|
| 5 | Agent Identity Registry Protocol CG | Verifiable credentials binding agents to controlling organisations for cross-organisational trust negotiation; the only group in the cluster listing external coordination targets. | https://www.w3.org/community/agent-identity/ |
| 6 | Agent Trust Protocol CG | Formed at the invitation of the AI Agent Protocol CG chairs, covering identity proof, trust establishment and privacy of the humans agents represent. | https://www.w3.org/community/atp/ |
| 7 | Semantic Agent Communication CG charter | Contains the explicit blockchain disclaimer alongside a Conformance and Semantic Ledger Editor role bound to DID/VC ecosystems. | https://w3c-cg.github.io/s-agent-comm/ |
| 8 | AI Agent Memory Interoperability CG proposal | Places public-chain receipts in scope as audit anchors while declaring the protocol chain-agnostic; also crosswalks NIST AI RMF, ISO/IEC 42001 and the EU AI Act. | https://www.w3.org/community/blog/2026/05/18/proposed-group-ai-agent-memory-interoperability-community-group-community-group/ |
| 9 | Agent Network Protocol white paper | The AI Agent Protocol CG's own document, arguing for self-hosted DID documents on the agent's domain and a federated architecture modelled on email. | https://w3c-cg.github.io/ai-agent-protocol/ |

### Literature

| # | Resource | One-line description | URL |
|---|---|---|---|
| 10 | Trust Without Trusting: A Recomputable Trust Protocol for Autonomous Agents | Deployment paper from the registry lineage reporting a live VC + DID layer on Base L2 and conceding the single-chain mortality problem. | https://arxiv.org/html/2605.06738 |
| 11 | AIP: Agent Identity Protocol for Verifiable Delegation Across MCP and A2A | Source of the throughput objection, with a gap analysis across eleven categories of prior identity work. | https://arxiv.org/pdf/2603.24775 |
| 12 | AI Agents with Decentralized Identifiers and Verifiable Credentials | Prototype multi-agent system using ledger-anchored DIDs, whose evaluation exposes limits when an LLM alone controls the security procedures. | https://arxiv.org/abs/2511.02841 |
| 13 | Autonomous Agents on Blockchains: Standards, Execution Models, and Trust Boundaries | Scoping survey covering agentic wallets, MPC and threshold signing, and policy-bypass risk in agent-driven transactions. | https://arxiv.org/pdf/2601.04583 |
| 14 | From Cloud-Native to Trust-Native: A Protocol for Verifiable Multi-Agent Systems | Argues for treating identity, policy and action as one composable architecture, with a critique of post-hoc blockchain auditing of model outputs. | https://arxiv.org/pdf/2507.22077 |
| 15 | Are We There Yet? A Study of Decentralized Identity Applications | Empirical survey of decentralized identity deployments and the interoperability shortfall between DID method implementations. | https://arxiv.org/pdf/2503.15964 |
| 16 | AESP: A Human-Sovereign Economic Protocol for AI Agents with Privacy-Preserving Settlement | Useful chiefly for its bibliography, which maps the autonomous-economic-agent literature back to 2020. | https://arxiv.org/pdf/2603.00318 |

### Prior coverage

| # | Resource | One-line description | URL |
|---|---|---|---|
| 17 | Digital identity trust anchors rest on operators no register names in words | DID Press, 2 August 2026, 3,417 words; established that trust anchors in deployed identity systems terminate in operator control rather than in a register of record. Document CWRE000020260802em8200001. | [Factiva](https://global.factiva.com/redir/default.aspx?p=sta&ep=AE&an=CWRE000020260802em8200001&fid=301096886&cat=a&aid=9ZZZ038900&ns=65&fn=content-wire&ft=g&vl=ev&jid=FSP3da1fd7d-306a-4863-95a7-45c1a3a55e3a) |

---

## Feed Plan

Seventeen sources support six to eight articles at feed length. Suggested splits:

1. **Charter fragmentation and the unspecified resolver** — Part II above, expanded.
2. **Resolution latency in agent delegation** — off AIP plus the DID method survey; quantitative where the papers permit.
3. **Single-chain governance capture** — halt, censorship, reorganisation and fork as identity-layer risks.
4. **Agent economics on-chain** — off the blockchain-agents scoping survey and AESP.
5. **The self-hosted alternative** — ANP's domain-hosted DID document approach and what it trades away.
6. **Standards-process piece** — how several overlapping groups cleared the five-supporter threshold in the same window with minimal cross-coordination.
7. **Regulatory read-across** — assurance claims in charter prose against EU AI Act and ISO/IEC 42001 conformance expectations.

Verification notes before shipping: fetch items 10 and 11 in full to confirm the throughput claim and the L2 anchoring detail directly rather than through search snippets; confirm the current count and status of registered DID methods against the DID Specification Registries before quantifying "most".
