# Inventory of Efforts Related to A2WF
## Agent-to-Web Governance: Existing Standards, Protocols, and Initiatives

*Compiled in response to the A2WF Community Group introduction by Wolfgang Wimmer, W3C public-aikr list, 13 May 2026*
*Source post: https://lists.w3.org/Archives/Public/public-aikr/2026May/0001.html*

---

## How to Read This Inventory

A2WF addresses a specific gap: **machine-readable governance of what autonomous AI agents may *do* on websites** — fill forms, book appointments, make purchases, submit requests — and under what conditions (authentication, human verification, rate limits, accountability). The entries below are grouped by how closely they address that same gap, from core overlaps to adjacent and complementary work.

---

## PART 1 — AT W3C

### 1.1 A2WF Community Group (the group itself)
| Field | Detail |
|---|---|
| **Name** | Agent-to-Web Framework (A2WF) Community Group |
| **Status** | Active, launched 2026 |
| **URL** | https://www.w3.org/community/a2wf/ |
| **Scope** | Machine-readable declarations of what AI agents may do on a website: permissible actions, authentication requirements, human-oversight triggers, transactional governance |
| **Relationship to A2WF** | This is the group itself — included here for reference |

---

### 1.2 Web & AI Interest Group (WAI-IG)
| Field | Detail |
|---|---|
| **Name** | Web & AI Interest Group |
| **Status** | Charter approved November 2025, active |
| **URL** | https://www.w3.org/groups/ig/webai/ |
| **Scope** | Forum for exploring how emerging AI technologies intersect with Web technologies. Coordinates AI-related work across W3C, incubates topics that may feed into Working Groups |
| **Relevance** | Horizontal coordination body — A2WF output could feed here for cross-group alignment and eventual Working Group track |

---

### 1.3 AI Agent Protocol Community Group
| Field | Detail |
|---|---|
| **Name** | AI Agent Protocol Community Group |
| **Status** | Active, launched May 2025; first draft specification published August 2025 |
| **URL** | https://www.w3.org/community/agentprotocol/ |
| **Spec** | https://w3c-cg.github.io/ai-agent-protocol/ |
| **Scope** | Inter-agent communication protocols, agent identity models (based on W3C DIDs), standardised metadata formats for agent capabilities, security and privacy mechanisms for cross-origin agent interactions |
| **Relevance** | Addresses *how agents identify themselves and communicate with each other* — directly relevant to A2WF's authentication and accountability layer. A2WF builds the website-side governance; this group builds the agent-side identity that A2WF would check |
| **Note** | Co-chaired by Gaowei Chang (Agent Network Protocol / ANP) and Song Xu (China Mobile); 50+ participants |

---

### 1.4 Autonomous Agents on the Web (WebAgents) Community Group
| Field | Detail |
|---|---|
| **Name** | Autonomous Agents on the Web (WebAgents) CG |
| **Status** | Active, proposed 2023 by Fabien Gandon |
| **URL** | https://www.w3.org/community/webagents/ |
| **Charter** | https://www.w3.org/community/webagents/charter/ |
| **Scope** | Design of Web-based Multi-Agent Systems (MAS) that are internet-scalable, evolvable, and human-centric. Emphasises Linked Data / Semantic Web standards, hypermedia-driven agent interaction (Hypermedia MAS), and integration with Web of Things |
| **Relevance** | Complementary to A2WF: where A2WF focuses on website-side governance declarations, WebAgents focuses on the architectural and semantic foundations of how agents navigate and act on hypermedia. Close collaboration opportunity, especially on semantic policy representation |

---

### 1.5 Agentic Arbitration Protocol Community Group
| Field | Detail |
|---|---|
| **Name** | Agentic Arbitration Protocol Community Group |
| **Status** | Launched November 2025 |
| **URL** | https://www.w3.org/community/groups/ (search "Agentic Arbitration") |
| **Scope** | Protocols for resolving disputes and arbitrating conflicts in multi-agent agentic interactions — including cases where agent actions cause unintended effects or exceed authorised scope |
| **Relevance** | Directly relevant to A2WF's governance and accountability objectives: complements A2WF's preventive governance layer with a dispute-resolution and remediation layer |

---

### 1.6 Semantic Agent Communication Community Group
| Field | Detail |
|---|---|
| **Name** | Semantic Agent Communication Community Group |
| **Status** | Launched November 2025 |
| **URL** | https://www.w3.org/community/blog/2025/11/09/proposed-group-semantic-agent-communication-community-group/ |
| **Scope** | Ontology and semantic structures for communication between AI agents operating as delegated and accountable technical principals. Proposes ontology files at github.com/slashlifeai/agent-ontology |
| **Relevance** | Highly relevant to A2WF's policy representation and terminology layer: shared semantic models for agent roles, delegation, accountability, and permissions directly feed A2WF's machine-readable governance vocabulary |

---

### 1.7 NLWeb Community Group
| Field | Detail |
|---|---|
| **Name** | NLWeb Community Group |
| **Status** | Created October 2025 |
| **URL** | https://www.w3.org/community/nlweb/ |
| **GitHub** | https://github.com/microsoft/NLWeb |
| **Scope** | Microsoft-originated open project enabling websites to expose structured, conversational interfaces to AI agents using existing standards (Schema.org, RSS, sitemaps, MCP). Websites add an `/ask` endpoint that agents can query in natural language instead of scraping HTML |
| **Relevance** | NLWeb addresses the *interface* side of A2WF's problem — how agents access website content and capabilities in a structured way. A2WF addresses the *governance* side — under what rules. The two are directly complementary: NLWeb gives agents a machine-readable interface; A2WF gives them a machine-readable permission and governance layer |

---

### 1.8 AI-Driven Web Standards Specification Community Group
| Field | Detail |
|---|---|
| **Name** | AI-Driven Web Standards Specification Community Group |
| **Status** | Created November 2025 |
| **URL** | https://lists.w3.org/Archives/Public/public-new-work/2025Nov/subject.html |
| **Scope** | Development of web standards specifications specifically driven by AI capabilities and requirements — covering how AI changes the requirements for existing web standards |
| **Relevance** | Umbrella scope that includes the problem space A2WF addresses; potential coordination partner for standardisation pathway |

---

### 1.9 WebMCP (Web Model Context Protocol) — WICG Incubation
| Field | Detail |
|---|---|
| **Name** | WebMCP |
| **Status** | Under active discussion, WICG / Web & AI IG; discussed at TPAC 2025 |
| **URL** | https://www.w3.org/blog/2025/ai-at-tpac-2025/ |
| **Scope** | Allows websites to expose their JavaScript functionality as "tools" for AI agents (particularly browser-embedded agents) to call securely, client-side — bypassing brittle DOM parsing or screenshot interpretation. Includes consent and permissions model for sensitive actions |
| **Relevance** | Core to A2WF's problem domain: WebMCP provides the programmatic action interface; A2WF provides the governance metadata that wraps it. At TPAC 2025, discussions specifically covered managing consent and permissions for sensitive agent actions — exactly A2WF's remit. Agentic payments and auditable consent logs were discussed in this context |

---

### 1.10 AI KR (Artificial Intelligence Knowledge Representation) Community Group
| Field | Detail |
|---|---|
| **Name** | AI KR Community Group |
| **Status** | Active; this is the list where Wolfgang's A2WF introduction was posted |
| **URL** | https://www.w3.org/community/aikr/ |
| **Chair** | Paola Di Maio |
| **Scope** | Knowledge representation, conceptual modelling, vocabularies, semantics, provenance, interoperability, and explainability in AI |
| **Relevance** | As Wolfgang notes directly: AI KR provides the semantic and ontological vocabulary layer that A2WF needs to express governance policies in a machine-readable, interoperable way. Collaboration already confirmed (Paola Di Maio is an A2WF participant) |

---

### 1.11 W3C Verifiable Credentials Working Group
| Field | Detail |
|---|---|
| **Name** | Verifiable Credentials Working Group |
| **Status** | Active; VC Data Model 2.0 published 2024 |
| **URL** | https://www.w3.org/groups/wg/vc/ |
| **Scope** | W3C standard for cryptographically verifiable, tamper-evident credentials — digital proofs of identity, authorisation, and attributes |
| **Relevance** | The foundational identity primitive for AI agent governance. A2WF's authentication requirements — "where authentication is required" — will need verifiable credentials for agents to prove identity and delegated authority to website operators. Multiple IETF drafts (see Part 2) build on W3C VCs for agent auth |

---

### 1.12 Decentralised Identifiers (DID) Working Group
| Field | Detail |
|---|---|
| **Name** | Decentralised Identifiers (DID) Core — W3C Recommendation |
| **Status** | W3C Recommendation (published 2022); DID WG 2.0 in planning |
| **URL** | https://www.w3.org/TR/did-core/ |
| **Scope** | A type of identifier that enables verifiable, decentralised digital identity — unique identifiers that are not controlled by any central authority, with cryptographic proof of control |
| **Relevance** | Agent Network Protocol (ANP) and multiple IETF drafts use DIDs as the identity layer for AI agents. A2WF's authentication requirements will likely reference DID-based agent identities as the mechanism by which a website operator can verify who (or what) is requesting to take an action |

---

### 1.13 WAI-ARIA / Accessibility and Agent Semantics (TPAC 2025 Discussion)
| Field | Detail |
|---|---|
| **Name** | WAI-ARIA (Accessible Rich Internet Applications) |
| **Status** | Active W3C standard; agent-applicability under discussion |
| **URL** | https://www.w3.org/TR/wai-aria/ |
| **Scope** | Semantic markup for making web interfaces accessible to assistive technologies |
| **Relevance** | At TPAC 2025, a dedicated discussion examined whether ARIA (designed for human accessibility) is sufficient for machine agents, or whether a new machine-facing semantic layer is needed — specifically for flagging destructive or irreversible actions. This is directly A2WF territory: the governance metadata that distinguishes "read content" from "submit form" from "complete transaction" |

---

## PART 2 — AT IETF

### 2.1 AI Agent Authentication and Authorization (draft-klrc-aiagent-auth)
| Field | Detail |
|---|---|
| **Name** | AI Agent Authentication and Authorization |
| **Draft** | draft-klrc-aiagent-auth-01 |
| **URL** | https://datatracker.ietf.org/doc/draft-klrc-aiagent-auth/ |
| **Status** | Internet-Draft, March 2026; expires October 2026 |
| **Scope** | Proposes a model for authentication and authorisation of AI agent interactions using existing WIMSE (Workload Identity in Multi-System Environments) architecture and OAuth 2.0. Covers identity chaining, delegated authority, and cross-domain agent interactions |
| **Relevance** | Directly addresses A2WF's "where authentication is required" dimension at the protocol level. A2WF's governance declarations would specify *that* authentication is required; this draft specifies *how* it is implemented |

---

### 2.2 New Requirements for Auth in the AI Agents Era (draft-chen-ai-agent-auth)
| Field | Detail |
|---|---|
| **Name** | New requirements for Authentication and Authorization in the AI Agents era |
| **Draft** | draft-chen-ai-agent-auth-new-requirements-00 |
| **URL** | https://www.ietf.org/archive/id/draft-chen-ai-agent-auth-new-requirements-00.html |
| **Status** | Internet-Draft, January 2026; expires July 2026 |
| **Scope** | Analyses why traditional security models (authenticate identity → grant fixed permissions) fail for AI agents, which are non-deterministic and can take a wide range of unpredictable actions. Proposes new requirements for behavioural observability, scoped permissions, and continuous authorisation |
| **Relevance** | Foundational requirements analysis that directly informs A2WF's design — particularly the governance dimension of "what agents may do" and "when human verification is needed" |

---

### 2.3 Agent Identity Protocol (draft-aip-agent-identity-protocol)
| Field | Detail |
|---|---|
| **Name** | Agent Identity Protocol (AIP): Agentic Authentication and Authorized Policy Enforcement |
| **Draft** | draft-aip-agent-identity-protocol-00 |
| **URL** | https://datatracker.ietf.org/doc/draft-aip-agent-identity-protocol/ |
| **Status** | Internet-Draft, March 2026; expires September 2026 |
| **Scope** | Open standard for verifiable identity and policy enforcement for AI agents. Defines Agent Records, AIP Tokens (signed JSON on every tool call), AgentPolicy (YAML config declaring permitted tools, argument constraints, Data Loss Prevention rules, and Human-in-the-Loop requirements). Includes append-only audit log |
| **Relevance** | Extremely close to A2WF's core scope: the AgentPolicy construct directly parallels what A2WF wants websites to declare — which tools/actions are permitted, with what constraints, and when human approval is required. Good candidate for alignment or reference |

---

### 2.4 Security Requirements for AI Agents (draft-ni-a2a-ai-agent-security)
| Field | Detail |
|---|---|
| **Name** | Security Requirements for AI Agents |
| **Draft** | draft-ni-a2a-ai-agent-security-requirements-01 |
| **URL** | https://datatracker.ietf.org/doc/draft-ni-a2a-ai-agent-security-requirements/ |
| **Status** | Internet-Draft, February 2026; expires September 2026 |
| **Scope** | Security requirements across the full AI agent lifecycle: provisioning, registration, discovery, cross-domain interconnection, and access control. Covers per-workload and attribute-based access control |
| **Relevance** | Provides the security requirements baseline that A2WF's governance declarations would need to satisfy |

---

### 2.5 AIVS: Agentic Integrity Verification Standard (draft-stone-aivs)
| Field | Detail |
|---|---|
| **Name** | AIVS: Agentic Integrity Verification Standard |
| **Draft** | draft-stone-aivs-00 |
| **URL** | https://www.ietf.org/archive/id/draft-stone-aivs-00.html |
| **Status** | Internet-Draft, March 2026; expires September 2026 |
| **Scope** | Enables any party to independently verify that every action in an agent session is complete, unmodified, and attributable to a specific cryptographic identity — entirely offline. Provides tamper-evident audit trails for agent sessions covering form fills, JavaScript execution, purchases, and data extraction |
| **Relevance** | Directly addresses A2WF's accountability layer: once a website has declared governance rules and an agent has acted, AIVS provides the proof that those rules were followed and the action record is authentic |

---

### 2.6 VCAP: Verified Commerce for Agent Protocols (draft-stone-vcap)
| Field | Detail |
|---|---|
| **Name** | VCAP: Verified Commerce for Agent Protocols |
| **Draft** | draft-stone-vcap-00 |
| **URL** | https://datatracker.ietf.org/doc/html/draft-stone-vcap-00 |
| **Status** | Internet-Draft, 2026 |
| **Scope** | Secure, verifiable framework for commercial transactions initiated by AI agents — covering agent-to-merchant payment flows with cryptographic verification of agent authorisation and transaction consent |
| **Relevance** | Directly addresses one of A2WF's primary use cases: agents that "add items to carts" or "initiate transactions." VCAP provides the transaction-level verification layer that A2WF's governance rules would reference |

---

### 2.7 OAuth for Agentic AI Authorization (draft-rosenberg-oauth-aauth)
| Field | Detail |
|---|---|
| **Name** | OAuth for Agentic AI Authorization |
| **Draft** | draft-rosenberg-oauth-aauth-01 |
| **URL** | https://datatracker.ietf.org/doc/html/draft-rosenberg-oauth-aauth-01 |
| **Status** | Internet-Draft, 2026 |
| **Scope** | Extends OAuth 2.0 to support AI agent authorisation patterns — including delegated authority (agent acting on behalf of user), scoped action permissions, and chain-of-authority tracing |
| **Relevance** | A2WF's "where authentication is required" dimension will likely build on or reference this: the OAuth extension provides the mechanism by which an agent proves it has user authorisation to perform a specific action on a specific website |

---

### 2.8 Agent Identity Registry (draft-drake-agent-identity-registry)
| Field | Detail |
|---|---|
| **Name** | Agent Identity Registry System: A Federated Architecture for Hardware-Anchored Identity |
| **Draft** | draft-drake-agent-identity-registry-00 |
| **URL** | https://datatracker.ietf.org/doc/draft-drake-agent-identity-registry/ |
| **Status** | Internet-Draft, April 2026 |
| **Scope** | Federated registry architecture for issuing, managing, and verifying persistent identities for autonomous entities. Enables registration, key lookup, and revocation of agent identities at a system level |
| **Relevance** | Provides the infrastructure layer for A2WF's authentication requirements — a website operator needs a reliable way to look up and verify an agent's identity claim. This registry is that infrastructure |

---

## PART 3 — INDUSTRY PROTOCOLS (OPEN / PUBLIC DOMAIN)

### 3.1 Model Context Protocol (MCP)
| Field | Detail |
|---|---|
| **Name** | Model Context Protocol (MCP) |
| **Origin** | Anthropic (November 2024); donated to Linux Foundation Agentic AI Foundation (AAIF) December 2025 |
| **URL** | https://modelcontextprotocol.io / https://github.com/modelcontextprotocol |
| **Governance** | Linux Foundation AAIF (co-founded by Anthropic, Block, OpenAI; platinum members include AWS, Google, Microsoft, Cloudflare, Bloomberg) |
| **Scope** | Standard for connecting AI agents to external tools, data sources, and services. JSON-RPC client-server interface enabling structured tool invocation. Describes *what* a website/service can expose to an agent (tools, resources, prompts). WebMCP extends MCP to browser-embedded agents |
| **Relevance** | MCP is the most widely adopted agent-to-service interface standard (adopted by Claude, GPT, Gemini, Copilot, VS Code, Cursor etc.). A2WF's governance layer would sit *above* MCP: MCP says "here are the tools"; A2WF says "here are the rules for using those tools." Strong alignment opportunity |

---

### 3.2 Agent2Agent Protocol (A2A)
| Field | Detail |
|---|---|
| **Name** | Agent2Agent Protocol (A2A) |
| **Origin** | Google (April 2025); now Linux Foundation AAIF open-source project |
| **URL** | https://google.github.io/A2A / https://github.com/a2aproject/A2A |
| **Scope** | Enables AI agents from different vendors to discover each other's capabilities and collaborate. Uses "Agent Cards" (capability declarations in JSON) for peer discovery. Supports asynchronous HTTP + Server-Sent Events. Horizontal agent-to-agent communication, vs. MCP's vertical agent-to-tool communication |
| **Relevance** | When an AI agent acting on behalf of a user is itself orchestrating sub-agents (e.g. a travel agent delegating to a booking agent), A2A governs that interaction. A2WF's governance rules for the website would need to account for multi-agent chains — this is the protocol they operate on |

---

### 3.3 Agent Communication Protocol (ACP)
| Field | Detail |
|---|---|
| **Name** | Agent Communication Protocol (ACP) |
| **Origin** | IBM BeeAI |
| **URL** | https://agentcommunicationprotocol.dev |
| **Scope** | RESTful HTTP-based protocol for agent communication using MIME-typed multipart messages, synchronous and asynchronous interactions, session management, message routing, and flexible authentication including RBAC and DID systems |
| **Relevance** | A general-purpose complement to MCP and A2A; relevant to A2WF wherever agents communicate with website services through REST interfaces |

---

### 3.4 Agent Network Protocol (ANP)
| Field | Detail |
|---|---|
| **Name** | Agent Network Protocol (ANP) |
| **Origin** | Open-source community, led by Gaowei Chang (also W3C AI Agent Protocol CG co-chair) |
| **URL** | https://agent-network-protocol.com |
| **Scope** | Layered protocol for cross-platform agent collaboration using W3C DIDs for cryptographic identity, JSON-LD for semantic capability discovery, and end-to-end encryption. Designed for internet-scale, decentralised agent-to-agent and agent-to-service communication |
| **Relevance** | ANP's W3C DID-based identity layer directly addresses A2WF's authentication needs at the decentralised level; its semantic discovery layer is relevant to how agents locate and interpret A2WF governance declarations |

---

### 3.5 NLWeb (Microsoft)
| Field | Detail |
|---|---|
| **Name** | NLWeb |
| **Origin** | Microsoft (open-sourced May 2025) |
| **URL** | https://github.com/microsoft/NLWeb |
| **W3C CG** | https://www.w3.org/community/nlweb/ |
| **Scope** | Open project enabling any website to expose a conversational `/ask` interface to AI agents using existing web standards (Schema.org, sitemaps, RSS, MCP). Converts websites from human-first HTML to agent-accessible structured interfaces without requiring new infrastructure |
| **Relevance** | Provides the practical agent-access interface that A2WF's governance layer would annotate. A site implementing NLWeb could include A2WF governance declarations specifying which NLWeb endpoints are open, which require authentication, and which require human approval |

---

### 3.6 Really Simple Licensing (RSL)
| Field | Detail |
|---|---|
| **Name** | Really Simple Licensing (RSL) |
| **Origin** | RSL Collective (nonprofit, 2025); founding participants include Medium, Reddit, Yahoo |
| **URL** | https://www.rsl.dev |
| **Scope** | Open content licensing standard allowing web publishers to set terms for AI bots in robots.txt files, including whether content may be used for training, indexing, or inference, and under what commercial conditions (including collective bargaining mechanisms) |
| **Relevance** | RSL addresses the content-access and licensing dimension of A2WF's problem space. Where A2WF focuses on *actions*, RSL focuses on *content rights*. The two are complementary: RSL governs what an agent may read and use; A2WF governs what an agent may do |

---

### 3.7 Agentic Commerce Protocol (ACP) / Agent Payments Protocol (AP2)
| Field | Detail |
|---|---|
| **Name** | Agentic Commerce Protocol (ACP) / Agent Payments Protocol (AP2) |
| **Origin** | Google Agentic Commerce |
| **URL** | https://www.agenticcommerce.dev / https://github.com/google-agentic-commerce/AP2 |
| **Scope** | AP2 uses verifiable digital credentials (Mandates) to structure user intent and authorise agent-driven commerce. ACP uses shared, scoped payment tokens. Both discussed at W3C TPAC 2025 in the context of agentic payments, fraud detection, and auditable consent logs |
| **Relevance** | Directly addresses A2WF's transactional use case: agents that "add items to carts" or "initiate transactions" need a payment authorisation and consent protocol. A2WF's website-side governance declarations would specify which payment protocols are accepted and what consent scope is required |

---

## PART 4 — FOUNDATIONAL / ADJACENT WEB STANDARDS

### 4.1 robots.txt / Robots Exclusion Protocol (Extended for AI)
| Field | Detail |
|---|---|
| **Name** | Robots Exclusion Protocol (robots.txt), extended for AI |
| **Origin** | IETF (updating the 1994 standard); Cloudflare, Google, Apple extensions |
| **Relevant extensions** | Google-Extended, Applebot-Extended, Cloudflare Content Signals (categories: search / ai-input / ai-train) |
| **Scope** | Specifies which crawlers may access which parts of a website. Extended for AI to distinguish training vs. inference vs. search use, and to name specific AI system user-agents. IETF is updating the standard with intent-based policies and API endpoint discovery |
| **Relevance** | robots.txt is A2WF's closest existing analogue — it is already a machine-readable website-side declaration about what automated agents may do. However, it only addresses *read/crawl* access, not *transactional actions*. A2WF extends the concept from "what may you read" to "what may you do." Understanding this gap precisely is key to A2WF's positioning |

---

### 4.2 llms.txt
| Field | Detail |
|---|---|
| **Name** | llms.txt |
| **Origin** | Proposed by Jeremy Howard (fast.ai), 2024 |
| **URL** | https://llmstxt.org |
| **Scope** | A Markdown file at a site's root (`/llms.txt`) providing AI models with a concise, structured summary of important site content, documentation hierarchy, and navigation hints. Optimises AI content retrieval without heavy crawling |
| **Relevance** | Addresses AI *content access* rather than *action governance* — but represents the same design pattern A2WF uses: a root-level machine-readable declaration file. A2WF could be seen as extending the llms.txt pattern from content hints to action governance |

---

### 4.3 .well-known/ai-plugin.json (OpenAI Plugin Manifest)
| Field | Detail |
|---|---|
| **Name** | OpenAI Plugin Manifest / API declaration |
| **Origin** | OpenAI (2023, de-facto standard) |
| **URL** | Via .well-known/ai-plugin.json with OpenAPI schema |
| **Scope** | Hosted JSON file describing a website's API capabilities, authentication methods, and available endpoints for AI agent integration. Allows AI agents to discover and call site APIs without HTML parsing |
| **Relevance** | Early precursor to A2WF's machine-readable capability declaration. Where ai-plugin.json says "here are our API endpoints," A2WF says "here are the governance rules for those endpoints." Strong precedent for the design pattern |

---

### 4.4 Schema.org (Structured Data)
| Field | Detail |
|---|---|
| **Name** | Schema.org vocabulary |
| **Governance** | Schema.org community (W3C, Google, Microsoft, Yahoo, Yandex collaboration) |
| **URL** | https://schema.org |
| **Scope** | Shared vocabulary for structured data markup on web pages. Enables machine-readable description of products, events, organisations, actions, etc. Already widely used (JSON-LD in HTML) as the semantic layer agents use to understand page content |
| **Relevance** | NLWeb is built on Schema.org. A2WF's policy vocabulary for describing permitted actions could extend Schema.org's Action types and Offer/Service patterns — building on the most widely deployed semantic web standard rather than inventing a new vocabulary from scratch |

---

### 4.5 W3C Open Digital Rights Language (ODRL)
| Field | Detail |
|---|---|
| **Name** | ODRL Information Model 2.2 |
| **Status** | W3C Recommendation |
| **URL** | https://www.w3.org/TR/odrl-model/ |
| **Scope** | Policy expression language for specifying permissions, prohibitions, and obligations over digital content and services. Machine-readable, linked-data-based, extensible |
| **Relevance** | ODRL is the most mature W3C vocabulary for machine-readable policy expression. A2WF's governance declarations — "agents may book but not purchase," "human approval required for transactions over €50" — are structurally ODRL policies. Strong candidate for A2WF's underlying policy language |

---

### 4.6 W3C Data Privacy Vocabularies and Controls (DPVCG)
| Field | Detail |
|---|---|
| **Name** | Data Privacy Vocabularies and Controls Community Group (DPVCG) |
| **Status** | Active; DPV 2.0 published 2024 |
| **URL** | https://www.w3.org/community/dpvcg/ |
| **Scope** | Vocabulary for expressing data protection and privacy information: purposes, legal bases, data categories, processing activities, rights, consent. Designed for GDPR and similar regulatory compliance |
| **Relevance** | A2WF's governance layer must intersect with privacy law: an agent booking an appointment or submitting a form triggers data processing. DPVCG's vocabulary can express the privacy conditions under which an agent action is permitted — directly relevant to A2WF's EU AI Act compliance dimension |

---

## PART 5 — REGULATORY CONTEXT

### 5.1 EU AI Act
| Field | Detail |
|---|---|
| **Name** | EU Artificial Intelligence Act |
| **Status** | In force; significant obligations applying from August 2026 |
| **URL** | https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689 |
| **Relevance** | As Wolfgang notes, the EU AI Act imposes transparency, governance, accountability, and human oversight requirements on AI systems. A2WF can provide the technical mechanism by which website operators document and enforce these obligations at the point of agent interaction. Particularly relevant to high-risk AI use cases involving transactions, appointments, and form submissions |

---

### 5.2 NIST AI RMF (AI Risk Management Framework)
| Field | Detail |
|---|---|
| **Name** | NIST AI Risk Management Framework (AI RMF 1.0) |
| **Status** | Published January 2023; NIST AI RMF Playbook ongoing |
| **URL** | https://www.nist.gov/system/files/documents/2023/01/26/AI%20RMF%201.0.pdf |
| **Relevance** | Wolfgang notes A2WF has already contacted NIST. The AI RMF's GOVERN, MAP, MEASURE, MANAGE functions align with A2WF's goal of structured, governable agent interactions. A2WF's machine-readable declarations are a technical implementation of AI RMF GOVERN-level controls at the web interface layer |

---

## Summary Matrix

| Initiative | Layer | AI Reading | AI Acting | Auth/Identity | Human Oversight | Policy/Governance |
|---|---|---|---|---|---|---|
| **robots.txt (extended)** | Content access | ✅ | ❌ | ❌ | ❌ | Partial |
| **llms.txt** | Content hints | ✅ | ❌ | ❌ | ❌ | ❌ |
| **RSL** | Content licensing | ✅ | ❌ | ❌ | ❌ | ✅ |
| **ai-plugin.json** | API declaration | ✅ | Partial | Partial | ❌ | ❌ |
| **NLWeb** | Interface | ✅ | Partial | Partial | ❌ | ❌ |
| **MCP** | Tool invocation | ✅ | ✅ | Partial | ❌ | ❌ |
| **A2A** | Agent-agent | — | ✅ | ✅ | ❌ | ❌ |
| **ANP** | Agent-agent | — | ✅ | ✅ | ❌ | ❌ |
| **ACP/AP2** | Commerce | ✅ | ✅ | ✅ | Partial | Partial |
| **IETF auth drafts** | Auth/identity | — | ✅ | ✅ | ❌ | Partial |
| **W3C VC / DID** | Identity primitive | — | — | ✅ | ❌ | ❌ |
| **ODRL** | Policy language | — | — | — | ✅ | ✅ |
| **DPVCG** | Privacy policy | — | — | — | ✅ | ✅ |
| **WebMCP** | Browser actions | ✅ | ✅ | ✅ | Partial | Partial |
| **WebAgents CG** | Architecture | ✅ | ✅ | Partial | ✅ | Partial |
| **AI Agent Protocol CG** | Identity/comms | — | ✅ | ✅ | ❌ | Partial |
| **Semantic Agent Comm CG** | Ontology | — | ✅ | ✅ | ✅ | ✅ |
| **Agentic Arbitration CG** | Dispute resolution | — | — | — | ✅ | ✅ |
| **AIVS (IETF)** | Audit/integrity | — | — | ✅ | ✅ | Partial |
| **AIP (IETF)** | Policy enforcement | — | ✅ | ✅ | ✅ | ✅ |
| **A2WF (proposed)** | Website governance | — | ✅ | ✅ | ✅ | ✅ |

*Key: ✅ = directly addresses this dimension; Partial = addresses in part; ❌ = does not address; — = not applicable*

---

## Key Observations for A2WF

**1. The gap is real and unoccupied.** No existing initiative provides a machine-readable, website-side declaration of what agents may *do* (as opposed to read), under what governance conditions. robots.txt, llms.txt, and ai-plugin.json all address the read/access side. MCP and A2A address the protocol side. The governance, consent, and human-oversight layer on the website side is genuinely missing.

**2. A2WF is a governance wrapper, not a new protocol.** The strongest positioning for A2WF is as the layer that *sits above* MCP/A2A/NLWeb and specifies the conditions under which those protocols may be used on a given website — analogous to how a CORS policy sits above HTTP.

**3. ODRL is the natural policy language.** Rather than inventing a new vocabulary, A2WF should seriously evaluate W3C ODRL as its underlying policy expression language — it is already a W3C Recommendation, designed exactly for machine-readable permissions and prohibitions.

**4. Multiple IETF drafts are converging on the same space.** The IETF drafts on agent auth, AIP, and AIVS represent the closest existing technical work to A2WF's scope. Early liaison with their authors would prevent duplication and enable A2WF to reference rather than re-specify authentication and audit mechanisms.

**5. The EU AI Act creates urgency.** With significant AI Act obligations applying from August 2026, website operators need governance tools now. A2WF is well-positioned to provide the technical mechanism for EU AI Act compliance at the web interface layer.

---

*Document prepared for the A2WF Community Group inaugural meeting, 27 May 2026.*
*For errors, omissions, or suggested additions: file an issue in this github repo https://github.com/w3c-cg/aikr/blob/main/A2WF/intersection.md or post to public-aikr@w3.org*
