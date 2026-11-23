# Language Index scope and identity

Language Index covers notations with an identifiable rule set for expressing software computation, constraints, structured descriptions, or transformations. The boundary is the language and its governed forms. Each accepted entity needs its own evidence-backed identity decision.

## Subjects

| Category | Inclusion rule |
| --- | --- |
| Programming and scripting | Include general-purpose, systems, automation, functional, declarative, logic, and constraint languages with a documented identity. |
| Domain-specific and technical | Include separately identifiable query, assembly, hardware description, shader, modeling, and formal specification languages. |
| Historical, educational, and experimental | Apply the same identity rule. Record incomplete sources as evidence gaps and retain unresolved candidates. |
| Markup, stylesheet, templates, configuration, and data description | Include when the notation supplies a documented expression, constraint, transformation, or declaration model. A file container, serialization encoding, and bare record layout belong to a format index. A grammar or notation can remain a related candidate when it lacks a defensible language identity. |
| Libraries, frameworks, platforms, and execution environments | Record only material relationships and versioned references to their owners. A language API or named execution environment cannot supply a language identity by itself. |

Paradigm, application area, syntax, type behavior, evaluation, memory, concurrency, module systems, interoperability, and lifecycle are scoped claims. A language can belong to multiple semantic or application categories. Each factual value must identify the edition, environment, and material qualifications appropriate to that claim.

## Owned identities

- **Language.** A governed language with a distinct definition, origin, or recognized compatibility boundary. Lexical similarity, a shared compiler, and access on the same platform are weak signals for identity.
- **Family.** A bounded group with source-backed lineage or shared design history. A family record does not transfer properties to its members.
- **Dialect.** A separately identifiable variant with a controlling source or repeatable boundary. Record the base language and the evidence distinguishing the variant. A transient extension or vendor option may be recorded as a scoped claim.
- **Edition.** An identifiable normative or documented revision of a language or dialect under the same authority. Record its parent identity and retain version-specific semantics. An edition is not a distinct language solely because it changes behavior.
- **Implementation.** A bounded supporting identity when needed to distinguish a particular compiler or interpreter from the language it implements. Reference external runtime and tooling identities explicitly when their owning index exists. Avoid general toolchain enumeration.

## Identity decisions

Mint one opaque ID per accepted entity. Retain aliases and historical names with individual claim bindings. A rename or a corrected classification retains the assigned ID and path. Alias collisions are allowed between distinct entities, and exact resolution returns all matching identities.

Retain predecessor records and add directed lineage claims for supersession, splits, and merges. A retired identity remains resolvable. Record a new identity for each successor whose definition changes materially and preserve the predecessors' authority, name, and scope through Git and SCES history. A fork or derivation may leave the predecessor active. Provide targeted independent review for consequential identity, lineage, normative semantics, compatibility, and cross-index decisions.

Keep ambiguous, incomplete, or disputed matches in the discovery ledger with concrete reasons. The registry's operational classifications do not supplant the governance of the underlying languages.
