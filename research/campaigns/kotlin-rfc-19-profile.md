# Kotlin 1.9 RFC profile

Eight additional claims concern the exact publisher release `v1.9-rfc+0.1` at Git revision `7bb3bfc2dcc9217c54d979a96c7580a164c54cec`. They cover safe property navigation, Boolean `when` conditions, the result of `try` with `finally`, call argument evaluation order, the `for` operator convention, extension receivers, data-class copies, and type alias scope. The separately enrolled, later specification tree remains within its own recorded scope. [Research receipts](../../sces/artifacts/kotlin-scope-proof-research.jsonl) · [Independent review receipts](../../sces/artifacts/kotlin-scope-proof-review.jsonl) · [Source witnesses](../../sces/artifacts/kotlin-rfc-source-witnesses.json)

The RFC’s declaration-site variance prose disagrees with its examples and type-system chapter. The selected `for` claim concerns the operator convention, whose illustrative expansion has inconsistent iterator identifiers. The variance mapping and the inconsistent pseudocode spelling remain outside the selected claims.

The existing Kotlin language and Kotlin/JVM Regex links retain their scopes. Gradle 9.2.1 identifies Kotlin as the source language of its hosted scripts. The full Gradle classifier remains unresolved because it also describes the Gradle-specific scripts and APIs. [Discovery review](../../sces/artifacts/kotlin-rfc-origin-review.json)
