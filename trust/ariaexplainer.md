# Agent identity and authorization — a plain-language explainer

*A reference note for anyone following this thread without a security background. It explains the problem, decodes the jargon, and summarizes the two proposals under discussion (ARIA, and Bacon/Siwei's admission-invariant idea).*

*Thread: https://lists.w3.org/Archives/Public/public-agent-identity/2026Jul/thread.html*

*Sources: the W3C Agent Identity Registry Protocol CG page; Adolfo Grego Micha's list message of 13 Jul 2026; aria.bar and its spec/protocol pages; Bacon (Siwei)'s reply of 17 Jul 2026. Corrections welcome — please flag anything misrepresented.*

## The problem, in one picture

Think of a valet at a hotel. Before he drives your car, two separate things need to be true. First, he has to actually be the hotel's valet and not a stranger in a vest — that's **identity**. Second, even a real valet is only allowed to park the car, not drive it home for the weekend — that's **authorization**. Identity is "who are you"; authorization is "what are you allowed to do." They are different checks, and you need both.

AI agents now do things on our behalf across the internet — move money, send email, call other companies' systems — thousands of times a second. When an agent shows up at some service, that service faces the same two questions: is this agent really who it claims, and is it allowed to do this particular thing? Today there's no shared way to answer either. Every company invents its own, and none of them talk to each other. The W3C group that Adolfo chairs exists to build a common standard so any service can check both automatically.

## A short glossary (everything you need to read the rest)

- **DID (Decentralized Identifier).** A special kind of ID, a bit like a web address for a "thing," that comes with a way to look up its public keys so you can check its signatures. It doesn't depend on any single company to vouch for it.
- **Verifiable Credential (VC).** A digital, tamper-proof "card" — like a driver's licence — signed by whoever issued it. Anyone can check the signature is real without phoning the issuer. In ARIA the agent's credential is called an **AID**.
- **Public-key signing.** A signature only the holder of a secret key can make, which anyone can verify with the matching public key. It proves a message really came from that holder and wasn't altered.
- **Ed25519.** A widely used, fast signing algorithm. It's "classical" (see below).
- **Hash.** A short fingerprint of some data. Change one character in the data and the fingerprint changes completely. Used to detect tampering.
- **Append-only ledger.** A logbook you can only add to, never quietly edit. Each entry is linked to the one before, so altering an old entry breaks the chain and is detectable. Good for audit trails.
- **Revocation.** Cancelling a credential — the "kill switch" for when a key is stolen or an agent goes rogue.
- **DNS.** The internet's address book, which turns names like `example.com` into the information needed to reach them. It can also hold small text notes (called **TXT records**) that a domain publishes about itself.
- **DNSSEC.** An add-on that cryptographically signs DNS entries so they can't be forged. Important caveat: it isn't switched on everywhere, so you can't assume it's present.
- **DANE / TLSA record.** A way to publish, in DNS, exactly which cryptographic key a service should be using. It only means anything if DNSSEC is on — without DNSSEC the entry can be faked.
- **HSM.** A tamper-resistant hardware box that holds secret keys so they can't be copied off the machine.

## Classical vs. post-quantum (the crypto point people keep raising)

"Classical" cryptography — like Ed25519 — is the signing math we use everywhere today. It's safe because certain problems are far too hard for any normal computer to crack.

A **quantum computer** is a very different kind of machine. Large enough ones don't exist yet, but they're expected eventually — and they could crack exactly those problems quickly. So a signature that's unbreakable today could become forgeable once quantum computers mature.

**Post-quantum** cryptography is a newer set of algorithms designed to stay safe even against a quantum computer. The US standards body NIST has standardized these; the main signing one is **ML-DSA**, published as **FIPS 204**.

Why it matters here: an agent's identity key may be used for years. There's a known worry called *"harvest now, decrypt later"* — an attacker records today's signed traffic and waits for quantum computers to catch up, then forges or breaks it retroactively. For a trust system meant to last, using only classical crypto is a gap. This is why the choice of algorithm keeps coming up.

## What ARIA is (Adolfo's project)

ARIA stands for **Agent Registry for Identity *and* Authorization** — note it covers *both* of the two questions above, not just identity. It's stewarded by the TrustLayer Foundation, a Mexican nonprofit; the W3C group is the open forum that shapes it. In plain terms, ARIA:

- Gives each agent a signed identity card (the **AID**), built on the standard **DID** and **Verifiable Credential** formats, anchored in **DNS**.
- Lets the agent **make and keep its own secret key** — ARIA issues the credential but never holds the private key.
- Signs using a **belt-and-braces pair**: a classical signature (Ed25519) *and* a post-quantum one (ML-DSA-65, FIPS 204) together, where **both must check out**. So it's covered whether or not quantum computers arrive.
- Offers **four trust levels, L0–L3**, matching a US government identity-assurance scale (NIST SP 800-63-4): L0 is free and instant (just email); higher levels add personal, organizational, and finally government-registry verification, with hardware-held keys at the top. DNS binding kicks in at L1.
- Has a **kill switch**: an append-only trust ledger plus a standard revocation list, so a compromised credential can be cancelled in real time.
- Includes the **Agent Trust Protocol (ATP)** — a three-step handshake, modelled on how email anti-spoofing (DMARC) works. A service publishes its admission rules in DNS; when an agent arrives it (1) proves its identity, (2) declares its intent — what it wants to do, for whom, with what data — and (3) the service checks that against its published policy before letting the agent touch anything.

Everything is published openly: the spec under a Creative-Commons licence, the developer kit under Apache 2.0, with a live registry you can test against.

## What Bacon (Siwei) proposes

Bacon describes a governance protocol for the "prove it happened and was authorized" side. In plain terms:

- He roots an agent's identity in DNS using **DANE/TLSA records** (see glossary), and signs with **Ed25519** plus a canonical JSON format (JCS) so two machines produce identical bytes to sign.
- His central idea is an **admission seal**: before an agent acts, it produces a small signed record — which agent, what action, what scope, a fingerprint of the policy in force, and a timestamp — and keeps these in a tamper-evident chain as an audit trail.
- The rule attached to the seal, written `Required(τ) ⊆ Supported(τ)`, means in plain words: *an agent may only do something if it stays within the powers it was actually granted.* (τ is just his symbol for "an action.")
- He frames trust as two checkable parts: identity ("is it who it claims") and authorization ("is it allowed"), with the second being where enforcement happens.
- Enforcement runs through **four gates** in his architecture: a capability-boundary check (blocks actions outside an agent's declared capability set), an "immune system" layer blocking known attack patterns via a set of contracts, an orchestrator that blocks low-confidence or high-uncertainty outputs, and a final arbitrator step (human, oracle, or heuristic) for the last call. The signed admission seal is the audit trail; the blocking itself happens at these gates, before an action executes.

## How the two relate — the original questions

Bacon initially presented his work as the "authorization half" that complements ARIA's "identity half." Read against ARIA's own description, that split didn't quite hold, and four questions followed from that — on how his seal differs from ATP, how his "granted powers" list is set and revoked, what mechanism actually blocks a disallowed action versus just logging it, why his crypto used only the classical half of ARIA's pair, and whether DANE/TLSA and ARIA's DNS TXT approach are really the same trust model. A fifth point noted that his contribution pointed to a marketplace listing rather than a citable, versioned spec.

## Update — Bacon's response (17 Jul 2026)

Bacon replied point by point on the list. Summary of where things landed:

- **Layering, not competing.** He now frames the admission-invariant as an *intra-agent* consistency check — internal to one system — that should feed into ATP's *inter-agent* handshake, rather than a rival protocol covering the same ground. ATP negotiates between two systems; his invariant checks a single action against a single system's own granted powers before that action goes out.
- **`Supported(τ)` provenance.** Currently comes from his own `capability_boundary` module, a runtime probe with six preset levels, maintained separately from ARIA. He agreed the clean answer is for it to be derivable from ARIA's credentials and ledger instead, so the invariant checks an action against the same authorization envelope ARIA already defines — an alignment point still to be worked out, not yet resolved.
- **Enforcement is real, not just logged.** He described the four gates above and said blocking happens before execution, with the signed seal providing the audit trail afterward rather than being the enforcement mechanism itself.
- **Post-quantum gap acknowledged.** His scheme currently uses Ed25519 only. He called this a genuine gap and put adding a composite Ed25519 + ML-DSA-65 signature — matching ARIA's approach — on his roadmap.
- **DANE vs DMARC-style TXT records.** He agreed these are different trust models, not interchangeable, and confirmed the DNSSEC dependency is a real soundness consideration on his side, since an unsigned zone makes a TLSA record spoofable.
- **Provenance resolved.** The prior marketplace listing has been replaced with a versioned, standalone specification published under CC-BY-4.0 (matching ARIA's own licence): `github.com/Liuyanfeng1234/governance-spec`. This is now the citable reference for evaluating the proposal.

## A second issue raised alongside this: extension and marketplace provenance

Separately from the ARIA/admission-invariant comparison, a broader concern was raised about open agent-skill marketplaces — using the ClawHub marketplace as the documented example, where a security audit found a meaningful share of listed extensions malicious, some able to persist by writing to an agent's memory files even after the credential that installed them is revoked.

Bacon, who publishes his own work on ClawHub, treated this as a serious and current problem rather than a hypothetical one:

- **Why it matters for identity/authorization standards.** A credential that says "this agent is authorized" doesn't cover what happens if the agent's own runtime has been altered by an uncredentialed extension. Revoking the credential doesn't undo a malicious write that already happened.
- **What already exists.** Content-addressed (hash-pinned) skill publishing would stop silent replacement attacks but isn't enforced; runtime sandboxing can catch known attack patterns but not novel ones; post-installation auditing catches some issues after the fact.
- **What's missing.** A **skill provenance chain** — a cryptographic link between a published skill and the agent that reviewed and approved it, comparable to what ARIA does for agent identity, but for the skill/extension itself rather than the agent invoking it.

Bacon's suggestion is that this becomes an explicit scoping question for the group: whether agent identity/authorization work should extend to cover extension and skill provenance, not just the identity of the agent making the request. This is now an open item for the list rather than something resolved in this exchange.
