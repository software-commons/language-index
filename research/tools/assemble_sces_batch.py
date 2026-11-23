"""Assemble candidate SCES records from assessed claims and exported tool receipts."""

import argparse
from collections import defaultdict
from hashlib import sha256
import json
from pathlib import Path
import re
import sys

from export_codex_receipts import TRACE_PATH, require


def read(path):
    return json.loads(path.read_bytes())


def encode(value):
    return (json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"),
                       allow_nan=False) + "\n").encode()


def reference(row):
    return {field: row[field] for field in ("kind", "id", "revision")}


def key(row):
    return row["kind"], row["id"], row["revision"]


def make_ref(kind, name):
    return {"kind": kind, "id": name, "revision": 1}


def phase_input(run_file, trace_file):
    run = read(run_file)
    trace = trace_file.read_bytes()
    path = run["trace"]["path"]
    require(re.fullmatch(TRACE_PATH, path) and ".." not in Path(path).parts, "Unsafe SCES trace path")
    require(sha256(trace).hexdigest() == run["trace"]["sha256"], "Exported trace digest differs")
    receipts = defaultdict(list)
    seen = set()
    for line in trace.splitlines():
        row = json.loads(line)
        require(row["execution"] == run["execution"] and row["event"] == "direct-inspection" and
                run["started"] <= row["retrieved_at"] <= run["completed"] and row["capture"] not in seen,
                "Receipt is duplicated or outside its declared execution")
        seen.add(row["capture"])
        receipts[key(row["source"])].append(row)
    return run, (path, trace), receipts


def assessments_support_claim(assessments, edges):
    if not any(edges[key(assessment["dependency"])]["relation"] == "support" for assessment in assessments):
        return False

    for assessment in assessments:
        relation = edges[key(assessment["dependency"])]["relation"]
        outcome = assessment["outcome"]
        checks = assessment["checks"].values()
        if relation in {"support", "context"} and outcome == "supports" and all(check == "pass" for check in checks):
            continue
        if (relation == "context" and outcome in {"insufficient", "inapplicable"}
                and all(check in {"pass", "not-applicable"} for check in checks)):
            continue
        return False
    return True


def assemble(batch, review, primary, independent, label, held):
    research_run, research_trace, research_receipts = primary
    review_run, review_trace, review_receipts = independent
    require(research_run["execution"] != review_run["execution"] and
            research_run["completed"] <= review_run["started"] and research_trace[0] != review_trace[0] and
            research_trace[1] != review_trace[1], "Research and review must have distinct sequential executions")
    require(re.fullmatch(r"[a-z][a-z0-9]*(?:-[a-z0-9]+)*", label), "Use a lower-case batch identifier")
    planned = dict((research_trace, review_trace))

    def record(row):
        kind, identifier, revision = key(row)
        require(kind in {"claim", "source", "dependency", "verification", "disposition", "conflict"} and
                re.fullmatch(r"[a-z][a-z0-9]*(?:-[a-z0-9]+)*", identifier) and
                type(revision) is int and revision > 0, "Invalid record identity")
        path = f"sces/records/{kind}/{identifier}--{revision}.json"
        data = encode(row)
        require(planned.setdefault(path, data) == data, f"Inconsistent exact record {path}")

    claims = {key(row): row for row in batch["claims"]}
    sources = {key(row): row for row in batch["sources"]}
    edges = defaultdict(dict)
    for row in batch["dependencies"]:
        require(key(row["claim"]) in claims, "Dependency has no frozen claim")
        edges[key(row["claim"])][key(row)] = row
    for group in (batch["sources"], batch["claims"], batch["dependencies"]):
        for row in group:
            record(row)

    research = defaultdict(list)
    for row in batch["research_assessments"]:
        claim_id = key(row["claim"])
        require(claim_id in claims, "Research verdict has no frozen claim")
        require(row["claim_sha256"] == sha256(encode(claims[claim_id])).hexdigest(),
                "Research verdict binds different claim bytes")
        research[claim_id].append(row["assessment"])

    concluded = set()
    for row in review["independent_assessments"]:
        claim_id = key(row["claim"])
        require(claim_id in claims and claim_id not in concluded, "Review lacks one unique frozen claim")
        concluded.add(claim_id)
        claim = claims[claim_id]
        digest = sha256(encode(claim)).hexdigest()
        require(row["claim_sha256"] == digest, "Independent verdict binds different claim bytes")
        reviewed = row.get("assessments") or [row["assessment"]]
        conclusion = row["conclusion"]
        require(conclusion in {"supported", "rejected", "inconclusive"}, "Unknown independent-review verdict")
        claim_edges = edges[claim_id]
        refs = {}
        for role, run, receipts, assessments in (
            ("research", research_run, research_receipts, research[claim_id]),
            ("independent-review", review_run, review_receipts, reviewed),
        ):
            assessment_refs = [key(assessment["dependency"]) for assessment in assessments]
            require(assessment_refs and len(set(assessment_refs)) == len(assessment_refs) and
                    set(assessment_refs) == claim_edges.keys(), "Assessment coverage differs from frozen dependencies")
            acquisitions = []
            for assessment in assessments:
                edge = claim_edges[key(assessment["dependency"])]
                require(edge["basis"]["kind"] == "source", "Batch assembly accepts directly inspected source dependencies")
                source_id = key(edge["basis"])
                source = sources[source_id]
                matches = [entry for entry in receipts[source_id] if entry["locator"] == source["locator"] and
                           entry.get("sha256") == source.get("captured_sha256")]
                require(matches, f"Missing exact {role} receipt for {source['id']}")
                capture = matches[0]
                receipt = {name: capture[name] for name in ("source", "locator", "sha256", "capture", "retrieved_at")
                           if name in capture}
                acquisitions.append({**receipt, "dependency": reference(edge)})
            supported = assessments_support_claim(assessments, claim_edges)
            phase_conclusion = conclusion if role == "independent-review" else ("supported" if supported else "inconclusive")
            require(phase_conclusion != "supported" or supported, "Supported verdict contains a failed binding")
            identifier = f"{label}-{role}-{claim['id']}-r{claim['revision']}"
            refs[role] = make_ref("verification", identifier)
            verification = dict(refs[role], claim=reference(claim), claim_sha256=digest, phase=role, run=run,
                                acquisitions=acquisitions, assessments=assessments, conclusion=phase_conclusion,
                                reasoning="\n\n".join(item["reasoning"] for item in assessments),
                                limitations=claim["limitations"] if role == "research" else row["limitations"])
            if role == "independent-review":
                verification["challenge"] = row["challenge"]
                if "reproduction" in row:
                    verification["reproduction"] = row["reproduction"]
            else:
                require(phase_conclusion == "supported" or conclusion != "supported", "Review cannot override primary findings")
            record(verification)

        if conclusion in {"supported", "inconclusive"} and claim["id"] not in held:
            identifier = f"{label}-{claim['id']}-r{claim['revision']}"
            accepted = conclusion == "supported"
            decisive_bindings = all(item["outcome"] == "supports" for item in [*research[claim_id], *reviewed])
            if not accepted:
                reason = "Independent verification was inconclusive. See the exact assessment and challenge."
            elif decisive_bindings:
                reason = "The two executions recorded support for each exact scoped binding."
            else:
                reason = "The two executions supported the claim and assessed every exact scoped binding."
            record(dict(make_ref("disposition", identifier), target=reference(claim),
                        evidence="supported" if accepted else "insufficient", verification="independently-reviewed",
                        finding="none" if accepted else "unknown", recorded=review_run["completed"],
                        reason=reason,
                        research=refs["research"], review=refs["independent-review"]))
    require(held <= {row["id"] for row in claims.values()}, "A withheld claim was not present in the batch")
    return planned


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("batch", type=Path)
    parser.add_argument("review", type=Path)
    parser.add_argument("--label", required=True)
    parser.add_argument("--research-run", type=Path, required=True)
    parser.add_argument("--research-trace", type=Path, required=True)
    parser.add_argument("--review-run", type=Path, required=True)
    parser.add_argument("--review-trace", type=Path, required=True)
    parser.add_argument("--hold", action="append", default=[], help="retain review data without a disposition for this claim ID")
    parser.add_argument("--output", type=Path, required=True, help="new directory outside the registry")
    args = parser.parse_args()
    try:
        planned = assemble(read(args.batch), read(args.review), phase_input(args.research_run, args.research_trace),
                           phase_input(args.review_run, args.review_trace), args.label, set(args.hold))
        args.output.mkdir(parents=True, exist_ok=False)
        for name, blob in sorted(planned.items()):
            path = args.output / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(blob)
    except (OSError, ValueError, TypeError, KeyError) as error:
        print(f"SCES batch assembly: {error}", file=sys.stderr)
        return 1
    print(f"Assembled {len(planned)} candidate files. Validate the combined repository under its pinned SCES policy.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
