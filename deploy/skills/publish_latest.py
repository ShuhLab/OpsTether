#!/usr/bin/env python3
"""Deploy latest vetted OpsTether skill ZIPs from public GitHub to the web.

Runs as the unprivileged opstether-skill-update system user.
Does NOT alter the hosted MCP backend, users' OAuth clients, or Agensi listings.
On any validation/fetch failure it preserves the prior downloadable ZIPs.
"""
import fcntl
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

BASE = Path("/opt/opstether/deploy/skill-autoupdate")
REPO = BASE / "repo"
PUBLIC = BASE / "public"
STATE = BASE / "state.json"
GIT = "https://github.com/ShuhLab/OpsTether.git"
VERSION = re.compile(r"^\d+\.\d+\.\d+$")


def call(args: list[str], cwd: Path | None = None, timeout: int = 90) -> None:
    environment = dict(os.environ)
    environment.update({"GIT_TERMINAL_PROMPT": "0", "GIT_CONFIG_NOSYSTEM": "1", "HOME": str(BASE)})
    completed = subprocess.run(args, cwd=cwd, env=environment, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=timeout)
    if completed.returncode:
        # Never print raw environment, response bodies or GitHub tokens.
        raise RuntimeError(f"Subprocess {args[0]} failed (exit {completed.returncode})")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def atomic_copy(src: Path, dest: Path) -> None:
    candidate = dest.with_name("." + dest.name + ".incoming")
    try:
        candidate.write_bytes(src.read_bytes())
        candidate.chmod(0o644)
        os.replace(candidate, dest)
    finally:
        candidate.unlink(missing_ok=True)


def main() -> None:
    BASE.mkdir(parents=True, exist_ok=True)
    with (BASE / ".lock").open("w") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        if not (REPO / ".git").exists():
            call(["git", "-c", "core.hooksPath=/dev/null", "clone", "--quiet", "--depth", "1", GIT, str(REPO)], timeout=110)
        else:
            call(["git", "-c", "core.hooksPath=/dev/null", "fetch", "--quiet", "--depth", "1", "origin", "main"], cwd=REPO)
            call(["git", "-c", "core.hooksPath=/dev/null", "reset", "--hard", "FETCH_HEAD"], cwd=REPO)

        # GitHub Actions already synchronized and versioned the source. Refuse
        # partial updates: never auto-bump a released version on the web host.
        with tempfile.TemporaryDirectory(prefix=".build-", dir=BASE) as temp:
            staging = Path(temp)
            call([sys.executable, str(REPO / "tools/release_opstether_skill.py"), "--check", "--output", str(staging)], cwd=REPO)
            manifest = json.loads((staging / "release-manifest.json").read_text())
            ver = manifest.get("version", "")
            if not VERSION.fullmatch(ver):
                raise RuntimeError("Unexpected version in manifest")
            prior = json.loads(STATE.read_text()) if STATE.exists() else {}
            if prior.get("version"):
                if tuple(map(int, ver.split("."))) < tuple(map(int, prior["version"].split("."))):
                    raise RuntimeError("Refusing downgrade")

            allowed = {
                f"opstether-linux-ops-{ver}.zip",
                f"opstether-linux-ops-agensi-{ver}.zip",
                "opstether-linux-ops-latest.zip",
                "opstether-linux-ops-agensi-latest.zip",
            }
            artifacts = manifest.get("artifacts", [])
            if {item.get("filename") for item in artifacts} != allowed:
                raise RuntimeError("Artifact allowlist mismatch")
            for item in artifacts:
                local = staging / item["filename"]
                if digest(local) != item["sha256"] or local.stat().st_size != item["bytes"]:
                    raise RuntimeError("Artifact digest mismatch")

            # Do not overwrite immutable archives if already published with a
            # different digest. All validation happens before stable links move.
            for item in artifacts:
                if item["filename"].endswith("-latest.zip"):
                    continue
                public = PUBLIC / item["filename"]
                if public.exists() and digest(public) != item["sha256"]:
                    raise RuntimeError("Immutable version archive conflict")

            for item in artifacts:
                if item["filename"].endswith("-latest.zip"):
                    continue
                public = PUBLIC / item["filename"]
                if not public.exists():
                    atomic_copy(staging / item["filename"], public)
            for item in artifacts:
                if item["filename"].endswith("-latest.zip"):
                    atomic_copy(staging / item["filename"], PUBLIC / item["filename"])

            state = {
                "name": "opstether-linux-ops",
                "version": ver,
                "sha256": {item["filename"]: item["sha256"] for item in artifacts},
                "github_source": "ShuhLab/OpsTether",
                "update_mode": "validated-atomic",
            }
            scratch = BASE / ".state.incoming"
            scratch.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n")
            os.replace(scratch, STATE)
            # This JSON has no credentials and contains only public release data.
            public_json = BASE / ".public-state.json"
            public_json.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n")
            atomic_copy(public_json, PUBLIC / "opstether-skill-latest.json")
            print(json.dumps({"ok": True, "version": ver, "updated": True, "files": len(artifacts)}))


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, RuntimeError, subprocess.TimeoutExpired) as err:
        print(json.dumps({"ok": False, "error": str(err)[:180]}))
        sys.exit(1)
