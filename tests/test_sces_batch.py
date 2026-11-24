"""Keep adverse research assessments when assembling a reviewed batch."""

import json
from hashlib import sha256
from pathlib import Path
import sys
import unittest


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "research/tools"))
from assemble_sces_batch import assemble, encode, key, make_ref
from export_codex_receipts import ReceiptError


class AssessmentCoverage(unittest.TestCase):
    def setUp(self):
        self.claim = dict(make_ref("claim", "fixture"), limitations=["Synthetic scope."])
        source_ref = make_ref("source", "fixture")
        source = dict(source_ref, locator="https://example.invalid/evidence", captured_sha256="0" * 64)
        edge_ref = make_ref("dependency", "fixture")
        edge = dict(edge_ref, claim=make_ref("claim", "fixture"), basis=source_ref, relation="support")
        assessment = dict(dependency=edge_ref, outcome="insufficient", checks={"applicability": "fail"},
                          reasoning="The source does not establish this claim.")
        self.assessment = dict(claim=edge["claim"], claim_sha256=sha256(encode(self.claim)).hexdigest(),
                               assessment=assessment)
        self.batch = dict(claims=[self.claim], sources=[source], dependencies=[edge],
                          research_assessments=[self.assessment])

        receipt = dict(source=source_ref, locator=source["locator"], sha256=source["captured_sha256"])
        research = dict(execution="research", completed="2026-01-01T00:01:00Z")
        review = dict(execution="review", started="2026-01-01T00:02:00Z", completed="2026-01-01T00:03:00Z")
        self.research = (research, ("sces/artifacts/research.jsonl", b"research\n"), {key(source_ref): [receipt]})
        self.review = (review, ("sces/artifacts/review.jsonl", b"review\n"), {key(source_ref): [receipt]})

    def test_reject_omitted_independent_assessment_even_for_held_claim(self):
        for held in (set(), {self.claim["id"]}):
            with self.subTest(held=held), self.assertRaisesRegex(ReceiptError, "missing frozen claims"):
                assemble(self.batch, {"independent_assessments": []}, self.research, self.review, "test", held)

    def test_rejected_claim_retains_both_phases(self):
        adverse = dict(self.assessment, conclusion="rejected", limitations=["Synthetic scope."],
                       challenge={"reasoning": "Attempted to disprove support."})
        planned = assemble(self.batch, {"independent_assessments": [adverse]},
                           self.research, self.review, "test", set())
        verification = [json.loads(blob) for path, blob in planned.items()
                        if path.startswith("sces/records/verification/")]
        records = {record["phase"]: record for record in verification}
        self.assertEqual({phase: record["conclusion"] for phase, record in records.items()},
                         {"research": "inconclusive", "independent-review": "rejected"})
        self.assertEqual(records["research"]["assessments"], [self.assessment["assessment"]])
        self.assertFalse(any(path.startswith("sces/records/disposition/") for path in planned))
