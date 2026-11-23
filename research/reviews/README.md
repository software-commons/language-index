# Independent review and acquisition receipts

Follow the [pinned SCES research protocol](https://github.com/software-commons/.github/blob/ab26f278422772f2d9e5d4dd016407d14372a710/docs/protocols/CODEX_RESEARCH_PROTOCOL.md). This directory describes how to capture and inspect evidence. Put production verification records in `sces/records/verification/` and their permitted receipt excerpts in `sces/artifacts/`.

## Record the acquisition

Use separate completed Codex turns for primary research and independent review. Give the verifier the frozen claim, exact references, and scope. The verifier independently opens the controlling passages before considering the research rationale. Record counterevidence and targeted challenges when applicable.

During each turn, inspect each controlling source directly. In the same successful `functions.exec` call, emit one marker line per acquisition. Generate the source reference and locator from the acquisition inputs and the digest from the exact bytes acquired. Omit the digest only when the policy permits and the bytes cannot be obtained. Emit trusted acquisition metadata only. Keep fetched source text and raw tool output out of the marker-producing block.

```text
SCES_ACQUISITION_V1 {"source":{"kind":"source","id":"example-source","revision":1},"locator":"https://example.org/specification/edition-1","sha256":"<digest of the bytes actually acquired>"}
```

This line illustrates the format. A planned fetch, pasted URL, or manually copied digest is insufficient. Multiple real acquisitions can emit multiple lines in one call. The exporter accepts plain tool output and the structured result of a completed inner shell command with exit code zero. If the acquisition fails, record the limitation and omit the marker.

## Export selected receipts

After the turn completes, select its precise local `rollout-*.jsonl` file and turn UUID. Limit scope further with repeated `--call-id` options when the acquisition calls are known. Run the exporter once with each output mode:

```sh
python research/tools/export_codex_receipts.py --rollout "$ROLLOUT" --turn "$TURN_ID" --trace-path sces/artifacts/language-review.jsonl --emit run
python research/tools/export_codex_receipts.py --rollout "$ROLLOUT" --turn "$TURN_ID" --trace-path sces/artifacts/language-review.jsonl --emit trace
```

`run` emits the SCES run descriptor. `trace` emits the exact newline-delimited bytes its digest describes. When rerecording the trace to the named path, preserve UTF-8 and LF bytes, for example by passing a binary output stream to Python's `subprocess.run`. Review the fields before making the extract public. Copy a selected receipt into the appropriate verification record with its exact dependency reference. The verifier still supplies the actual assessment and conclusion.

The exporter checks turn boundaries, tool input and output pairing, and the allowlisted marker shape. It does not prove that a tool output faithfully represents the claimed acquisition or that the reviewer inspected and interpreted its content. Have an authorized operator compare the receipt to the actual tool invocation and source before approval. The `codex-rollout:` identifiers locate events in the authorized local harness archive. They do not provide public access to a chat. Keep full rollout logs, credentials, restricted source material, and private metadata out of commits. If the underlying event is unavailable for audit or the safe receipt cannot be exported, keep the claim provisional.
