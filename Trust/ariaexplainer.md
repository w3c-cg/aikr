# Agent identity and authorization — a plain-language explainer

*A reference note for anyone following this thread without a security background. It explains the problem, decodes the jargon, and summarizes the two proposals under discussion (ARIA, and Bacon/Siwei's admission-invariant idea).*

*Thread: https://lists.w3.org/Archives/Public/public-agent-identity/2026Jul/thread.html*

*Sources: the W3C Agent Identity Registry Protocol CG page; Adolfo Grego Micha's list message of 13 Jul 2026; aria.bar and its spec/protocol pages. Corrections welcome — please flag anything misrepresented.*

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

## How the two relate — the honest summary

Bacon presents his work as the "authorization half" that complements ARIA's "identity half." Read against ARIA's own description, that split doesn't quite hold, and the useful questions follow from that:

- **ARIA already does authorization.** Its Agent Trust Protocol is a full three-step "declare your intent, get admitted or refused" handshake — very close to Bacon's admission seal. So the real question is not "is authorization missing?" but "how does Bacon's seal differ from ATP, and what does it add?"
- **ARIA already has a kill switch.** It revokes credentials in real time. Bacon's rule depends on a list of "granted powers," but he doesn't say how that list is set or cancelled — so: does he build on ARIA's revocation, or run his own, and how do they stay in sync?
- **Enforcement vs. wishful thinking.** Bacon says the check "must hold" before an action. That states a rule but not a mechanism. What actually *blocks* a disallowed action — a gateway that refuses it, or just a log that notes it afterwards?
- **The crypto is half-aligned.** ARIA signs with a classical + post-quantum pair (both must verify). Bacon lists only the classical piece (Ed25519). So he has one half of ARIA's approach but not the quantum-resistant half — worth clarifying whether his is meant to be post-quantum.
- **Both use DNS, differently.** ARIA binds to DNS TXT records (the DMARC model); Bacon uses DANE/TLSA, which only holds up if DNSSEC is switched on. Whether these are really the same trust model, and whether the DNSSEC dependency is safe to assume, are open questions.

Finally, a point about *where the work lives*, which matters especially for a trust proposal: ARIA publishes a licensed, versioned spec, an open SDK, and a live registry — things the group can inspect and cite. Bacon's contribution currently points to a listing on an open-publish agent-skill marketplace rather than a citable specification. A versioned spec that can be read and referenced, independent of any marketplace, would let the group evaluate the idea on its merits.
