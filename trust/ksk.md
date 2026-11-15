# Root KSK rollover, W3C trust groups and AI KR

*Part of the AI KR CG trust work. Main document: [The Knowledge Representation of the Trust Layer](kroftrust.md). Trust record visualiser: [AI Agent Trust Record](https://w3c-cg.github.io/aikr/trust/AI_Agent_Trust_Record.html).*

## Rollover on 11 October

On 11 October the DNS root switches to a new key-signing key, KSK-2024 (key tag 38696), replacing KSK-2017 (key tag 20326). It is only the second root KSK change. The key anchors the DNSSEC chain of trust, and a validating resolver that does not trust the new key could leave its users unable to reach sites under any top-level domain.

- KSK-2024 has been published in the root DNSKEY set since early 2025, giving resolvers using RFC 5011 automatic updates time to accept it
- RFC 8509 trust anchor sentinels let anyone ask a supporting resolver whether it trusts a given root key; Cloudflare runs a readiness test at [dnstest.dev/ksk-2024](https://dnstest.dev/ksk-2024/)
- Both keys use RSA/SHA-256; ICANN has proposed a later algorithm rollover to ECDSA P-256
- ICANN plans to revoke KSK-2017, remove it from the root zone and delete its private key in 2027

A post-quantum DNSSEC chain will need a post-quantum KSK at the root and resolvers that trust it. That means another root rollover, and Cloudflare frames this one as practice for the anchor-update process it will require.

## W3C trust groups

No W3C community group thread found discusses the rollover event itself. The related discussion runs in the Credentials Community Group (CCG), on rooting decentralised identifiers (DIDs) in DNSSEC, and it has already produced an IETF draft.

| Date (2026) | Who | Contribution |
| :---- | :---- | :---- |
| 1 Aug | Ranjbar and Aravind | Publish [draft-ranjbar-dane-did-01](https://www.ietf.org/archive/id/draft-ranjbar-dane-did-01.html), crediting CCG participants |
| 22 Jul | [Kaveh Ranjbar](https://lists.w3.org/Archives/Public/public-credentials/2026Jul/0057.html) | Declares continuity of holding out of scope for the binding; points to RDAP registry events, stapled historical DNSSEC chains and witnessed append-only logs |
| 21 Jul | [Anivar Aravind](https://lists.w3.org/Archives/Public/public-credentials/2026Jul/0062.html) | DANE binds a key to a name but says nothing about who holds the name; after a transfer or drop-catch every signature still verifies to the IANA root |
| 19 Jul | [Brian Richter](https://lists.w3.org/Archives/Public/public-credentials/2026Jul/0046.html) | Proposes adding did:webvh to the profile's scope |
| 17 Jul | [Dmitri Zagidulin](https://lists.w3.org/Archives/Public/public-credentials/2026Jul/0043.html) | Backs a shared normative profile for DNS-using DID methods |
| 11 Jul | [Kaveh Ranjbar](https://lists.w3.org/Archives/Public/public-credentials/2026Jul/0041.html) | Proposes one DANE-EE key-binding profile for did:web high-assurance and did:dns, chained to the IANA root |

Provisions in the draft that touch the root anchor:

- A relying party MUST validate the DNSSEC chain from a trust anchor; a bogus result MUST fail verification
- A bogus, insecure or indeterminate lookup counts as failure, not absence, so a stripped response cannot demote a binding to a weaker fallback
- A stapled historical proof carries the TLSA record with its RRSIG, DNSKEY and DS records up to the publicly archived root trust anchor
- Key continuity (RFC 5011, trust-on-first-use) is kept separate from whether the party behind the name changed

Reading for the rollover: a DID verified under this profile through a resolver that missed KSK-2024 fails closed. Proofs stapled under KSK-2017 will depend on IANA's archived anchor once the old key is retired.

## Impact on AI KR

The CCG work supplies vocabulary the KR for Trust thread can adopt, and one gap the AIKR CG could fill.

**Anchor succession.** A rollover is a scheduled handover of trust with an overlap window, a cutover and a revocation. If agents and their credentials root in DNS, the ontology needs an anchor with a validity interval and a successor, plus an agent's trust state at a given moment.

**Currency vs historical validity.** The draft forbids accepting evidence that a binding was once valid as evidence that it is still current. This maps onto the deferred KRT items: resolved targets on receipts, and carried-versus-referenced evidence on audit reports. A stapled chain is carried evidence; an RDAP query is referenced evidence answering a different question.

**Scope ceiling.** A valid binding shows a key signed a document. It does not show whether a human or an agent operated the key; operator and accountability need separate claims. Ranjbar's companion draft, [DANE-Anchored Identity for Network Clients, Devices, and Autonomous Agents](https://datatracker.ietf.org/doc/html/draft-ranjbar-dane-anchored-identity-00), puts DNS-rooted agent identity on the table.

**Sentinel pattern.** RFC 8509 lets anyone ask a validator which anchors it trusts. AI agents have no equivalent. A KR concept for a trust state query, where an agent declares the anchors, vocabularies or authorities it currently accepts, is a contribution the CCG is not making.

## Open web and agentic web

The root KSK reaches W3C standards wherever a spec lets trust rest on a DNS name. DID Resolution standardises how a DID resolves to a document and leaves authenticity to each DID method. The root key enters a W3C trust chain only where a method makes DNSSEC normative.

**Relevance to open web standards.** did:web relies today on the WebPKI certificate at its domain and only recommends DNSSEC. The Ranjbar–Aravind profile would make DNSSEC validation mandatory for keys published under it. At that point the root KSK anchors every identifier bound this way, and each root rollover becomes an event for those identifiers.

**Open web.** The draft argues that DANE-EE takes the certificate authority out of the trust path and leaves the DNSSEC-signed name as sole authority for the key. Its case: cross-organisation identity needs one globally agreed root that is not a commercial CA, and the DNS root is the only candidate. The cost is concentration. Trust moves onto the DNS operator, the parent zone and the registrar, and compromise of a zone's keys compromises every key bound under it. A resolver that misses a new root key can lose reach to sites under every top-level domain.

**Agentic web.** A TLS session is short, but an agent may record an identifier and re-verify it much later or across an organisational boundary. If the domain changed hands in between, the verifier gets a correct answer with no signal that it now concerns a different party. A valid binding also does not show whether a human or an agent operated the key; the draft refers out to separate operator-of-record and decision-subject claims. A root rollover adds a third failure mode next to name transfer and key rotation. Under the draft's rules an agent resolving through a stale resolver fails closed, so the outage appears as agents refusing to act.

W3C trust specifications should state which root anchors they inherit and what happens to their claims across a rollover. None of the specifications reviewed here does so.

## Risks to everyday users: open questions

An everyday user's access to the web depends on a trust anchor they cannot see, check or choose. These questions are offered for answer by resolver operators, standards groups and researchers.

- **Stale resolver.** A validating resolver that does not trust KSK-2024 may leave its users unable to reach sites under any top-level domain. Does that loss extend to publishing as well as reading, since both start with a name lookup? How many users sit behind resolvers that have not taken up the new key, and who is counting?
- **Readiness lost later.** In 2018 resolvers lost learned trust in the new key during software upgrades and moves between machines. Can a resolver that is ready today lose readiness after a reinstall or migration? Once KSK-2017 stops signing, can a resolver restored with only the old anchor still learn the new one through RFC 5011, or does it need manual repair?
- **Misread failures.** Sites can be working yet unreachable. How would a user, or a support desk, tell a trust-anchor failure from an ordinary outage? What error signal reaches the person affected?
- **User control.** ISPs, enterprises and others run validating resolvers on users' behalf, and browser-based tests reflect whichever resolver path is in use, including VPN or Secure DNS. What means does an everyday user have to check their status, and what can they do if the answer is wrong? Who is accountable when a resolver operator misses a rollover?
- **Rollovers ahead.** KSK-2017 is due for revocation in 2027, ICANN has proposed an ECDSA algorithm rollover from 2027 to 2029, and a post-quantum root key will follow. Will each event carry the same risks, and does an algorithm change add new ones for resolver software that cannot verify the new signatures?
- **Identifiers.** Under draft-ranjbar-dane-did-01, a bogus or indeterminate lookup is a verification failure. Would DNS-bound credentials and agent identities stop verifying behind a stale resolver? How would a relying party, or an agent, learn why?

## TPAC 2026

Two issues have been opened on the TPAC 2026 pages to raise awareness of what could go wrong and to encourage communities and individuals to take up the topic during TPAC:

- Data Governance & Ownership mini-workshop: [w3c/tpac2026-miniworkshops#39](https://github.com/w3c/tpac2026-miniworkshops/issues/39)
- Breakout session: [w3c/tpac2026-breakouts#83](https://github.com/w3c/tpac2026-breakouts/issues/83)

## Sources

- [Cloudflare: The keys to the Internet change on October 11](https://blog.cloudflare.com/root-ksk-2024-rollover/)
- [Ranjbar, CCG introduction thread](https://lists.w3.org/Archives/Public/public-credentials/2026Jul/0041.html)
- [Zagidulin reply](https://lists.w3.org/Archives/Public/public-credentials/2026Jul/0043.html)
- [Richter reply](https://lists.w3.org/Archives/Public/public-credentials/2026Jul/0046.html)
- [Aravind on continuity of holding](https://lists.w3.org/Archives/Public/public-credentials/2026Jul/0062.html)
- [Ranjbar response](https://lists.w3.org/Archives/Public/public-credentials/2026Jul/0057.html)
- [draft-ranjbar-dane-did-01](https://www.ietf.org/archive/id/draft-ranjbar-dane-did-01.html)
- [IANA: Trust Anchors and Rollovers](https://www.iana.org/dnssec/files)
- [ICANN: Proposed Root KSK Algorithm Rollover](https://www.icann.org/en/public-comment/proceeding/proposed-root-ksk-algorithm-rollover-03-02-2026)
