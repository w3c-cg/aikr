# Authority Continuity: a Formal Model and Proposed Cases

*Contribution to group D (authority continuity). Proposed; open for
review by the AI KR CG. Case numbering is left to the editors.*

*Contributor's interest: the author is the editor of the PIC
specifications, stewarded by Nitro Agility S.r.l. PIC is published under
CC BY 4.0 at <https://pic-protocol.org/> and is not a standard.*

## Threat model

How can a relying party rely on an agent it does not trust, configured
by someone it does not know? The agent may be prompt-injected, mix
contexts or be wrong. PIC treats every executor as untrusted: executors
may be buggy, confused or adversarially influenced, and may hold several
authority sources at once. The adversary cannot forge the relationship
evidence or make a valid verifier accept a non-monotonic transition;
compromise of the verifier, the cryptographic root of trust or the
initial bootstrap is out of scope [2, §2, Threat Model and Scope].

Under this model an executor can act arbitrarily within its own step,
but what the next verifier accepts as valid authority is never wider
than what the executor received.

## Scope of the claims

The claims below are about accepted authority within a lineage, not
about physical effects. The model does not claim that an executor
cannot attempt an operation outside its authority; it claims that such
an operation cannot be accepted as a valid continuation [2, Theorem 6,
"Confused deputy is impossible under PIC"]. Protected effects must pass
through a mediated path, and effects must be attributed to the lineage
that caused them [5, Assumption 1, "Complete mediation"; Assumption 2,
"Causal attribution"]. Whether an executor may open a new lineage with its own authority is an
origination question outside the continuity invariant [1, §IV.A,
Limitations].

## A formal model for the scope variant of C9

PIC (Provenance Identity Continuity) models authority continuity as a
property of the execution lineage:

- the origin authority context `C_0` bounds every later step,
  `C_n ⊆ C_0` [2, Theorem 1, "PIC Safety"];
- each hop proves it is a valid continuation of its predecessor
  (Proof of Relationship);
- ordinary continuation never expands authority, `C_{i+1} ⊆ C_i`; any
  widening is an explicit, separately authorised transition, never an
  ordinary hop [4, Proposition 2, "Conservative ordinary-join
  authority"];
- continuity holds transitively as the composition of valid hops
  (Proof of Continuity).

The model is peer reviewed (accepted at IEEE NCA 2026 [1]) and its
definitions and theorems are machine-checked in Lean 4 [3]. In C9,
€5,000 is not a valid continuation of a €500 mandate, so the next
verifier rejects it. The revocation variant of C9 is outside this note.

## Proposed case: two valid mandates, one unauthorised effect

Alice lets agent C read her documents for a verification. Bob lets C
send official email. C emails Alice's document.

- **Current draft.** Each mandate is verified on its own and each chain
  is traced. R3 requires a decision on authority over the affected
  party, but no rule states what the combined authority of two mandates
  is, so the combination is left to the relying party's policy.
- **With the amendment.** The send causally depends on Alice's data and
  on Bob's mandate, so it is a join of two lineages. An ordinary join is
  bounded by the intersection of its parents' authority,
  `C(e) ⊆ C(p)` for every parent `p` [4, Proposition 2], which here
  contains neither read nor send. Combining them is admissible only as
  an explicit, separately authorised composition.
- **Resolves.** The confused deputy. Within the model, under complete
  mediation and causal attribution, the effect cannot be accepted
  [2, Theorem 6; 5, Corollary 2, "Exclusion of the confused deputy"].
  A buggy deputy may still attempt it; the result concerns acceptance,
  not attempt.

## Proposed case: a successor that does not exist when the step is emitted

X mandates A to process a refund. A places the payment step on a queue.
Which worker B takes it is decided by a scheduler, and B may be
instantiated after A has emitted the step.

- **Current draft.** Delegation is modelled as an artefact passed
  between parties (`grantedTo`). The case where the step is emitted
  before any successor exists is not treated.
- **With the amendment.** The continuation is not bound to a holder.
  Whichever executor takes the step must prove that its concrete step
  validly continues A's accepted step, under the authority and
  constraints A established; admissibility is evaluated by the receiving
  side at acceptance time, not by A at emission time [1, §I; 5, §8.2,
  Extended valid transition; 6, Prover and Verifier, "Delegating the
  Future"].
- **Resolves.** The N+1 Unknown Executor problem [1].

## Proposed case: authority that depends on a future fact (open)

X allows A to refund up to €500, and up to €800 only if a damage report
is confirmed. When X grants the mandate, no report exists.

- **Current draft.** A mandate carries a scope and a value limit, fixed
  at grant time: the exception is refused or granted too broadly.
- **Status.** PIC identifies this as the N+1 Outcome on Unknown Facts
  problem and leaves its treatment to future work [5, §19, Limitations
  and Future Work]. Evidence monotonicity gives a partial guarantee:
  withholding evidence can never turn a rejection into an admission
  [5, Appendix A, Worked Example]. A full treatment needs a
  representation of admissible future outcomes before their witnesses
  exist. Proposed for group D as an open item.

## Proposed case: authority mixing across concurrent executions

As in S4, many instances of A run in parallel. A serves two customers'
requests concurrently, with authority contexts `C_A = {refund order 1}`
and `C_B = {refund order 2}`. A bug in one instance constructs the
continuation of request B carrying authority from request A.

- **Current draft.** As C7 states, B checks the mandate against the
  action. Every permission in the mixed request is authentic and
  legitimately held by A, so a check of the individual artefacts
  passes. S4 is marked Gap for instance attribution in the coverage
  matrix.
- **With the amendment.** The mixed context `C'` is not a subset of `C_B`,
  so it is not a valid continuation of request B's lineage, whatever
  A's internal state. B does not rely on A's internal correctness; it
  verifies the continuation against the lineage [1, §I].
- **Resolves.** The N+1 Invalid State problem (authority mixing) [1].

## References

1. Gallo, N., Silvestri, S., Radesca, A. *Authority Continuity for
   Verifiable Lineage in Distributed Systems and AI Agents*. Accepted,
   24th IEEE International Symposium on Network Computing and
   Applications (NCA 2026), 10–13 November 2026.
   <https://www.nca-ieee.org/2026/>
2. Gallo, N. *Proof-of-Continuity: A Temporal Model for Authority
   Propagation in Distributed Systems and AI Agents*. Version 3, Zenodo,
   9 July 2026. <https://doi.org/10.5281/zenodo.21285112>
3. Gallo, N. *PIC Lean Verification*. Lean 4 formalization of the
   definitions and theorems of [2].
   <https://github.com/ngallo/pic-model/tree/main/draft/0.1/pic-model-math/pic-lean>
4. Gallo, N. *Full Provenance on the COSS Causal Axis: An Event-Level
   Closure of Causal Attribution and Confused-Deputy Exclusion*. Zenodo,
   2 October 2026. <https://doi.org/10.5281/zenodo.23102373>
5. Gallo, N. *Beyond Proof of Possession: A Relational Theory of
   Authority*. Zenodo, 25 September 2026.
   <https://doi.org/10.5281/zenodo.23102206>
6. PIC Specification 0.2. <https://github.com/pic-protocol/pic-spec>
7. PIC Protocol project site, with the specification set and the
   problem statements. <https://pic-protocol.org/>
