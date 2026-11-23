# Regex Conformance predecessor reconciliation

## Pinned evidence

STRling Regex Conformance's declared-cutoff census is pinned to commit `62084ca0ef9b05a28711dd28bf10885c6ed0cb5d`. It reports 1,025 language discovery roots, 664 broad-catalog leads, 6,677 candidate facts, 1,176 source scans, and 3,071 unresolved candidate facts at the 2026-08-19 cutoff. A discovery root is an ecosystem used to locate regex facilities. The conservative facility estimate is also 1,025 and measures a different population. [Census method and results](https://github.com/strling-lang/regex-conformance/blob/62084ca0ef9b05a28711dd28bf10885c6ed0cb5d/docs/campaigns/known-universe-census-2026-08-19.md) · [Frozen forecast](https://github.com/strling-lang/regex-conformance/blob/62084ca0ef9b05a28711dd28bf10885c6ed0cb5d/reports/scale/known-universe-census-forecast.json)

The forecast validated against its pinned JSON Schema. The canonical report SHA-256 was recomputed after removing its digest property, and both of the forecast's tracked input digests matched the checked Git blobs. [Forecast schema](https://github.com/strling-lang/regex-conformance/blob/62084ca0ef9b05a28711dd28bf10885c6ed0cb5d/schemas/json/known-universe-census-forecast.schema.json) · [Verification contract](https://github.com/strling-lang/regex-conformance/blob/62084ca0ef9b05a28711dd28bf10885c6ed0cb5d/tools/campaigns/verify_known_universe_census.py)

| Recorded or recomputed object | SHA-256 |
| --- | --- |
| Forecast raw Git blob bytes | `2c1134a4b2c7708aa2357af664bae7257167edcb339aa104d66e52e4f29ddc69` |
| Forecast canonical report digest | `bd41377d3f5ce5bed5f141dcc09b1050f2b7a85a523519fc6b6bf158de919a2f` |
| Tracked August 15 planning inventory | `0601c2c948b19c7f5265bd53260c7c8a47478d12d3dc79e863a2f2f8e411f9f8` |
| Tracked Evidence Pack v2 certification input | `f39c80c34e75cec6a2c002d18ab0221ab55ce090fd59e68525f8a1988a80d6ca` |
| Tracked scientific identity registry | `040c16f1d29840e97374f8b3e61023a2735a5846284e110753ff346fa1a95f0a` |

## Original ledger recovery

An exact-name search of the accessible STRling project tree, including the Regex Conformance checkout, retained external evidence, and scientific continuation checkout, returned no files matching the five original ledger names. A separate exact-name search in local Downloads and Codex Documents also returned no matches. The predecessor's November 21 recovery records independently record zero verified originals from those prior searches and zero matching member names among 15 local archive indexes. Its reported previous searches also included connected storage, mail attachments, earlier worktrees, and private scratch. This reconciliation inspected those outcome records and did not repeat those connected-account searches. Recovery can reopen if an authorized archive or directory containing the original files becomes accessible.

| External file named by the pinned verifier | Expected SHA-256 | Recovery result |
| --- | --- | --- |
| `language-screening.tsv` | `9e1edcbab15d8b83d2997ce6b57a6636464c1c56854cfa5b017eb29a8a5fcdbf` | Unavailable in the searched scope |
| `wikipedia-programming-languages-2026-08-17.tsv` | `50be1f27254c2d04d7edd315123f3f9db250a5c5cdfb81a92c1708a733c7d45d` | Unavailable in the searched scope |
| `candidate-ledger.tsv` | `6ff8caa140ea78e38bb37808b988b46ae64dfbcc263f7c7a9871b26e5f977669` | Unavailable in the searched scope |
| `source-scans.tsv` | `0682089f3e0c5ec9ade294a884d178125e9a73e1bd8a0024840f126d4acb738d` | Unavailable in the searched scope |
| `non-language-surface-audit-2026-08-19.tsv` | `9e9bd072ecb1fc2fec10f043bd3fe9b6ddc18ef0a8a34b6cbdd18ba581709478` | Unavailable in the searched scope |

The historical counts remain attributable to the forecast. Exact per-root membership, catalog aliases, and candidate-to-root joins cannot be derived from its aggregates. A new reconstruction needs its own cutoff, source set, and reconciliation record.

## Tracked fallback and identity implications

The August 15 planning inventory contains 77 facility rows and 16 auxiliary candidate rows. It yields 47 Language Index discovery leads after selecting explicit language labels, interpreter or engine names that require identity adjudication, named SQL surfaces, and related notations that warrant a scope decision. Each lead has one exact line locator at the pinned Git revision. The remaining rows principally describe regex libraries, host applications, or other product surfaces. No facility disposition or regex semantic assertion was imported as a Language Index property. [Tracked planning inventory](https://github.com/strling-lang/regex-conformance/blob/62084ca0ef9b05a28711dd28bf10885c6ed0cb5d/registries/universe/full-known-universe-2026-08-15.v1.json)

The distinction between a host language and an implementation is needed to reconcile Python and its runtimes, and ECMAScript and the listed engines. The facility-level association of Kotlin, Scala, and Clojure with Java Pattern concerns shared regex behavior. It does not establish a language identity merge. Likewise, a named SQL surface starts a dialect investigation and needs primary documentation about its scope and governance. [Fallback JVM entries](https://github.com/strling-lang/regex-conformance/blob/62084ca0ef9b05a28711dd28bf10885c6ed0cb5d/registries/universe/full-known-universe-2026-08-15.v1.json#L148-L150)

The predecessor's assigned scientific IDs identify its own semantic entities, while content-derived identifiers bind immutable revisions. Its pinned scientific registry contains 28,016 bindings and 3,162 lineage records. Language Index keeps those IDs under predecessor ownership and records a crosswalk only when the mapping itself is qualified. The inherited scientific inventory supplies neither the missing discovery ledger nor an alternate language denominator. [Identity registry](https://github.com/strling-lang/regex-conformance/tree/62084ca0ef9b05a28711dd28bf10885c6ed0cb5d/registries/identity) · [Identity and migration contract](https://github.com/strling-lang/regex-conformance/blob/62084ca0ef9b05a28711dd28bf10885c6ed0cb5d/docs/architecture/scientific-identities.md)

## Original-row inspection on 2026-11-23

The retained inventory was re-acquired at the recorded commit and matched SHA-256 `0601c2c948b19c7f5265bd53260c7c8a47478d12d3dc79e863a2f2f8e411f9f8`. Every one of the 47 ledger fragments resolved to its actual JSON record. Each existing candidate retains its opaque identity and original locator. Its reason now names the predecessor row and the exact downstream identity question that remains.

The source categories include 14 language-runtime rows, 10 database rows, five ECMAScript-runtime rows, eight other facility rows, and 10 auxiliary rows. These are categories from the predecessor inventory. For example, the C lead originates in the PCRE2 API row, the Java lead names the `java.util.regex.Pattern` facility, and several SQL leads originate in a product-specific regex surface. The original-row inspection leaves each of the 47 dispositions unresolved pending the applicable language, dialect, implementation, or notation evidence and review. Reopening recovery of the predecessor's missing external ledgers still requires a new accessible archive or directory.
