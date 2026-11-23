"""Test shared index invariants without real language evidence."""

from copy import deepcopy
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from index import Index, RegistryError, encode


FIRST = "10000000000000000000000000000000"
SECOND = "20000000000000000000000000000000"


def ref(kind, identifier, revision=1):
    return {"kind": kind, "id": identifier, "revision": revision}


def entity(identifier, kind, name, claim=None, **changes):
    return {
        "id": identifier, "kind": kind, "name": name, "state": "active", "aliases": [],
        "identity_claim": claim or ref("claim", f"identity-{identifier}"),
        "relations": [], **changes,
    }


def write(root, path, value):
    target = root / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(encode(value))
    return target


def entity_path(identifier):
    return f"registry/entities/{identifier[:2]}/{identifier}.json"


def snapshots(root):
    return {path.relative_to(root).as_posix(): path.read_bytes()
            for path in (root / "registry").rglob("*.json")}


class RegistryArchitecture(unittest.TestCase):
    def setUp(self):
        temp = TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)

    def test_incremental_identity_alias_rename_and_reverse_relationship(self):
        first = entity(FIRST, "language", "Fixture Alpha")
        second = entity(SECOND, "language", "Fixture Beta")
        first_path = entity_path(FIRST)
        second_path = entity_path(SECOND)
        write(self.root, first_path, first)
        original = snapshots(self.root)
        write(self.root, second_path, second)
        created = snapshots(self.root)
        self.assertEqual(set(created) - set(original), {second_path})
        self.assertEqual(created[first_path], original[first_path])
        updated = deepcopy(first)
        updated["name"] = "Fixture Renamed"
        updated["aliases"] = [{"name": "Fixture Alpha", "claim": ref("claim", "former-name")}]
        updated["relations"] = [{"type": "derived-from", "target": {"id": SECOND},
                                 "claim": ref("claim", "synthetic-lineage")}]
        write(self.root, first_path, updated)
        after = snapshots(self.root)
        self.assertEqual(set(after), {first_path, second_path})
        self.assertEqual(after[second_path], created[second_path])
        registry = Index(self.root)
        self.assertEqual([item["id"] for item in registry.lookup("fixture alpha", exact=True)], [FIRST])
        self.assertEqual(registry.entities[SECOND]["relations"], [])
        self.assertEqual(
            [row["id"] for row in registry.entities.values()
             for edge in row["relations"] if edge["target"] == {"id": SECOND}], [FIRST]
        )
        self.assertEqual(after, snapshots(self.root), "loading and lookup must be read-only")

    def test_candidate_add_is_isolated_and_cutoff_does_not_mutate_records(self):
        registry = Index(self.root)
        candidate = registry.add("Fixture discovery", "https://example.invalid/catalog/2026#fixture")
        before = snapshots(self.root)
        self.assertEqual(len(before), 1)
        second = Index(self.root).add("Another fixture", "https://example.invalid/catalog/2026#another")
        after_add = snapshots(self.root)
        self.assertNotEqual(candidate["id"], second["id"])
        self.assertEqual({path: after_add[path] for path in before}, before)
        self.assertEqual(len(after_add), 2)
        change = "registry/coverage/current.json"
        coverage = {"snapshot": "first-cutoff", "campaign": "fixture", "cutoff": "2026-11-22",
                    "scope": "Fixture catalog", "method": "Synthetic traversal", "limitations": ["Test only"]}
        write(self.root, "registry/coverage/snapshots/first-cutoff.json", coverage)
        write(self.root, change, coverage)
        before_cutoff = snapshots(self.root)
        updated = dict(coverage, snapshot="second-cutoff", cutoff="2026-11-23")
        write(self.root, "registry/coverage/snapshots/second-cutoff.json", updated)
        write(self.root, change, updated)
        after_cutoff = snapshots(self.root)
        self.assertEqual([key for key in before_cutoff if before_cutoff[key] != after_cutoff[key]], [change])
        self.assertEqual(Index(self.root).discovery["cutoff"], updated["cutoff"])

    def test_bulk_discovery_preserves_original_candidate_identity(self):
        lead = {"name": "Fixture discovery", "origin": "https://example.invalid/catalog/2026#row"}
        first = Index(self.root).import_candidates([lead])[0]
        before = snapshots(self.root)
        second = Index(self.root).import_candidates([lead, lead])
        self.assertEqual([row["id"] for row in second], [first["id"]])
        self.assertEqual(snapshots(self.root), before)
        with self.assertRaisesRegex(RegistryError, "different name"):
            Index(self.root).import_candidates([dict(lead, name="Conflicting fixture label")])
        self.assertEqual(snapshots(self.root), before)

    def test_candidate_adjudication_preserves_original_source(self):
        subprocess.run(["git", "init", "-q", str(self.root)], check=True)
        original = Index(self.root).add("Incorrectly transcribed label", "https://example.invalid/report#page=27")
        path = f"registry/candidates/{original['id'][:2]}/{original['id']}.json"
        subprocess.run(["git", "-C", str(self.root), "add", "registry"], check=True)
        subprocess.run(["git", "-C", str(self.root), "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
                        "-c", "commit.gpgsign=false", "commit", "-qm", "Add original candidate"], check=True)
        base = subprocess.check_output(["git", "-C", str(self.root), "rev-parse", "HEAD"], text=True).strip()

        corrected = dict(original, name="Corrected label", reason="Checked printed page and project locator.",
                         origins=[*original["origins"], "https://example.invalid/project#identity"])
        write(self.root, path, corrected)
        Index(self.root).check_history(base)

        write(self.root, path, dict(corrected, origins=corrected["origins"][1:]))
        with self.assertRaisesRegex(RegistryError, "Discovery origins must remain"):
            Index(self.root).check_history(base)

    def test_missing_sces_qualification_blocks_accepted_identity(self):
        write(self.root, entity_path(FIRST), entity(FIRST, "language", "Fixture Alpha"))
        with self.assertRaises(RegistryError):
            Index(self.root).qualified()

    def test_unpinned_cross_index_reference_is_rejected(self):
        target = {"id": SECOND, "index": "software-commons/runtime-index", "revision": "main"}
        relation = {"type": "external", "target": target, "claim": ref("claim", "invalid-link")}
        write(self.root, entity_path(FIRST), entity(FIRST, "language", "Fixture Alpha", relations=[relation]))
        with self.assertRaises(RegistryError):
            Index(self.root)

    def test_missing_local_relation_target_is_rejected(self):
        relation = {"type": "derived-from", "target": {"id": SECOND}, "claim": ref("claim", "invalid-link")}
        write(self.root, entity_path(FIRST), entity(FIRST, "language", "Fixture Alpha", relations=[relation]))
        with self.assertRaises(RegistryError):
            Index(self.root)

    def test_circular_local_lineage_is_rejected(self):
        for identifier, target in ((FIRST, SECOND), (SECOND, FIRST)):
            relation = {"type": "derived-from", "target": {"id": target},
                        "claim": ref("claim", "invalid-cycle")}
            write(self.root, entity_path(identifier),
                  entity(identifier, "language", f"Fixture {identifier}", relations=[relation]))
        with self.assertRaisesRegex(RegistryError, "Circular"):
            Index(self.root)

    def test_dialect_cannot_declare_an_implementation_as_parent(self):
        relation = {"type": "dialect-of", "target": {"id": SECOND}, "claim": ref("claim", "bad-parent")}
        write(self.root, entity_path(FIRST), entity(FIRST, "dialect", "Fixture dialect", relations=[relation]))
        write(self.root, entity_path(SECOND), entity(SECOND, "implementation", "Fixture implementation"))
        with self.assertRaisesRegex(RegistryError, "Incompatible"):
            Index(self.root)

    def test_wrong_shard_and_duplicate_path_cannot_supply_identity(self):
        row = entity(FIRST, "language", "Fixture Alpha")
        write(self.root, entity_path(FIRST), row)
        write(self.root, f"registry/entities/ff/{FIRST}.json", row)
        with self.assertRaises(RegistryError):
            Index(self.root)

    def test_unbound_structural_assertions_cannot_pass_as_factual_fields(self):
        row = entity(FIRST, "language", "Fixture Alpha", paradigms=["Synthetic"])
        write(self.root, entity_path(FIRST), row)
        with self.assertRaises(RegistryError):
            Index(self.root)

    def test_duplicate_json_keys_are_rejected(self):
        path = write(self.root, entity_path(FIRST), entity(FIRST, "language", "Fixture Alpha"))
        path.write_bytes(path.read_bytes().replace(b'"name":"Fixture Alpha"',
                                                 b'"name":"Fixture Beta","name":"Fixture Alpha"'))
        with self.assertRaises(RegistryError):
            Index(self.root)

    def test_historical_identity_cannot_be_removed_or_reallocated(self):
        def git(*args):
            return subprocess.check_output(["git", "-C", str(self.root), *args], text=True).strip()

        git("init", "-q")
        git("config", "user.name", "Software Commons synthetic fixtures")
        git("config", "user.email", "fixture@example.invalid")
        git("config", "core.autocrlf", "false")
        prior = write(self.root, entity_path(FIRST), entity(FIRST, "language", "Fixture Alpha"))
        git("add", "--", "registry")
        git("commit", "-qm", "Freeze prior fixture")
        revision = git("rev-parse", "HEAD")
        prior.unlink()
        write(self.root, entity_path(SECOND), entity(SECOND, "language", "Fixture Alpha"))
        with self.assertRaisesRegex(RegistryError, "permanent paths"):
            Index(self.root).check_history(revision)

    def test_unqualified_cli_build_creates_no_artifact(self):
        target = self.root / "build" / "rejected.json"
        process = subprocess.run([sys.executable, "-B", str(ROOT / "tools/index.py"), "--root",
                                  str(self.root), "build", "--output", str(target)], capture_output=True)
        self.assertNotEqual(process.returncode, 0)
        self.assertFalse(target.exists())
