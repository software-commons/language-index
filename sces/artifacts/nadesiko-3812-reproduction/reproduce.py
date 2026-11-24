from base64 import b64encode
from hashlib import sha256, sha512
from io import BytesIO
import json
import os
from pathlib import Path
import subprocess
import tarfile
from tempfile import TemporaryDirectory

INPUTS_SHA256 = "6a2a562b709c0adf301f861dd44f4d7dde2279bdb7c9b2c9987f1bbc03143550"
PROBE_SHA256 = "e0f9462cae1bd80d25723ed2a3bfacaef85c01dc9cc54b59ed06867cce8b1172"


def verified_bytes(path, expected_sha256):
    body = path.read_bytes()
    if sha256(body).hexdigest() != expected_sha256:
        raise ValueError(f"SHA-256 mismatch for enrolled input {path.name}")
    return body


def read_member(archive, path):
    member = archive.getmember(path)
    if not member.isfile():
        raise ValueError(f"Non-regular archive member {path}")
    with archive.extractfile(member) as body:
        return body.read()


root = Path(__file__).resolve().parent
manifest = json.loads(verified_bytes(root / "inputs.json", INPUTS_SHA256))
probe = verified_bytes(root / "probe.mjs", PROBE_SHA256)
inputs = {path: verified_bytes(root / path, row["sha256"]) for path, row in manifest.items()}
archive = inputs["native/nadesiko-3812-package-tarball.bytes"]
npm = json.loads(inputs["native/nadesiko-3812-package.bytes"])
if (npm["name"], npm["version"], npm["gitHead"]) != (
    "nadesiko3", "3.8.12", "d24c8f150850221133f605c3da3d03f99ec1b2fb"
):
    raise ValueError("Unexpected enrolled npm release identity")
if npm["dist"]["integrity"] != "sha512-" + b64encode(sha512(archive).digest()).decode("ascii"):
    raise ValueError("Enrolled archive differs from npm publisher integrity")

names = ("nako_errors.mjs", "nako_indent.mjs", "nako_prepare.mjs")
with tarfile.open(fileobj=BytesIO(archive), mode="r:gz") as tf:
    for source, name in (("indent", "nako_indent.mts"), ("prepare", "nako_prepare.mts")):
        if read_member(tf, f"package/core/src/{name}") != inputs[f"native/nadesiko-3812-{source}-source.bytes"]:
            raise ValueError(f"Archive member differs from enrolled upstream source {name}")
    module_bytes = {name: read_member(tf, f"package/core/src/{name}") for name in names}

with TemporaryDirectory(prefix="nadesiko-3812-") as directory:
    staged = Path(directory)
    modules = staged / "native" / "modules"
    modules.mkdir(parents=True)
    for name, body in module_bytes.items():
        (modules / name).write_bytes(body)
    (staged / "probe.mjs").write_bytes(probe)
    node_env = {key: value for key, value in os.environ.items() if key.upper() not in {"NODE_OPTIONS", "NODE_PATH"}}
    execution = subprocess.run(["node", str(staged / "probe.mjs")], cwd=staged, env=node_env,
                               check=True, capture_output=True)

module_hashes = {f"package/core/src/{name}": sha256(body).hexdigest() for name, body in module_bytes.items()}
result = {"release_commit": npm["gitHead"], "npm_package": npm["name"], "npm_version": npm["version"],
          "npm_archive_sha256": sha256(archive).hexdigest(), "publisher_integrity": npm["dist"]["integrity"],
          "module_sha256": module_hashes, "probe_sha256": sha256(probe).hexdigest(),
          **json.loads(execution.stdout)}
payload = (json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True) + "\n").encode()
(root / "implementation-probe.json").write_bytes(payload)
print("implementation-probe.json", sha256(payload).hexdigest(), len(result["results"]), "asserted cases")
