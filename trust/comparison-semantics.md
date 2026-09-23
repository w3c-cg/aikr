# Comparison semantics

*Full text of §4.1 of [kroftrust.md](kroftrust.md), which carries the short version. Arising from the discussion on public-aikr and public-agent-identity, and issue #10.*

## The property

The resolution properties proposed for the crosswalk in kroftrust.md — integrity resolution, availability resolution, freshness, revocation — establish properties of a single artefact. Integrity resolution establishes that an object is the right one. Availability resolution establishes that it can be obtained and is current. Freshness and revocation establish whether it still holds.

None of them establishes that two independently produced artefacts carrying the same identifier concern the same subject.

This matters because a trust decision often consumes more than one artefact. A relying party reading two receipts about the same action has to know whether they corroborate each other or conflict. Both can resolve cleanly, prove their respective propositions, and still not be comparable.

Canonicalization is the usual answer and it is a partial one. RFC 8785 (JCS) is a canonical form over the JSON data model: two documents equal in that model serialize to identical bytes, and the function is idempotent. That is the whole of what it provides.

The JSON data model has no notion of subject identity or reference. Canonical bytes establish that two artefacts are the same document. They do not establish that the document is about the same thing.

## Three failure classes, and they are not symmetric

Cases (a) and (b) follow from documented RFC 8785 behaviour rather than from implementation error, and both have been observed independently in two implementations: did:trail and AgentAvow's attestation layer. Case (c) lies outside RFC 8785 entirely. The distinction between the three matters more than any one of them.

**(a) Unicode normalization. Fails closed.**

JCS does not normalize. RFC 8785 section 3.1 requires that all components in a scheme depending on JCS preserve Unicode string data as is. A subject identifier in precomposed and decomposed form renders identically and canonicalizes to different bytes:

```
{"agent":"café-01"}   NFC   ...63 61 66 c3 a9 2d 30 31...
{"agent":"café-01"}   NFD   ...63 61 66 65 cc 81 2d 30 31...
```

A comparison reports a conflict between two artefacts that name the same subject. That is a false conflict, and the relying party sees it.

In key position it is harder to diagnose, because property names sort by UTF-16 code unit. An object carrying both forms as keys, alongside a key `z`, canonicalizes with `z` between them:

```
{"é":2,"z":3,"é":1}
```

Two keys that render identically, not adjacent in the output, and indistinguishable by eye.

**(b) Integers above 2^53. Fails open.**

JCS serializes numbers per ECMA-262. RFC 8785 Appendix B note (1) states that values to be interpreted as true integers SHOULD lie in the range -9007199254740991 to 9007199254740991; Appendix D recommends that numbers outside the JSON number type's range be carried as strings.

Where that guidance is not followed, two distinct identifiers converge:

```
{"subject":9007199254740993}  →  {"subject":9007199254740992}
{"subject":9007199254740992}  →  {"subject":9007199254740992}
```

Two subjects, one canonical form. A relying party comparing them concludes they are the same subject and proceeds. That is a false match, and nothing in the artefacts reveals it.

The same identifier carried as a string survives intact:

```
{"subject":"9007199254740993"}  →  {"subject":"9007199254740993"}
```

**(c) Divergent declared semantics. Fails open.**

Two producers use the same field name under different conventions: `{"refund":500}` where one means euros and the other means cents. Identical canonical bytes, different actions. Canonicalization cannot reach this at all, since both documents are correct under their own schema.

**The asymmetry is the point.** Case (a) produces a visible disagreement a relying party can investigate. Cases (b) and (c) produce agreement that is not there. A property that only says "pin a canonical form" treats all three alike and catches none of them.

The two fail-open cases are also distinct from each other, and the distinction determines the fix. In (b) the information was present in the input and the encoding lost it, so an encoding constraint recovers it. In (c) the information was never in the document at all, so no encoding constraint can recover it. Stated generally: (b) is a failure to bind what the encoding can lose; (c) is a failure to bind what the encoding never carried. This is why declared semantics is listed separately below rather than as a stricter form of numeric encoding.

## The attestation side

A signature changes what is at stake above without resolving any of it. An attestation over the canonical form — Ed25519 in both implementations, carried as a JWS in one and as a multibase `proofValue` on a `DataIntegrityProof` in the other — binds those exact bytes to a signer. It establishes who produced them and that they are unaltered. It establishes nothing about which subject they denote. The JSON data model carried no subject identity into the canonical bytes, and the signature carries none out.

The asymmetry therefore reappears one layer up, and it is sharper. Under case (a) two signers produce different canonical bytes for the same subject and each signs honestly. A verifier reading both sees two valid signatures over two different documents and records a conflict. The false conflict is now signed, but it stays visible and a relying party can investigate it.

Cases (b) and (c) are the dangerous pair, because the signature is verifying over the collision. A valid signature over a canonical form that two subjects share is a valid signature over a false match. The verifier recomputes the bytes, checks the signature, and it passes. The cryptography lends its authority to the wrong answer, and the stronger the proof the more convincing the error. A signature is evidence of integrity and origin; it is not evidence of reference, and it must not be read as if it were.

This bears directly on recomputability, which is the property the attestation exists to provide. Its value is that a relying party re-derives the canonical form from the evidence and checks the signature offline, trusting the computation rather than the issuer. That recompute reproduces the signer's bytes only when the canonicalization is identical in every respect the signer used: the same JCS, the same normalization decision before it, the same numeric-encoding rule. Where any is left unstated, the relying party's recompute diverges from the signer's and a sound attestation fails to verify.

The fail-open cases are worse than that, and worth stating precisely. Under case (b) there is no divergence at all. The signer carries the identifier as a number and loses the digit; the relying party recomputes and loses the same digit; both arrive at the same bytes. The recompute is exact and the signature verifies correctly. Nothing malfunctions anywhere, because the loss occurred before signing and identically on both sides. Recomputability is therefore necessary and not sufficient: it establishes that two parties performed the same computation, never that the computation preserved what distinguishes the subjects.

The properties listed below are therefore preconditions for comparing signed artefacts, not refinements of it. One addition follows from treating recomputability as the requirement. The canonicalization must be pinned as a parameter carried with the attestation and versioned independently of the verdict it canonicalizes, so a verifier selects the exact function the signer used and a change to that function is detectable on its own rather than folded into a change of content. A verifier that records the version without dispatching on it holds a label, not a guarantee: recomputation must select the serializer by the recorded version and fail closed on one it does not recognise.

Versioning is also what keeps the pin revisable. Without it, fixing a canonicalization is a one-way door, since any change invalidates every artefact already signed under the old function. With it, a profile can add a new version as active, retain the old one for verification of artefacts already issued, and migrate without breaking the record.

## What a profile must state

An artefact can pin JCS and still be non-comparable if any of the following is left unstated. The numeric requirement is a constraint rather than a disclosure, because case (b) is a silent collision and stating the encoding does not make it visible.

- **Canonical form.** Which canonicalization is pinned, carried as a version the verifier dispatches on and failing closed on an unrecognised one, as set out above.
- **Normalization.** Which Unicode normalization form is applied before canonicalization, if any. JCS applies none.
- **Numeric encoding.** Identifiers outside the range in RFC 8785 Appendix B note (1) MUST be carried as strings, per Appendix D. Stating the encoding is not sufficient: the requirement is to bind what the encoding would otherwise lose, which for a JSON number is the width that produced it.
- **Declared semantics.** The namespace, units or schema that fix what a field means. Distinct from numeric encoding because it binds what the encoding never carried at all.
- **Derivation.** Whether the derivation from evidence to artefact is recomputable by a third party.

## Use case

Two agents in a delegation chain independently produce receipts referring to the same tool invocation. A relying party assembling an account of what occurred has to determine whether the receipts describe one action or two.

With all five properties stated, it re-derives both to canonical bytes and compares. A difference is a genuine disagreement about the action.

With normalization unstated, two receipts describing the same action can differ because one producer's identifier was decomposed. The relying party reads a conflict where none exists.

With numeric encoding unconstrained, two receipts describing different actions can agree because both identifiers rounded to the same value. The relying party reads a single action where there were two, and nothing in either artefact indicates it.

## Boundary: declared against executed

The property above settles comparison of what was **declared**. It does not reach what was **executed**.

Syed Anas Mohiuddin reports a class of failure in independently built MCP servers in which an authorization check passes against the endpoint a tool call names, and a caller-supplied identifier argument is then interpolated into the outbound request path. Path normalization collapses a crafted value, and the request reaching the backend targets a different operation, under the same credential and within a valid, correctly scoped delegation chain.

Canonicalizing the declared call does not detect this, because the declared call is not what executed. The referent of an action attestation in such a system is the effect on the target system rather than the bytes of the call the agent emitted.

The presence of a receipt does not settle it either. Where these systems keep a session or audit log, the log commonly records the tool call as declared and the arguments as given, rather than the destination the request reached. A complete and faithful record can therefore be blind to this class, because every entry records the wrong side of the comparison. Evgenii Arsentev's counter over records that carry their evidence against those that only reference it needs a second axis here: of the records that carry evidence, how many carry evidence of the declaration and how many of the execution.

Binding an attestation to the executed effect, whether a canonical record of the request as sent or a server-side effect receipt, is the open extension. Two constraints follow and are noted rather than resolved here.

The receipt cannot be produced by the component that was retargeted, since the interpolation occurs inside it. It has to originate somewhere the argument cannot reach: the outbound client after the request is constructed, an observer on the wire, or the backend. And it has to carry the resolved target, the final path or URL after interpolation and normalization, rather than the declared arguments.

And an effect receipt is itself an artefact a relying party recomputes and compares, so the properties above apply to it. Path normalization introduces its own equivalence question, since percent-encoded and literal forms may be treated differently across stacks. A receipt canonicalized differently from the request it describes reproduces the same mismatch one layer down.

## Note on conformance vectors

Cases (a) and (b) reduce to fixed inputs with expected canonical output. A vector set carrying them is published as an independent author-set in the `draft-etcheverry-action-ref` conformance directory, anchored to the UTF-8 byte listing in RFC 8785 section 3.2.4 and the property-sorting test data in RFC 8785 section 3.2.3, so the set demonstrates agreement with the reference before reaching the cases the reference does not cover. Each vector states its failure mode, fails-open or fails-closed, so the asymmetry above is machine-readable rather than resting on this prose.

<https://github.com/giskard09/draft-etcheverry-action-ref/tree/main/conformance/trail>

Case (c) cannot be expressed as a conformance vector. The two documents are byte-identical, so no test over canonical output distinguishes them. That boundary is worth stating: the vector set can demonstrate what canonicalization loses, and cannot demonstrate what it never carried. Only the declared-semantics property reaches case (c).

A related point applies to any harness written in JavaScript. Property order must be read from the canonical string and never by parsing it back, because JavaScript hoists integer-like keys to the front of an object and so destroys the ordering under test. The RFC 8785 section 3.2.3 anchor contains the key `"1"` and will expose a harness that gets this wrong.
