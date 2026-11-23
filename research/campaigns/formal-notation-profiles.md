# Formal specification and proof language profiles

Independent review matched all 11 claim sources and all ten pinned classifier specimens. The six language identities and eight scoped discovery links retain the original editions, subject boundaries, and source coordinates. The AlloyTools executable repository and the historical mixed Lean classifier remain unresolved. [Independent lead decisions](../../sces/artifacts/formal-notation-crosswalk/independent-leads.json) · [Origin audit](../../sces/artifacts/formal-notation-crosswalk/origin-audit.json)

| Identity | Reviewed profile scope |
| --- | --- |
| Alloy | Alloy 6 signature categories, next-state expressions, and the documented purposes of `run` and `check`. |
| Dafny | 4.11.0 method conditions, modification frames, termination metrics, and ghost lemma boundaries. |
| Temporal Logic of Actions | Lamport’s original author manuscript on action state pairs, stuttering with respect to a state function, and weak and strong fairness. |
| TLA+ | The separately documented specification language, the author’s initial and next-state clock example, and named `INSTANCE` substitution in the first-printing reference. |
| Lean 3 | The 3.23.0 author text on dependent function types, propositions as types, and tactic proof construction. |
| Lean 4 | The 4.35.0 reference on dependent function types, proof irrelevance, and tactic proof states. |

The pinned classifier label `TLA` links to TLA+ for the two inspected module specimens. The original logic keeps its own identity. The Lean project README resolves to Lean 4 for that exact origin, while the historical `.lean` and `.hlean` classifier stays open. The evidence leaves release compatibility and formal lineage assignments open. [Exact scope witnesses](../../sces/artifacts/formal-notation-crosswalk/source-witnesses.json)

The review withheld the first TLA+ `EXTENDS` claim. The author’s reference explicitly keeps `LOCAL` definitions and `LOCAL INSTANCE` imports within their defining module. The first statement did not account for that scope. The separate `INSTANCE` statement covers the names supplied by a named instantiation. [Held claim](../../sces/records/claim/tla-plus-formal-module-extends--1.json) · [Independent assessment](../../sces/artifacts/formal-notation-crosswalk/independent-assessment.json) · [Research receipts](../../sces/artifacts/formal-notation-proof-research.jsonl) · [Independent review receipts](../../sces/artifacts/formal-notation-proof-review.jsonl)

Revision 2 now binds the global-definition rule and the local exception to the exact corrected author PDF. The new executions inspected printed pages 171 and 327 and preserved the first revision and its inconclusive assessment. [Corrected claim](../../sces/records/claim/tla-plus-formal-module-extends--2.json) · [Correction research receipts](../../sces/artifacts/ruby-cpp-tla-proof-research.jsonl) · [Correction review receipts](../../sces/artifacts/ruby-cpp-tla-proof-review.jsonl)
