"""Extract provisional leads with line-level provenance from a pinned Linguist catalog."""

import argparse
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import re

import yaml


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("snapshot", type=Path)
    parser.add_argument("--revision", required=True)
    parser.add_argument("--sha256", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if not re.fullmatch(r"[0-9a-f]{40}", args.revision):
        parser.error("revision must be an exact Git commit")
    data = args.snapshot.read_bytes()
    actual = sha256(data).hexdigest()
    if actual != args.sha256:
        parser.error("snapshot digest differs from the discovery declaration")
    raw = data.decode("utf-8")
    catalog = yaml.safe_load(raw)
    tree = yaml.compose(raw, Loader=yaml.SafeLoader)
    rows = []
    categories = Counter()
    seen = set()
    for node, _ in tree.value:
        name = node.value
        if name in seen or name not in catalog:
            parser.error(f"duplicate or unexpected catalog key: {name}")
        seen.add(name)
        line = node.start_mark.line + 1
        origin = (f"https://github.com/github-linguist/linguist/blob/{args.revision}"
                  f"/lib/linguist/languages.yml#L{line}")
        rows.append({"name": name, "origin": origin})
        categories[catalog[name]["type"]] += 1
    args.output.write_text(json.dumps(rows, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
                           encoding="utf-8", newline="\n")
    print(json.dumps({"leads": len(rows), "source_categories": categories, "sha256": actual}, sort_keys=True))


if __name__ == "__main__":
    main()
