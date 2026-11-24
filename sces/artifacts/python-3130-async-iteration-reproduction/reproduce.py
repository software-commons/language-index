from hashlib import md5, sha256
from io import BytesIO
import json
from pathlib import Path
import re
import shutil
import stat
import subprocess
from tempfile import TemporaryDirectory
import zipfile

here = Path(__file__).resolve().parent
package = here / "native" / "cpython-3130-embed.bytes"
expected_size = 12_499_601
expected_md5 = "9d2a0301c2bba8df05c8815c954a2fc0"
expected_sha256 = "01c32d0737432240adcf0bbc1d32327f0976d3a1e1427774bc8febc8f1c03111"
expected_probe_sha256 = "edb0f1b4c403334e756a5e5124bc8886558258cb69d49b7458893f341429a819"
with package.open("rb") as source:
    archive_data = source.read(expected_size + 1)
if len(archive_data) != expected_size or sha256(archive_data).hexdigest() != expected_sha256:
    raise SystemExit("CPython package does not match the qualified size and SHA-256")
if md5(archive_data, usedforsecurity=False).hexdigest() != expected_md5:
    raise SystemExit("CPython package does not match the recorded publisher MD5")
probe_data = (here / "probe.py").read_bytes()
if sha256(probe_data).hexdigest() != expected_probe_sha256:
    raise SystemExit("Probe source does not match the qualified SHA-256")

with zipfile.ZipFile(BytesIO(archive_data)) as archive:
    members = archive.infolist()
    names = set()
    for member in members:
        name = member.orig_filename
        stem = name.partition(".")[0].upper()
        if (name != member.filename or not re.fullmatch(r"[A-Za-z0-9_][A-Za-z0-9_.-]*", name)
                or name.endswith(".") or re.fullmatch(r"CON|PRN|AUX|NUL|(?:COM|LPT)[0-9]", stem)
                or member.is_dir() or member.external_attr & 0x10
                or stat.S_IFMT(member.external_attr >> 16) not in (0, stat.S_IFREG)
                or name.casefold() in names):
            raise SystemExit("CPython archive contains an unsafe or duplicate member")
        names.add(name.casefold())
    if not any(member.filename == "python.exe" for member in members):
        raise SystemExit("CPython archive does not contain python.exe")

    with TemporaryDirectory(prefix="cpython-3130-embed-", dir=here) as temp:
        scratch = Path(temp)
        destination = scratch / "runtime"
        destination.mkdir()
        for member in members:
            with archive.open(member) as source, (destination / member.filename).open("xb") as out:
                shutil.copyfileobj(source, out)

        probe = scratch / "probe.py"
        probe.write_bytes(probe_data)
        exe = destination / "python.exe"
        result = subprocess.run([str(exe), "-I", "-B", str(probe)], cwd=destination, capture_output=True, check=True)
        document = {
            "publisher_release": "https://www.python.org/downloads/release/python-3130/",
            "package": "https://www.python.org/ftp/python/3.13.0/python-3.13.0-embed-amd64.zip",
            "publisher_md5": expected_md5, "acquired_package_sha256": expected_sha256,
            "python_executable_sha256": sha256(exe.read_bytes()).hexdigest(),
            "probe_source_sha256": expected_probe_sha256,
            **json.loads(result.stdout),
        }
        output = (json.dumps(document, sort_keys=True, indent=2) + "\n").encode()
        result_file = scratch / "implementation-probe.json"
        result_file.write_bytes(output)
        result_file.replace(here / result_file.name)
print("implementation-probe.json", sha256(output).hexdigest())
print(result.stdout.decode())
