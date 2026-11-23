"""Maintain and query the Language Index without a database."""

import argparse
from collections import Counter, defaultdict
from datetime import date
from hashlib import sha1, sha256
import json
from pathlib import Path
import re
import subprocess
import sys
from uuid import uuid4


ID = re.compile(r"[0-9a-f]{32}")
KEY = re.compile(r"[a-z][a-z0-9]*(?:-[a-z0-9]+)*")
REVISION = re.compile(r"(?:[0-9a-f]{40}|v?[0-9]+\.[0-9]+(?:\.[0-9]+)?(?:-[a-z0-9.-]+)?)")
LANGUAGE_KINDS = {"language", "family", "dialect", "edition", "implementation"}
DISPOSITIONS = {"canonical", "dialect", "family", "alias", "implementation", "out-of-scope",
                "duplicate", "rejected", "unresolved"}
SCES_COMMIT = "ab26f278422772f2d9e5d4dd016407d14372a710"
REPOSITORY = "software-commons/language-index"
DATASET = "language-index"
DOMAIN_SCHEMA = "registry-v1"
RELATIONS = {"dialect-of", "edition-of", "member-of", "derived-from", "forked-from",
             "supersedes", "split-from", "merged-from", "implemented-by", "external"}
LINEAGE = {"dialect-of", "edition-of", "member-of", "derived-from", "forked-from",
           "supersedes", "split-from", "merged-from"}
LANGUAGE_TARGETS = {
    "dialect-of": ({"dialect"}, {"language", "dialect"}),
    "edition-of": ({"edition"}, {"language", "dialect"}),
    "member-of": ({"language", "dialect", "family"}, {"family"}),
    "implemented-by": ({"language", "dialect", "edition"}, {"implementation"}),
}
PROFILE_PREDICATES = {"normative-semantics", "language-design", "language-history",
                      "implementation-behavior", "compatibility"}


class RegistryError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise RegistryError(message)


def encode(value):
    return (json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"),
                       allow_nan=False) + "\n").encode()


def unique(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, f"Duplicate JSON key {key}")
        result[key] = value
    return result


def decode(data):
    return json.loads(data.decode("utf-8"), object_pairs_hook=unique,
                      parse_constant=lambda value: require(False, f"Non-JSON number {value}"))


def read(path):
    return decode(path.read_bytes())


def text(value):
    return type(value) is str and bool(value.strip())


def reference(value):
    return (type(value) is dict and set(value) == {"kind", "id", "revision"} and
            value["kind"] == "claim" and text(value["id"]) and KEY.fullmatch(value["id"]) and
            type(value["revision"]) is int and value["revision"] > 0)


def claim_key(ref):
    return ref["id"], ref["revision"]


def frozen_value(value):
    return encode(value).decode().removesuffix("\n")


def git_blobs(root, commit, path):
    output = git(root, "ls-tree", "-rz", commit, "--", path)
    result = {}
    for entry in output.decode().split("\0"):
        if entry:
            metadata, name = entry.split("\t", 1)
            mode, kind, oid = metadata.split(" ")
            require(kind == "blob" and mode in {"100644", "100755"}, f"Non-file Git record: {name}")
            result[name] = oid
    return result


def git_blob_id(data):
    return sha1(f"blob {len(data)}\0".encode() + data, usedforsecurity=False).hexdigest()


def git(root, *args):
    result = subprocess.run(["git", "-C", str(root), *args], capture_output=True)
    require(result.returncode == 0, f"Git could not read {' '.join(args)}")
    return result.stdout


class Index:
    def __init__(self, root, kinds=LANGUAGE_KINDS):
        self.root = root.resolve()
        require(self.root.is_dir(), f"Index root does not exist: {root}")
        self.kinds = kinds
        self.entity_blobs = {}
        self.entities = self.load("entities", self.check_entity)
        self.candidates = self.load("candidates", self.check_candidate)
        self.discovery = self.load_coverage()
        require(not self.entities.keys() & self.candidates.keys(), "Entity and candidate IDs must be distinct")
        self.incoming = defaultdict(list)
        self.check_links()
        self.origins = {}
        for row in self.candidates.values():
            if "entity" in row:
                require(row["entity"] in self.entities, f"Unknown candidate target in {row['id']}")
            for origin in row["origins"]:
                require(origin not in self.origins, f"Duplicate discovery locator: {origin}")
                self.origins[origin] = row
            for ref in row.get("evidence", []):
                path = self.root / "sces/records/claim" / f"{ref['id']}--{ref['revision']}.json"
                require(path.resolve() == path and path.is_file(),
                        f"Missing candidate evidence {claim_key(ref)} in {row['id']}")
                claim = read(path)
                require(all(claim.get(field) == value for field, value in ref.items()),
                        f"Misidentified candidate evidence {claim_key(ref)} in {row['id']}")

    def load_coverage(self):
        directory = self.root / "registry" / "coverage"
        require(directory.resolve() == directory, "Linked coverage directory")
        current = directory / "current.json"
        snapshots = directory / "snapshots"
        require(snapshots.resolve() == snapshots, "Linked coverage history")
        for path in sorted(snapshots.glob("*")):
            require(path.resolve() == path and path.is_file() and path.suffix == ".json",
                    f"Unexpected coverage artifact: {path}")
            row = read(path)
            self.check_coverage(row)
            require(path.stem == row["snapshot"], f"Misplaced coverage snapshot: {path}")
        if not current.exists():
            return None
        require(current.resolve() == current, "Linked coverage pointer")
        row = read(current)
        self.check_coverage(row)
        matching = snapshots / f"{row['snapshot']}.json"
        require(matching.is_file() and row == read(matching), "Coverage pointer must match its frozen snapshot")
        return row

    @staticmethod
    def check_coverage(row):
        required = {"snapshot", "campaign", "cutoff", "scope", "method", "limitations"}
        require(type(row) is dict and row.keys() == required and
                all(text(row[name]) for name in required - {"limitations"}) and
                KEY.fullmatch(row["snapshot"]) and re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", row["cutoff"])
                and type(row["limitations"]) is list and row["limitations"] and all(map(text, row["limitations"])),
                "Invalid coverage declaration")
        date.fromisoformat(row["cutoff"])

    def check_links(self):
        lineage = {}
        for row in self.entities.values():
            successors = []
            for relation in row["relations"]:
                target = relation["target"]
                if "index" not in target:
                    require(target["id"] != row["id"] and target["id"] in self.entities,
                            f"Missing or self-referential relationship in {row['id']}")
                    other = self.entities[target["id"]]
                    if self.kinds == LANGUAGE_KINDS and relation["type"] in LANGUAGE_TARGETS:
                        source_kinds, target_kinds = LANGUAGE_TARGETS[relation["type"]]
                        require(row["kind"] in source_kinds and other["kind"] in target_kinds,
                                f"Incompatible {relation['type']} relationship in {row['id']}")
                    if relation["type"] in {"supersedes", "merged-from", "split-from"}:
                        require(other["state"] == "retired", f"Lineage predecessor must be retained and retired: {other['id']}")
                    if relation["type"] in LINEAGE:
                        successors.append(target["id"])
                    self.incoming[target["id"]].append({"from": row["id"], **relation})
            lineage[row["id"]] = successors
        done = set()
        for start in lineage:
            if start in done:
                continue
            active = {start}
            stack = [(start, iter(lineage[start]))]
            while stack:
                current, remaining = stack[-1]
                target = next(remaining, None)
                if target is None:
                    done.add(current)
                    active.remove(current)
                    stack.pop()
                elif target not in done:
                    require(target not in active, f"Circular entity lineage involving {target}")
                    active.add(target)
                    stack.append((target, iter(lineage[target])))

    def load(self, section, validator):
        records = {}
        directory = self.root / "registry" / section
        require(directory.resolve() == directory, f"Registry section escapes its path: {directory}")
        for path in sorted(directory.rglob("*")):
            require(path.resolve() == path, f"Linked path in registry: {path}")
            if path.is_dir():
                continue
            require(path.suffix == ".json", f"Unexpected registry file {path}")
            data = path.read_bytes()
            row = decode(data)
            require(type(row) is dict and text(row.get("id")) and ID.fullmatch(row["id"]),
                    f"Invalid identity in {path}")
            validator(row)
            expected = directory / row["id"][:2] / f"{row['id']}.json"
            require(expected == path and row["id"] not in records, f"Misplaced or duplicate identity: {path}")
            records[row["id"]] = row
            if section == "entities":
                self.entity_blobs[path.relative_to(self.root).as_posix()] = git_blob_id(data)
        return records

    def check_entity(self, row):
        fields = {"id", "kind", "name", "aliases", "state", "identity_claim", "relations"}
        require(fields <= row.keys() <= fields | {"crosswalks"} and row["kind"] in self.kinds and text(row["name"]) and
                row["state"] in {"active", "retired"} and reference(row["identity_claim"]),
                f"Invalid entity {row['id']}")
        require(type(row["aliases"]) is list and type(row["relations"]) is list,
                f"Invalid aliases or relationships for {row['id']}")
        aliases = set()
        for alias in row["aliases"]:
            require(type(alias) is dict and set(alias) == {"name", "claim"} and text(alias["name"]) and
                    reference(alias["claim"]), f"Invalid alias in {row['id']}")
            name = alias["name"].casefold()
            require(name not in aliases and name != row["name"].casefold(), f"Duplicate alias in {row['id']}")
            aliases.add(name)
        edges = set()
        for relation in row["relations"]:
            require(type(relation) is dict and set(relation) == {"type", "target", "claim"} and
                    relation["type"] in RELATIONS and reference(relation["claim"]),
                    f"Invalid relationship in {row['id']}")
            target = relation["target"]
            require(type(target) is dict and text(target.get("id")), f"Invalid relationship target in {row['id']}")
            if set(target) == {"id"}:
                require(ID.fullmatch(target["id"]), f"Invalid local target in {row['id']}")
            else:
                require(set(target) == {"id", "index", "revision"} and
                        text(target["index"]) and re.fullmatch(r"software-commons/[a-z0-9-]+-index", target["index"]) and
                        text(target["revision"]) and REVISION.fullmatch(target["revision"]),
                        f"Unpinned external target in {row['id']}")
            edge = relation["type"], encode(target)
            require(edge not in edges, f"Duplicate relationship in {row['id']}")
            edges.add(edge)
        crosswalks = row.get("crosswalks", [])
        require(type(crosswalks) is list, f"Invalid crosswalks in {row['id']}")
        seen = set()
        for crosswalk in crosswalks:
            require(type(crosswalk) is dict and set(crosswalk) == {"origin", "revision", "key", "claim"} and
                    all(text(crosswalk[field]) for field in ("origin", "revision", "key")) and
                    crosswalk["revision"].casefold() not in {"main", "master", "latest", "head", "current"} and
                    reference(crosswalk["claim"]), f"Invalid predecessor crosswalk in {row['id']}")
            locator = crosswalk["origin"], crosswalk["revision"], crosswalk["key"]
            require(locator not in seen, f"Duplicate predecessor crosswalk in {row['id']}")
            seen.add(locator)

    def check_candidate(self, row):
        required = {"id", "name", "origins", "disposition", "reason"}
        require(required <= row.keys() <= required | {"entity", "evidence"} and text(row["name"]) and
                text(row["reason"]) and row["disposition"] in DISPOSITIONS and
                type(row["origins"]) is list and row["origins"] and all(map(text, row["origins"])),
                f"Invalid candidate {row['id']}")
        if row["disposition"] in {"canonical", "dialect", "family", "alias", "implementation", "duplicate"}:
            require("entity" in row, f"Candidate disposition requires an entity: {row['id']}")
        if "entity" in row:
            require(text(row["entity"]) and ID.fullmatch(row["entity"]), f"Invalid candidate target: {row['id']}")
        evidence = row.get("evidence", [])
        require(type(evidence) is list and all(reference(ref) for ref in evidence),
                f"Invalid candidate evidence: {row['id']}")
        if row["disposition"] in {"out-of-scope", "rejected"}:
            require(evidence, f"Candidate disposition needs evidence: {row['id']}")

    def add(self, name, origin):
        return self.import_candidates([{"name": name, "origin": origin}])[0]

    def import_candidates(self, leads):
        require(type(leads) is list, "Candidate input must be a JSON array")
        known = self.origins.copy()
        rows = {}
        pending = []
        for lead in leads:
            require(type(lead) is dict and set(lead) == {"name", "origin"} and
                    all(map(text, lead.values())), "Each candidate input needs a name and exact discovery locator")
            name, origin = lead["name"], lead["origin"]
            if origin in known:
                row = known[origin]
                require(row["name"] == name, f"Discovery locator already records a different name: {origin}")
            else:
                identifier = uuid4().hex
                row = {"id": identifier, "name": name, "origins": [origin],
                       "disposition": "unresolved", "reason": "Awaiting identity investigation."}
                known[origin] = row
                pending.append(row)
            rows[row["id"]] = row
        for row in pending:
            identifier = row["id"]
            path = self.root / "registry" / "candidates" / identifier[:2] / f"{identifier}.json"
            require(path.resolve() == path, f"Linked candidate path: {path}")
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open("xb") as file:
                file.write(encode(row))
            self.candidates[identifier] = row
            self.origins[row["origins"][0]] = row
        return list(rows.values())

    def qualified(self, policy=None):
        selection_path = self.root / "sces" / "publication.json"
        if policy is not None:
            require(git(policy, "rev-parse", "HEAD").decode().strip() == SCES_COMMIT, "SCES checkout is not pinned")
            result = subprocess.run([sys.executable, "-B", str(policy / "tools" / "sces" / "validate.py"),
                                     "--repo", str(self.root), "--repository", REPOSITORY],
                                    capture_output=True, text=True)
            require(result.returncode == 0, f"SCES rejected the repository: {result.stderr.strip()}")
        if not selection_path.exists():
            require(not self.entities, "Accepted identities require an active SCES qualification")
            return None, {}
        require(policy is not None, "An active selection requires --policy pointing to the pinned SCES checkout")
        selection = read(selection_path)
        directory = self.root / "sces" / "releases" / selection["release"]
        report = read(directory / "qualification.json")
        payload = read(directory / "claims.json")
        require(report["repository"] == REPOSITORY and not report["synthetic"],
                "Synthetic or foreign release cannot qualify Language Index")
        require(report["dataset"] == DATASET and report["schema_version"] == DOMAIN_SCHEMA,
                "The publication does not name the Language Index dataset and domain schema")
        commit = report["source_commit"]
        declared = git_blobs(self.root, commit, "registry/entities")
        require(self.entity_blobs == declared, "Entity bytes differ from the exact SCES source commit")
        require(self.entities, "A release must identify its domain entities")
        claims = self.bind_payload(payload)
        profiled = {item["claim"]["subject"] for item in claims.values()
                    if item["claim"]["predicate"] in PROFILE_PREDICATES}
        for entity in self.entities.values():
            if entity["kind"] == "language":
                require("e-" + entity["id"] in profiled, f"Missing qualified profile facet: {entity['id']}")
        return report, claims

    def bind_payload(self, payload):
        """Check that projected registry fields agree with the supplied SCES payload."""
        claims = {}
        for row in payload:
            claim = row["claim"]
            identity = claim_key(claim)
            require(identity not in claims and claim["subject"].startswith("e-") and
                    claim["subject"][2:] in self.entities, f"Invalid or duplicate publication claim: {identity}")
            claims[identity] = row
        for entity in self.entities.values():
            if entity["kind"] in {"dialect", "edition"}:
                parent_role = f"{entity['kind']}-of"
                parent_count = sum(edge["type"] == parent_role and "index" not in edge["target"]
                                   for edge in entity["relations"])
                require(parent_count == 1, f"Exactly one local {parent_role} is required: {entity['id']}")
            identity_value = frozen_value({field: entity[field] for field in ("kind", "name", "state")})
            base = (entity["identity_claim"], "identity-boundary", identity_value)
            aliases = [(alias["claim"], "identity-boundary", alias["name"]) for alias in entity["aliases"]]
            relations = [(edge["claim"], "cross-index-relationship" if "index" in edge["target"] else
                          "identity-boundary", edge["type"] + ":" + frozen_value(edge["target"]))
                         for edge in entity["relations"]]
            crosswalks = [(item["claim"], "identity-boundary", frozen_value({
                field: item[field] for field in ("origin", "revision", "key")}))
                          for item in entity.get("crosswalks", [])]
            for ref, predicate, value in [base, *aliases, *relations, *crosswalks]:
                claim = claims.get(claim_key(ref), {}).get("claim", {})
                require(claim.get("subject") == "e-" + entity["id"] and
                        claim.get("predicate") == predicate and claim.get("value") == value,
                        f"Qualified claim does not bind the entity field {entity['id']}: {claim_key(ref)}")
            for edge in entity["relations"]:
                if "index" in edge["target"]:
                    claim = claims[claim_key(edge["claim"])]["claim"]
                    require(claim.get("scope", {}).get("target-revision") == edge["target"]["revision"],
                            f"Cross-index SCES scope differs from target revision: {entity['id']}")
        return claims

    def export(self, report, claims):
        return encode({"release": report, "entities": sorted(self.entities.values(), key=lambda row: row["id"]),
                       "claims": [claims[key] for key in sorted(claims)]})

    def check_history(self, base):
        require(re.fullmatch(r"[0-9a-f]{40}", base), "Use a full Git commit ID for the history base")
        old = git_blobs(self.root, base, "registry/entities")
        require(old.keys() <= self.entity_blobs.keys(), "Accepted identities must be retained at their permanent paths")
        past_candidates = git_blobs(self.root, base, "registry/candidates")
        candidates = {f"registry/candidates/{identifier[:2]}/{identifier}.json" for identifier in self.candidates}
        require(past_candidates.keys() <= candidates, "Discovered candidates must be retained in the ledger")
        for name, oid in git_blobs(self.root, base, "registry/coverage/snapshots").items():
            path = self.root / name
            require(path.is_file() and path.resolve() == path and git_blob_id(path.read_bytes()) == oid,
                    f"Prior coverage snapshots must remain immutable: {name}")

    def sources(self, identifier, claims):
        self.get(identifier)
        selected = [row for row in claims.values() if row["claim"]["subject"] == "e-" + identifier]
        pending = [edge["basis"] for row in selected for edge in row["dependencies"]]
        sources = {}
        seen = set()
        premise_dependencies = None
        while pending:
            ref = pending.pop()
            key = ref["kind"], ref["id"], ref["revision"]
            if key in seen:
                continue
            seen.add(key)
            if ref["kind"] == "claim":
                if premise_dependencies is None:
                    premise_dependencies = defaultdict(list)
                    for path in (self.root / "sces/records/dependency").glob("*.json"):
                        dependency = read(path)
                        premise_dependencies[claim_key(dependency["claim"])].append(dependency["basis"])
                pending.extend(premise_dependencies[claim_key(ref)])
            else:
                source = read(self.root / "sces/records/source" / f"{ref['id']}--{ref['revision']}.json")
                sources[key] = source
                pending.extend(source["upstream"])
        return {"claims": selected, "sources": [sources[key] for key in sorted(sources)]}

    def coverage(self, claims):
        facets = Counter(
            (value["claim"]["predicate"], value["claim"]["scope"].get("facet", "unspecified"))
            for value in claims.values() if value["claim"]["predicate"] in PROFILE_PREDICATES)
        return {"entities": dict(sorted(Counter(row["kind"] for row in self.entities.values()).items())),
                "aliases": sum(len(row["aliases"]) for row in self.entities.values()),
                "candidates": dict(sorted(Counter(row["disposition"] for row in self.candidates.values()).items())),
                "qualified_claims_by_predicate": dict(sorted(Counter(
                    value["claim"]["predicate"] for value in claims.values()).items())),
                "profile_depth": [{"predicate": predicate, "facet": facet, "claims": count}
                                  for (predicate, facet), count in sorted(facets.items())],
                "discovery": self.discovery}

    def lookup(self, query, exact=False):
        query = query.casefold()
        matches = []
        for entity in self.entities.values():
            values = [entity["id"], entity["name"].casefold(), *(a["name"].casefold() for a in entity["aliases"])]
            if (query in values if exact else any(query in value for value in values)):
                matches.append(entity)
        return sorted(matches, key=lambda row: row["id"])

    def get(self, identifier):
        require(identifier in self.entities, f"Unknown identity: {identifier}")
        return self.entities[identifier]


def revision_diff(root, left, right):
    require(all(re.fullmatch(r"[0-9a-f]{40}", rev) for rev in (left, right)), "Use two full Git commit IDs")
    paths = git(root, "diff", "--name-status", "--no-renames", "-z", left, right, "--", "registry", "sces")
    fields = paths.decode().rstrip("\0").split("\0") if paths else []
    return [{"change": status, "path": path} for status, path in zip(fields[::2], fields[1::2])]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--policy", type=Path)
    commands = parser.add_subparsers(dest="command", required=True)
    for name in ("list", "coverage", "candidates"):
        commands.add_parser(name)
    commands.add_parser("validate").add_argument("--base")
    for name in ("search", "resolve", "show", "relations", "sources"):
        commands.add_parser(name).add_argument("value")
    add = commands.add_parser("add")
    add.add_argument("name")
    add.add_argument("--origin", required=True)
    commands.add_parser("import-candidates").add_argument("file", type=Path)
    build = commands.add_parser("build")
    build.add_argument("--output", type=Path, required=True)
    diff = commands.add_parser("diff")
    diff.add_argument("left")
    diff.add_argument("right")
    args = parser.parse_args()
    try:
        index = Index(args.root)
        if args.command == "add":
            output = index.add(args.name, args.origin)
        elif args.command == "import-candidates":
            output = index.import_candidates(read(args.file))
        elif args.command == "diff":
            output = revision_diff(index.root, args.left, args.right)
        else:
            report, claims = index.qualified(args.policy)
            if args.command == "list":
                output = sorted(index.entities.values(), key=lambda row: row["id"])
            elif args.command == "candidates":
                output = sorted(index.candidates.values(), key=lambda row: row["id"])
            elif args.command in {"search", "resolve"}:
                output = index.lookup(args.value, exact=args.command == "resolve")
            elif args.command == "show":
                output = index.get(args.value)
            elif args.command == "relations":
                output = {"outgoing": index.get(args.value)["relations"],
                          "incoming": index.incoming[args.value]}
            elif args.command == "sources":
                output = index.sources(args.value, claims)
            elif args.command == "coverage":
                output = index.coverage(claims)
            elif args.command == "validate":
                if args.base:
                    index.check_history(args.base)
                output = {"valid": True, "publication": report["release"] if report else None}
            else:
                require(report, "A consumer export requires active SCES qualification")
                blob = index.export(report, claims)
                output_path = args.output.resolve()
                build = index.root / "build"
                require(build.resolve() == build and output_path != build and output_path.is_relative_to(build),
                        "Write consumer exports below the ignored build directory")
                output_path.parent.mkdir(parents=True, exist_ok=True)
                output_path.write_bytes(blob)
                output = {"output": str(output_path), "sha256": sha256(blob).hexdigest()}
        sys.stdout.buffer.write(encode(output))
        return 0
    except (OSError, ValueError, TypeError, KeyError) as error:
        print(f"Language Index: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
