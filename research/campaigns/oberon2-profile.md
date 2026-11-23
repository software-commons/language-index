# Oberon-2 report profile

The original designer report lead denotes the Oberon-2 dialect. The separate GitHub Linguist `Oberon` classifier remains unresolved because its sample inventory includes both Oberon and Oberon-2 material. The registry keeps the historical Oberon language and the Oberon-2 report dialect distinct. [Oberon-2 report](https://ssw.jku.at/Research/Papers/Oberon2.pdf) · [Mössenböck’s second-edition book](https://ssw.jku.at/Research/Books/Oberon2.pdf) · [Classifier investigation](linguist-source-crosswalk.md#ada-and-oberon-follow-up)

The seven reviewed claims cover the dialect identity, its parent language, and five boundaries in the report.

| Profile dimension | Reviewed scope |
| --- | --- |
| Type-bound procedures | Receiver type forms and scope of procedure binding |
| Procedure dispatch | Dynamic receiver dispatch and explicit base procedure selection |
| Module visibility | Report rules for read-only exports |
| Allocation | Pointer allocation of open arrays in the report |
| Type refinement | `WITH` statement guards and their local type effects |

The publication selection uses exact report and book revisions. The review separately compared an ETH report capture whose PDF wrapper changed. That capture supplies historical context. The records leave later dialect editions and actual compiler behavior outside the selected scope. [Lead decision](../../sces/artifacts/oberon2-profile-locator-review.json) · [Research receipts](../../sces/artifacts/oberon2-profile-proof-research.jsonl) · [Independent review receipts](../../sces/artifacts/oberon2-profile-proof-review.jsonl)
