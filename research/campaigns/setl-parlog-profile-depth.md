# ISETL, SETL, and PARLOG profile depth

Two Codex executions independently reacquired the three exact registered authorities. Eleven claims are supported within their documented scope. The wording on SETL read-write parameters remains open. [Research receipts](../../sces/artifacts/setl-parlog-depth-proof-research.jsonl) · [Independent review receipts](../../sces/artifacts/setl-parlog-depth-proof-review.jsonl)

| Authority | Supported profile dimensions |
| --- | --- |
| Levin’s ISETL 3.0 manual | Lexical retention for `func`, restoration of local iterator bindings, existential and universal tests over iterator instances, and order and empty-input behavior of unseeded reduction. |
| Dewar’s 1979 SETL reference | Set-valued brace map lookup, bounded integer tuple progression, and filtered set construction. |
| Clark and Gregory’s 1984 account of PARLOG | Committed clause choice after successful matching and guard evaluation, parallel and sequential conjunction, suspension at an insufficiently instantiated input match, and status values in the proposed two-argument metacall. |

The SETL reference contains inconsistent examples for brace lookup and filter expansion. The independent review compared those examples with the formal brace rule and the separate explanation of iteration tests. The held `rw` statement included trailing variadic formals. The source describes their tuple aggregation and leaves the proposed general writeback interpretation unresolved. A separately reviewed revision may establish the narrower fixed-formal, explicit-return case. [SETL `rw` claim](../../sces/records/claim/dewar-1979-setl-read-write-parameter-return--1.json) · [Inconclusive review](../../sces/records/verification/setl-parlog-depth-proof-independent-review-dewar-1979-setl-read-write-parameter-return-r1--1.json)

The claims establish documented edition scope. Runtime behavior, portability across implementations, and additional profile dimensions require separate evidence.
