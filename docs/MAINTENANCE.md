# Maintain and query Language Index

The offline CLI uses Python 3.10 or newer. Run commands from the repository root. Git is needed for historical diffs, history checks, and the qualified publication path.

```text
python -B tools/index.py list
python -B tools/index.py search <query>
python -B tools/index.py resolve <name-or-alias>
python -B tools/index.py show <id>
python -B tools/index.py relations <id>
python -B tools/index.py sources <id>
python -B tools/index.py candidates
python -B tools/index.py coverage
python -B tools/index.py add <discovered-name> --origin <discovery-locator>
python -B tools/index.py import-candidates <candidate-batch.json>
python -B tools/index.py validate
python -B tools/index.py diff <full-commit-a> <full-commit-b>
```

Command results are JSON. `resolve` yields zero or more exact, case-insensitive matches. `relations` derives inverse edges at read time. `sources` follows exact claim bindings and source lineage. `coverage` reports structural counts and the current discovery declaration. The discovery ledger reports candidate dispositions, including unresolved names. Counts describe tracked coverage only.

For bulk intake, supply a JSON array of objects containing exactly `name` and `origin`. Each origin identifies one precise row in a pinned discovery source. Repeating the same input reuses the assigned IDs. Distinct locators that spell a name identically remain independent leads until an adjudicator establishes the relationship.

For a repository with an active publication, add `--policy /path/to/pinned/.github` before the command. Install the pinned policy checkout's `tools/sces/requirements.txt`. The CLI verifies its Git revision and calls the pinned validation tool before reading any qualified projections.

## Storage

- `registry/entities/<first-two-id-characters>/<id>.json` stores one accepted identity per file. IDs are 32 lowercase hexadecimal characters generated independently of the entity's metadata. Kind and display name live inside the record. Changing either preserves the path.
- `registry/candidates/<first-two-id-characters>/<id>.json` preserves every discovered lead and its disposition. `add` writes only a provisional lead. Evidence-backed decisions use exact SCES claim links where applicable. Source discovery notes can retain unresolved statements and conflicting candidate classifications.
- `registry/coverage/current.json` selects an exact declaration with the same content at `registry/coverage/snapshots/<snapshot>.json`. Record a cutoff in calendar date form, campaign, scope, method, and material limitations. Append snapshots when the discovery boundary changes.
- `sces/records/<kind>/<id>--<revision>.json` retains immutable evidence and claim history under SCES-1.0. Store safe acquisition and verification artifacts at the policy-defined paths.

The [domain schema](../schemas/domain/registry-v1.schema.json) describes stored JSON. Runtime validation also checks path and ID agreement, links, lineage, coverage history, and claim consistency. Registries are scanned without hand-maintained enumerations.

## Convert a lead to a qualified record

1. Add a candidate and record its discovery source. Keep predecessor locators and aliases distinct until the scope and identity boundary are resolved.
2. Use the [pinned Codex research protocol](https://github.com/software-commons/.github/blob/ab26f278422772f2d9e5d4dd016407d14372a710/docs/protocols/CODEX_RESEARCH_PROTOCOL.md). Register exact source revisions and create claim bindings. Record the research and independent review with actual execution evidence.
3. Assign permanent entity IDs only for accepted identities. The canonical entity record contains an identity claim for subject `e-<id>` and predicate `identity-boundary`. Its value is a canonical JSON string containing `kind`, `name`, and `state`. Aliases draw on individual `identity-boundary` claims whose values equal the names. A predecessor crosswalk uses a canonical JSON string containing the predecessor origin, revision, and key.
4. Store each relationship once on its source entity. An edge's claim value is its type, a colon, and the canonical JSON target. Local edges use predicate `identity-boundary`. External edges use `cross-index-relationship` and a target of `{index, id, revision}` with an exact Git or dataset revision. The claim's target revision scope must equal the external reference. Relative links and moving aliases do not supply link identity. A dialect and edition each need one qualified parent edge.
5. Freeze the SCES evidence and entity files in the same exact source commit. Follow [publication control](PUBLICATION.md) to prepare an active selection and verify all evidence gates. Work in progress can stay in a candidate ledger and research notes pending acceptance.

Each published language needs a qualified identity plus at least one qualified design, history, semantics, implementation, or compatibility claim. This is an admission floor. Track the breadth and depth of researched facets as separate measures.

## Build a consumer export

```text
python -B tools/index.py --policy /path/to/pinned/.github validate
python -B tools/index.py --policy /path/to/pinned/.github build --output build/language-index.json
```

The build requires an active qualified SCES bundle. It validates exact entity bytes against the SCES source commit and checks each identity, alias, crosswalk, and relationship against the selected claim. It then generates sorted UTF-8 JSON with the report, registry records, and qualified claims. The digest is reported by the command. Build outputs are disposable and ignored by Git. The export becomes a release payload only through the approved claim-to-output mapping and release decision required by SCES. Validation reads the repository without writing its registry or artifacts.

Every evidence, identity, or coverage update belongs in a governed pull request. A new source, alias, relationship, or discovery cutoff affects only its owning records and directly affected evidence, review, or coverage files. Release artifacts change when the selected release changes.
