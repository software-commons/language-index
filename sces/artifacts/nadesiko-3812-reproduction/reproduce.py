from base64 import b64encode
from hashlib import sha256, sha512
import json
from pathlib import Path
import subprocess
import tarfile

root = Path(__file__).resolve().parent
native = root / "native"
archive = native / "nadesiko-3812-package-tarball.bytes"
npm = json.loads((native / "nadesiko-3812-package.bytes").read_bytes())
assert npm["name"] == "nadesiko3" and npm["version"] == "3.8.12"
assert npm["gitHead"] == "d24c8f150850221133f605c3da3d03f99ec1b2fb"
assert npm["dist"]["integrity"] == "sha512-" + b64encode(sha512(archive.read_bytes()).digest()).decode()
modules = native / "modules"
modules.mkdir(exist_ok=True)
names = ("nako_errors.mjs", "nako_indent.mjs", "nako_prepare.mjs")
module_hashes = {}
with tarfile.open(archive, "r:gz") as tf:
    for name in names:
        path = f"package/core/src/{name}"
        member = tf.getmember(path)
        assert member.isfile()
        body = tf.extractfile(member).read()
        (modules / name).write_bytes(body)
        module_hashes[path] = sha256(body).hexdigest()
    for source, name in (("indent", "nako_indent.mts"), ("prepare", "nako_prepare.mts")):
        assert tf.extractfile(f"package/core/src/{name}").read() == (
            native / f"nadesiko-3812-{source}-source.bytes").read_bytes()
execution = subprocess.run(["node", str(root / "probe.mjs")], check=True, capture_output=True)
result = {"release_commit": npm["gitHead"], "npm_package": npm["name"], "npm_version": npm["version"],
          "npm_archive_sha256": sha256(archive.read_bytes()).hexdigest(), "publisher_integrity": npm["dist"]["integrity"],
          "module_sha256": module_hashes, "probe_sha256": sha256((root / "probe.mjs").read_bytes()).hexdigest(),
          **json.loads(execution.stdout)}
payload = (json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True) + "\n").encode()
(root / "implementation-probe.json").write_bytes(payload)
print("implementation-probe.json", sha256(payload).hexdigest(), len(result["results"]), "asserted cases")
