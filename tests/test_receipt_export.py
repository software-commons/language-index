"""Check continuation receipts remain attributable to their original tool call."""

import json
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
import unittest


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "research/tools"))
from export_codex_receipts import ReceiptError, export
from assemble_sces_batch import ASSESSMENT_CHECKS, assessments_support_claim, key


THREAD = "00000000-1111-2222-3333-444444444444"
TURN = "00000000-1111-2222-3333-555555555555"


class AssessmentRoles(unittest.TestCase):
    def setUp(self):
        self.support = {"kind": "dependency", "id": "direct-rules", "revision": 1}
        self.context = {"kind": "dependency", "id": "related-runtime", "revision": 1}
        self.edges = {key(self.support): {"relation": "support"}, key(self.context): {"relation": "context"}}
        self.passing_checks = dict.fromkeys(ASSESSMENT_CHECKS, "pass")
        self.direct = {"dependency": self.support, "outcome": "supports", "checks": self.passing_checks}

    def test_allow_inspected_context_with_limited_applicability(self):
        for outcome in ("insufficient", "inapplicable"):
            context = {"dependency": self.context, "outcome": outcome,
                       "checks": {**self.passing_checks, "applicability": "not-applicable"}}
            self.assertTrue(assessments_support_claim([self.direct, context], self.edges))

    def test_require_successful_direct_support(self):
        context = {"dependency": self.context, "outcome": "supports", "checks": self.passing_checks}
        self.assertFalse(assessments_support_claim([context], self.edges))
        self.assertFalse(assessments_support_claim([{**self.direct, "outcome": "insufficient"}, context], self.edges))

    def test_reject_support_with_missing_checks(self):
        for checks in ({}, {"authenticity": "pass"}):
            with self.subTest(checks=checks):
                self.assertFalse(assessments_support_claim([{**self.direct, "checks": checks}], self.edges))

    def test_block_failed_or_adverse_context(self):
        for outcome, integrity in (("opposes", "pass"), ("unverifiable", "fail"), ("insufficient", "fail")):
            context = {"dependency": self.context, "outcome": outcome,
                       "checks": {**self.passing_checks, "integrity": integrity}}
            self.assertFalse(assessments_support_claim([self.direct, context], self.edges))


class ContinuedAcquisitions(unittest.TestCase):
    def fixture(self, wait_cell):
        marker = {"source": {"kind": "source", "id": "fixture", "revision": 1},
                  "locator": "https://example.invalid/frozen", "sha256": "0" * 64}
        chunks = [
            ("session_meta", {"id": THREAD, "cli_version": "0.1.0"}),
            ("event_msg", {"type": "task_started", "turn_id": TURN}),
            ("turn_context", {"turn_id": TURN, "model": "fixture"}),
            ("response_item", {"type": "custom_tool_call", "call_id": "call_start", "name": "exec",
                               "status": "completed"}),
            ("response_item", {"type": "custom_tool_call_output", "call_id": "call_start",
                               "output": [{"type": "input_text", "text": "Script running with cell ID g1:2\n"}]}),
            ("response_item", {"type": "function_call", "call_id": "call_wait", "name": "wait",
                               "arguments": json.dumps({"cell_id": wait_cell})}),
            ("response_item", {"type": "function_call_output", "call_id": "call_wait",
                               "output": [{"type": "input_text", "text": "Script completed\n"},
                                          {"type": "input_text", "text": "SCES_ACQUISITION_V1 " + json.dumps(marker)}]}),
            ("event_msg", {"type": "task_complete", "turn_id": TURN}),
        ]
        folder = TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        path = Path(folder.name) / f"rollout-fixture-{THREAD}.jsonl"
        path.write_text("\n".join(json.dumps({"type": kind, "payload": payload,
                                              "timestamp": f"2026-11-22T10:00:{i:02}Z"})
                                  for i, (kind, payload) in enumerate(chunks)) + "\n", encoding="utf-8")
        return path

    def test_match_original_cell_and_completion(self):
        blob, run = export(self.fixture("g1:2"), TURN, "sces/artifacts/fixture.jsonl", ["call_wait"])
        self.assertEqual(json.loads(blob)["capture"], f"codex-rollout:{THREAD}:call_wait:1")
        self.assertEqual(run["completed"], "2026-11-22T10:00:07Z")

    def test_reject_unrelated_wait(self):
        with self.assertRaisesRegex(ReceiptError, "earlier functions.exec cell"):
            export(self.fixture("g1:3"), TURN, "sces/artifacts/fixture.jsonl", ["call_wait"])
