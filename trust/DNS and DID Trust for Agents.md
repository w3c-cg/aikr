# DNS and DID Trust for Agents

Oct 31, 2026 · @Paola · Draft for comment

## Summary

Agent trust work is following two lines with different roots. DNS-anchored trust starts from the DNS root key and the registries below it. DID-anchored trust starts from keys the agent's controller holds and publishes in a DID document.

The split is less clean than it looks. The DID methods now used for agents (did:web, did:wba, did:atp) fetch their documents over HTTPS from a domain, so they already depend on DNS and the WebPKI, usually without DNSSEC. Bridging work exists at the IETF and in the W3C Credentials CG, but none of it has been adopted yet.

## Trust anchored in DNS

An agent is trusted because it speaks for a domain name. The chain runs from the domain up through its registry to the DNS root, whose key-signing key (KSK) anchors DNSSEC. The root switched to a new key, KSK-2024, in October; a resolver that does not trust the new key fails to validate anything under it ([AIKR note on the KSK rollover](https://github.com/w3c-cg/aikr/blob/main/trust/ksk.md)).

Most agent schemes bind identity to a domain, but few verify that binding with authenticated DNS. A2A agent cards and Web Bot Auth key directories are fetched from well-known paths over HTTPS, so their assurance comes from the WebPKI. Drafts that put agent data into DNS records themselves (ANS, DNS-AID, a shared `_ag` SVCB profile) are pre-1.0, and DNSSEC validation reaches roughly a third of users ([AIKR technical note on DNS anchoring](https://w3c-cg.github.io/aikr/trust/dns-dependency-agent-identity-note.html)).

The root of trust is clear and global. The cost is that registrars, registries and certificate authorities can revoke an agent's identity through domain suspension, transfer or lapse, with no relation to the agent's conduct.

For a plain-language account of DNSSEC and DANE as they apply to one agent registry, see the [ARIA explainer](https://github.com/w3c-cg/aikr/blob/main/trust/ariaexplainer.md).

## Trust anchored in DIDs

An agent is trusted because it can prove control of keys listed in its DID document, and because issuers vouch for it with verifiable credentials. No central registry is needed to create the identifier ([W3C DID Core](https://www.w3.org/TR/2021/WD-did-core-20210305/)).

The [Agent Trust Protocol specs](https://w3c-cg.github.io/atp/specs/) from Larry Lewis's ATP CG are drafts in this line. [did:atp](https://w3c-cg.github.io/atp/specs/did-atp/) binds an Ed25519 key and a post-quantum ML-DSA-65 key into one identifier, and trust levels travel as an ATP Trust Credential. Rotating either key produces a new DID.

Resolution is inherited unchanged from did:wba: the `did.json` document is fetched from the domain named in the identifier. The specs state the lineage did:web, then did:wba, then did:atp. They do not mention DNS, DNSSEC or how that web retrieval is secured, and they leave revocation open.

The AIKR [vocabulary crosswalk](https://w3c-cg.github.io/aikr/trust/Crosswalk.html) found that the Agent Identity Registry Protocol CG and the ATP CG both define DID-anchored trust negotiation, with no visible coordination between them as of July.

## Where they differ

The two lines answer the same question, who stands behind this agent, from opposite ends.

|  | DNS-anchored | DID-anchored |
| --- | --- | --- |
| Root of trust | DNS root KSK, then registry and registrar | Keys the DID controller holds |
| Proves | Control of a domain name | Control of keys; claims via credentials from issuers |
| Who can withdraw identity | Registrars, registries, CAs (suspension, transfer, lapse) | The controller (rotation, deactivation) or issuers (credential revocation) |
| Key change | Scheduled rollovers with overlap windows | did:atp: any key change yields a new DID |
| Failure mode | Resolver missing the current root key fails closed | Web-based methods inherit any weakness in the HTTPS fetch |
| Revocation signal | Missing or changed records under DNSSEC | Credential status lists; left open in the ATP drafts |
| Maturity for agents | Record formats pre-1.0; DNSSEC reaches a minority of users | Specs in draft; did:wba deployed through ANP |

## Bridges

The bridging work checks a DID against DNS, so a forger would need to compromise both the web host and the DNS zone.

- [High Assurance DIDs with DNS](https://datatracker.ietf.org/doc/draft-carter-high-assurance-dids-with-dns/) (Carter, Latour of CIRA; Glaude; Bouma), recommended by Markus Sabadello as the most advanced work on the topic. A `_did` URI record publishes the DID at the domain, TLSA records publish its keys, and a signed DID document must match both. DNSSEC is recommended, and a missing `_did` record can signal revocation. Individual submission, now expired at revision 08.
- [DANE profile for DIDs](https://www.ietf.org/archive/id/draft-ranjbar-dane-did-01.html) (Ranjbar and Aravind). One DANE-EE key-binding profile for did:web high assurance and did:dns, chained to the IANA root, proposed in the [W3C Credentials CG](https://lists.w3.org/Archives/Public/public-credentials/2026Jul/0041.html). Failed or stripped DNSSEC lookups count as failure.
- [DANE-Anchored Identity for Network Clients, Devices, and Autonomous Agents](https://datatracker.ietf.org/doc/html/draft-ranjbar-dane-anchored-identity-00) puts DNS-rooted agent identity on the IETF table.

No bridge yet covers did:wba or did:atp. Because both resolve from a domain, the did:web route above is the nearest fit. A credential that verifies under DNS does not show who operated the key, or whether the domain changed hands; those need separate claims.

## Questions for comment

1. Should agent DID methods that resolve from a domain (did:wba, did:atp) adopt a DNS binding such as the DANE profile, or state that the WebPKI is their anchor?
2. When the domain behind an agent's DID expires or changes hands, what happens to credentials issued to that agent, and who must act?
3. Can one revocation signal serve both lines, for example a removed `_did` record checked alongside a credential status list?
4. How should an agent record which trust anchors it accepts at a given moment, the way RFC 8509 sentinels let anyone query a resolver?
5. Which group should hold the bridging profile: the Credentials CG, ATP, the AI Agent Protocol CG, or the AIKR CG?

## Sources

- [Agent Trust Protocol specs](https://w3c-cg.github.io/atp/specs/) and [did:atp](https://w3c-cg.github.io/atp/specs/did-atp/), ATP CG drafts
- [High Assurance DIDs with DNS](https://www.ietf.org/archive/id/draft-carter-high-assurance-dids-with-dns-05.html), revision 05 text; [datatracker status](https://datatracker.ietf.org/doc/draft-carter-high-assurance-dids-with-dns/)
- [Kaveh Ranjbar, DANE-EE profile proposal](https://lists.w3.org/Archives/Public/public-credentials/2026Jul/0041.html), W3C Credentials CG
- [Root KSK rollover, W3C trust groups and AI KR](https://github.com/w3c-cg/aikr/blob/main/trust/ksk.md), AIKR CG
- [What the agentic web actually rests on](https://w3c-cg.github.io/aikr/trust/dns-dependency-agent-identity-note.html), ESL technical note for the AIKR CG
- [The Knowledge Representation of the Trust Layer](https://github.com/w3c-cg/aikr/blob/main/trust/kroftrust.md), AIKR CG draft note
- [W3C Decentralized Identifiers v1.0](https://www.w3.org/TR/2021/WD-did-core-20210305/)

Further material in the AIKR CG trust folder:

- [Knowledge representation for trust: vocabulary, use cases and working draft](https://w3c-cg.github.io/aikr/trust/trust-layer-thread-summary.html), with a glossary group on trust anchors and DNS
- [Key and evidence states](https://w3c-cg.github.io/aikr/trust/key-evidence-states.html), test cases for keys that age, rotate, are revoked or cannot be looked up
- [Agent Trust & Identity: Vocabulary Crosswalk Across W3C Community Groups](https://w3c-cg.github.io/aikr/trust/Crosswalk.html)
- [Agent identity and authorization explainer](https://github.com/w3c-cg/aikr/blob/main/trust/ariaexplainer.md) (ARIA)
