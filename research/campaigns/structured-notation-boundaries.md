# Structured notation and format boundaries

The primary and independent investigations verified six exact Linguist classifier rows and ten pinned specimens. Publisher specifications supplied the language rules and format boundaries. The specimens established origin and use. [Classifier locators](../../sces/artifacts/structured-notation-origin-crosswalk/classifier-leads.json) · [Independent decisions](../../sces/artifacts/structured-notation-origin-crosswalk/decisions.md) · [Fixture captures](../../sces/artifacts/structured-notation-origin-crosswalk/fixture-captures.json)

## Language identities

| Identity | Selected technical scope |
| --- | --- |
| GraphQL | October 2021 query root, fragment type overlap, conditional field collection, and variable definitions across referenced fragments. |
| Protocol Buffers schema language | Proto2 declaration rules for syntax defaults, field cardinality, explicit defaults, and nested messages. Wire encodings, generated code, and other syntax editions have separate applicability. |
| TOML | v1.0.0 declaration rules for dotted keys, inline tables, and arrays of tables. The native rules constrain table redefinition and identify the table affected by subsequent declarations. |

The independently verified TOML identity relies on project intent and the separate evidence for its declaration model. The same policy applies to other configuration notations with a documented native rule set. [GraphQL October 2021](https://spec.graphql.org/October2021/) · [Proto2 guide](https://protobuf.dev/programming-guides/proto2/) · [TOML v1.0.0](https://toml.io/en/v1.0.0)

## Format leads

The three resolved exclusions apply to the exact base-format leads. Related notations retain separate evidence requirements.

| Lead | Evidence boundary |
| --- | --- |
| CSV | RFC 4180 documents a delimited record representation. RFC 7111 supplies client-side selectors over an existing CSV resource. The pinned classifier sample uses LF line endings, outside the CRLF convention in the RFC. |
| JSON | RFC 8259 specifies serialization of a value. JSON Pointer, JSON Schema, and a host application's vocabulary supply distinct selection or constraint rules. |
| JSON5 | The 1.0.0 specification defines alternate syntax for writing and parsing interchange values. The sample includes host-package keys whose semantics come from the host. |

The narrower second revisions retain the original claims and supporting histories. The revision review corrected the RFC 7111 locator and kept changing GameMaker and JSON Schema captures as discovery context. A subsequent acquisition matched the exact JSON5 source bytes and all cited slices. The format claims support the discovery decisions and stay outside the selected language profiles. [Independent assessment](../../sces/artifacts/structured-notation-origin-crosswalk/independent-assessment.json) · [Original assessment](../../sces/artifacts/structured-notation-initial-review.json) · [Research receipts](../../sces/artifacts/structured-notation-r2-proof-research.jsonl) · [Independent review receipts](../../sces/artifacts/structured-notation-r2-proof-review.jsonl)
