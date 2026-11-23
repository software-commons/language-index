"""Exercise the candidate architecture and the exact SCES validator together."""

from dataclasses import dataclass
from importlib.util import module_from_spec, spec_from_file_location
import json
import os
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory
import unittest

from test_architecture import FIRST, SECOND, Index, RegistryError, encode, entity, entity_path, ref, snapshots, write


COMMIT = "ab26f278422772f2d9e5d4dd016407d14372a710"
BUNDLE = "14da3f31f697ab828d4a4560f060dbe511861020db54bea7bc531e20ea0855ce"


@dataclass(frozen=True)
class Domain:
    name: str
    kind: str
    dimension: str
    predicate: str
    category: str
    role: str

    @property
    def repository(self):
        return f"software-commons/{self.name}-index"


DOMAINS = (
    Domain("language", "language", "edition", "syntax", "documented", "official-documentation"),
    Domain("runtime", "runtime", "runtime-version", "feature", "observed", "observation"),
    Domain("platform", "platform", "platform-release", "abi", "implemented", "implementation"),
    Domain("specification", "specification", "edition", "wire-profile", "normative", "governing"),
)


class SyntheticIndex:
    """Self-contained fake sources and evidence for validator tests only."""

    def __init__(self, root, domain, sces):
        self.root, self.domain, self.sces = root, domain, sces
        self.git("init", "-q")
        self.git("config", "user.name", "Software Commons synthetic fixtures")
        self.git("config", "user.email", "fixture@example.invalid")
        self.git("config", "core.autocrlf", "false")
        self.scope = {domain.dimension: "1.2.0"}
        self.now = sces.instant("2041-01-05T00:00:00Z")
        predicates = {
            "identity-boundary": ("documented", True),
            "cross-index-relationship": ("documented", True),
            domain.predicate: (domain.category, domain.category == "normative"),
        }
        write(root, "sces/adoption.json", {
            "policy": "SCES-1.0", "policy_sha256": BUNDLE, "repository": domain.repository,
            "mode": "synthetic", "predicates": {
                predicate: {"scope_dimensions": ([domain.dimension, "owning-revision", "target-revision"]
                                                 if predicate == "cross-index-relationship" else [domain.dimension]),
                            "categories": [category],
                            "targeted_review": targeted}
                for predicate, (category, targeted) in predicates.items()
            },
        })
        self.revalidation = {"due": "2042-01-01T00:00:00Z", "triggers": ["Fixture revision changes"]}
        external = "language" if domain.name == "specification" else "specification"
        self.target = {"index": f"software-commons/{external}-index", "id": SECOND, "revision": "1.2.0"}

    def git(self, *args):
        result = subprocess.run(["git", "-C", str(self.root), *args], capture_output=True, check=True)
        return result.stdout.decode().strip()

    def artifact(self, name, blob):
        relative = f"sces/artifacts/{name}"
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(blob)
        return {"path": relative, "sha256": self.sces.digest(blob)}

    def record(self, value):
        name = f"{value['id']}--{value['revision']}.json"
        relative = f"sces/records/{value['kind']}/{name}"
        return write(self.root, relative, value)

    def source(self, identifier, revision=1, role="official-documentation"):
        body = f"Synthetic fixture statement only for {identifier} revision {revision}.\n".encode()
        source = {
            **ref("source", identifier, revision), "title": f"Synthetic {identifier}",
            "publisher": "Fixture only", "release": f"1.2.{revision}", "published": "2041-01-01",
            "locator": f"https://example.invalid/{self.domain.name}/{identifier}/{revision}",
            "role": role, "origin": identifier, "scope": self.scope, "access": "public",
            "reuse": "Synthetic fixture only", "upstream": [], "revalidation": self.revalidation,
            "artifact": self.artifact(f"{identifier}-{revision}.txt", body),
        }
        self.record(source)
        return source, body

    def claim(self, identifier, value, predicate, source_data, *, revision=1, category="documented"):
        source, body = source_data
        modality = "required" if category == "normative" else "descriptive"
        claim_ref = ref("claim", identifier, revision)
        scope = dict(self.scope)
        if predicate == "cross-index-relationship":
            scope.update({"owning-revision": "1.2.0", "target-revision": self.target["revision"]})
        claim = {**claim_ref, "subject": "e-" + FIRST, "predicate": predicate,
                 "statement": f"Synthetic {identifier} revision {revision} fixture assertion.",
                 "value": value, "category": category, "modality": modality, "polarity": "affirmative",
                 "scope": scope, "conditions": [],
                 "limitations": ["This artificial assertion describes a test fixture only."],
                 "risks": [], "corroboration_required": False, "revalidation": self.revalidation}
        review_key = f"{identifier}-r{revision}"
        if category == "observed":
            claim["method"] = self.artifact(f"{review_key}-method.txt", b"Fixture method and inputs.")
        claim_file = self.record(claim)
        dependency = ref("dependency", f"{review_key}-binding")
        source_ref = ref("source", source["id"], source["revision"])
        self.record({**dependency, "claim": claim_ref, "basis": source_ref, "relation": "support",
                     "citation": {"locator": "Entire synthetic projection", "start": 0, "end": len(body),
                                  "sha256": self.sces.digest(body), "modality": modality}})
        refs = {}
        for phase, day in (("research", 2), ("independent-review", 3)):
            name = f"synthetic-{review_key}-{phase}"
            prefix = f"2041-01-0{day}"
            receipt = {"capture": f"{name}-receipt", "source": source_ref, "locator": source["locator"],
                       "retrieved_at": f"{prefix}T00:15:00Z", "sha256": self.sces.digest(body)}
            trace = self.artifact(f"{name}.jsonl",
                                  encode(dict(receipt, event="direct-inspection", execution=name)))
            refs[phase] = ref("verification", name)
            assessment = dict.fromkeys(
                ("authenticity", "integrity", "relevance", "interpretation", "applicability", "contradiction"),
                "pass",
            )
            review = {**refs[phase], "phase": phase, "claim": claim_ref,
                      "claim_sha256": self.sces.digest(claim_file.read_bytes()), "conclusion": "supported",
                      "run": {"execution": name, "agent": "codex", "harness": "synthetic-harness",
                              "model": "synthetic", "started": f"{prefix}T00:00:00Z",
                              "completed": f"{prefix}T00:30:00Z", "trace": trace},
                      "acquisitions": [dict(receipt, dependency=dependency)],
                      "assessments": [{"dependency": dependency, "outcome": "supports", "checks": assessment,
                                       "reasoning": "Predeclared synthetic fixture rule."}],
                      "reasoning": "Synthetic fixture only.", "limitations": ["No real run or source."]}
            if phase == "independent-review":
                review["challenge"] = {"method": "Fixture scope test", "results": "Synthetic match.",
                                       "targeted": True}
                if category == "observed":
                    review["reproduction"] = {
                        "result": "reproduced", "reason": "Synthetic result only",
                        "artifact": self.artifact(f"{review_key}-result.txt", b"Fixture result."),
                    }
            self.record(review)
        self.record({**ref("disposition", f"{review_key}-eligible"), "target": claim_ref,
                     "evidence": "supported", "verification": "independently-reviewed", "finding": "none",
                     "recorded": "2041-01-04T00:00:00Z", "reason": "Synthetic fixture status.",
                     "research": refs["research"], "review": refs["independent-review"]})
        return claim_ref

    def registry(self, name, revision, prior=()):
        canonical = {"kind": self.domain.kind, "name": name, "state": "active"}
        base = self.claim("identity", encode(canonical).decode().strip(), "identity-boundary",
                          self.source("identity-text", revision), revision=revision)
        retained = list(prior)
        if not prior:
            edge_value = "external:" + encode(self.target).decode().strip()
            edge = self.claim("relationship", edge_value, "cross-index-relationship",
                              self.source("relationship-text"))
            alias = self.claim("alternate-name", "Fixture alias", "identity-boundary", self.source("alias-text"))
            feature = self.claim("applicable-feature", "fixture-present", self.domain.predicate,
                                 self.source("feature-text", role=self.domain.role), category=self.domain.category)
            retained = [edge, alias, feature]
        row = entity(FIRST, self.domain.kind, name, claim=base,
                     aliases=[{"name": "Fixture alias", "claim": retained[1]}],
                     relations=[{"type": "external", "target": self.target, "claim": retained[0]}])
        write(self.root, entity_path(FIRST), row)
        return [base, *retained]

    def qualify(self, version, claims, previous=None):
        self.git("add", "--", "sces/records", "sces/artifacts", "sces/adoption.json", "registry")
        self.git("commit", "-qm", f"Freeze synthetic inputs for release {version}")
        name = f"fixture-v{version}"
        selection = {"release": name, "dataset": "fixture", "dataset_version": f"{version}.0",
                     "schema_version": "1.0", "source_commit": self.git("rev-parse", "HEAD"),
                     "scope": "Synthetic fixture only", "research_cutoff": "2041-01-01T00:00:00Z",
                     "evaluated_at": "2041-01-04T03:00:00Z", "claims": claims,
                     "limitations": ["No material beyond this test."], "exclusions": []}
        if previous:
            previous_report = previous / "qualification.json"
            selection["previous_report"] = {"path": previous_report.relative_to(self.root).as_posix(),
                                            "sha256": self.sces.digest(previous_report.read_bytes())}
        write(self.root, "sces/publication.json", selection)
        register = self.sces.Registry(self.root, BUNDLE, self.now, synthetic=True)
        status = register.validate_publication(write=True)
        self.assert_qualified(status, name)
        recheck = self.sces.Registry(self.root, BUNDLE, self.now, synthetic=True)
        self.assert_qualified(recheck.validate_publication(), name)
        result = self.root / f"sces/releases/{name}"
        self.git("add", "--", "sces/publication.json", "sces/releases")
        self.git("commit", "-qm", f"Retain synthetic qualification {version}")
        return result

    @staticmethod
    def assert_qualified(status, name):
        if not status.startswith(f"qualified {name} "):
            raise AssertionError(status)


class ExactPolicyIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        policy_root = os.environ.get("SCES_POLICY_ROOT")
        if not policy_root:
            if os.environ.get("GITHUB_ACTIONS") == "true":
                raise AssertionError("CI must check out and supply the exact SCES policy")
            raise unittest.SkipTest("Set SCES_POLICY_ROOT to the pinned checkout to exercise qualification")
        cls.policy = Path(policy_root).resolve()
        head = subprocess.check_output(["git", "-C", str(cls.policy), "rev-parse", "HEAD"], text=True).strip()
        if head != COMMIT:
            raise AssertionError(f"Unexpected SCES policy revision {head}")
        spec = spec_from_file_location("pinned_sces_validator", cls.policy / "tools/sces/validate.py")
        cls.sces = module_from_spec(spec)
        spec.loader.exec_module(cls.sces)
        if cls.sces.policy_bundle() != BUNDLE:
            raise AssertionError("Unexpected SCES bundle digest")

    def test_each_domain_qualifies_and_updates_through_immutable_records(self):
        for domain in DOMAINS:
            with self.subTest(domain=domain.name), TemporaryDirectory() as folder:
                root = Path(folder)
                fixture = SyntheticIndex(root, domain, self.sces)
                refs = fixture.registry(f"Fixture {domain.name}", 1)
                release1 = fixture.qualify(1, refs)
                saved_report = (release1 / "qualification.json").read_bytes()
                initial_payload = json.loads((release1 / "claims.json").read_bytes())
                initial_report = json.loads(saved_report)
                baseline = snapshots(root)
                index = Index(root, kinds={domain.kind})
                claims = index.bind_payload(initial_payload)
                self.assertEqual(len(claims), 4)
                self.assertTrue(initial_report["synthetic"])
                self.assertEqual(initial_report["repository"], domain.repository)
                identity_features = [item["claim"] for item in claims.values()
                                     if item["claim"]["predicate"] == domain.predicate]
                self.assertEqual(identity_features[0]["scope"], {domain.dimension: "1.2.0"})
                rebuilt = Index(root, kinds={domain.kind})
                reverse_order = rebuilt.bind_payload(reversed(initial_payload))
                first_export = index.export(initial_report, claims)
                self.assertEqual(first_export, rebuilt.export(initial_report, reverse_order))
                self.assertEqual(len(json.loads(first_export)["claims"]), 4)
                self.assertEqual(baseline, snapshots(root))
                with self.assertRaises(self.sces.Invalid):
                    self.sces.Registry(root, BUNDLE, fixture.now, synthetic=False)

                old_records = {path: path.read_bytes() for path in (root / "sces/records").rglob("*.json")}
                fixture.source("new-discovery-source")
                second = fixture.registry(f"Renamed fixture {domain.name}", 2, prior=refs[1:])
                release2 = fixture.qualify(2, second, previous=release1)
                self.assertEqual((release1 / "qualification.json").read_bytes(), saved_report)
                self.assertEqual({path: path.read_bytes() for path in old_records}, old_records)
                self.assertEqual(set(snapshots(root)), set(baseline))
                payload2 = json.loads((release2 / "claims.json").read_bytes())
                changed = Index(root, kinds={domain.kind})
                claims2 = changed.bind_payload(payload2)
                self.assertIn(("identity", 2), claims2)
                self.assertNotIn(("identity", 1), claims2)
                with self.assertRaises(RegistryError):
                    changed.bind_payload(initial_payload)
