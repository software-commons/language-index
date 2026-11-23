from hashlib import md5, sha256
import json
from pathlib import Path
import shutil
import subprocess
import zipfile

here = Path(__file__).resolve().parent
package = here / "native" / "cpython-3130-embed.bytes"
archive_data = package.read_bytes()
expected_md5 = "9d2a0301c2bba8df05c8815c954a2fc0"
expected_sha256 = "01c32d0737432240adcf0bbc1d32327f0976d3a1e1427774bc8febc8f1c03111"
assert sha256(archive_data).hexdigest() == expected_sha256
assert md5(archive_data).hexdigest() == expected_md5
destination = here / "native" / "cpython-3130-embed"
destination.mkdir(exist_ok=True)
with zipfile.ZipFile(package) as z:
    for member in z.infolist():
        name = member.filename
        assert Path(name).name == name and "/" not in name and "\\" not in name and ":" not in name
        if not member.is_dir():
            with z.open(member) as source, (destination / name).open("wb") as out:
                shutil.copyfileobj(source, out)

exe = destination / "python.exe"
result = subprocess.run([str(exe), "-I", "-B", str(here / "probe.py")], cwd=here, capture_output=True, check=True)
document = {
    "publisher_release": "https://www.python.org/downloads/release/python-3130/",
    "package": "https://www.python.org/ftp/python/3.13.0/python-3.13.0-embed-amd64.zip",
    "publisher_md5": expected_md5, "acquired_package_sha256": sha256(archive_data).hexdigest(),
    "python_executable_sha256": sha256(exe.read_bytes()).hexdigest(),
    "probe_source_sha256": sha256((here / "probe.py").read_bytes()).hexdigest(),
    **json.loads(result.stdout),
}
output = (json.dumps(document, sort_keys=True, indent=2) + "\n").encode()
(here / "implementation-probe.json").write_bytes(output)
print("implementation-probe.json", sha256(output).hexdigest())
print(result.stdout.decode())
