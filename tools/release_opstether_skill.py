#!/usr/bin/env python3
"""Build and synchronize a versioned OpsTether skill release.

Canonical files live under skills/opstether-linux-ops/.
This script never installs software, runs remote skill content, accesses credentials,
or sends anything to Agensi. It only validates and packages text-only files.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "skills" / "opstether-linux-ops"
PLUGIN = ROOT / "claude-plugin" / "opstether" / "skills" / "opstether-linux-ops"
PROJECT = ROOT / ".claude" / "skills" / "opstether-linux-ops"
MANIFEST = ROOT / "claude-plugin" / "opstether" / ".claude-plugin" / "plugin.json"
VERSION = re.compile(r"^\d+\.\d+\.\d+$")
SKILL_VERSION = re.compile(r"(?m)^(version:[ \t]*)(\d+\.\d+\.\d+)[ \t]*$")
SECRET = re.compile(rb"(?i)(-----BEGIN (?:RSA|EC|OPENSSH|DSA) PRIVATE KEY-----|sk-proj-[A-Za-z0-9_-]{15,}|KC_BOOTSTRAP_ADMIN_PASSWORD\s*=)")
MAX_TEXT_BYTES = 256_000
ZIP_DATE = (2020, 1, 1, 0, 0, 0)


def version_tuple(value: str) -> tuple[int, int, int]:
    if not VERSION.fullmatch(value):
        raise ValueError("Invalid semantic version: major.minor.patch required")
    return tuple(map(int, value.split(".")))


def read_files(path: Path) -> dict[str, bytes]:
    if not path.is_dir():
        raise ValueError(f"Missing skill directory: {path}")
    files: dict[str, bytes] = {}
    for file in sorted(path.rglob("*")):
        if file.is_symlink():
            raise ValueError(f"Symlink not allowed: {file}")
        if not file.is_file():
            continue
        rel = file.relative_to(path).as_posix()
        if file.suffix not in {".md", ".json"} or file.stat().st_size > MAX_TEXT_BYTES:
            raise ValueError(f"Unexpected extension/size: {rel}")
        raw = file.read_bytes()
        if b"\x00" in raw or SECRET.search(raw) or raw.startswith(b"#!"):
            raise ValueError(f"Possible binary, executable or secret: {rel}")
        raw.decode("utf-8")
        if file.suffix == ".json":
            json.loads(raw)
        files[rel] = raw
    if "SKILL.md" not in files:
        raise ValueError("SKILL.md is required at the skill root")
    if len(files) < 5 or len(files) > 30:
        raise ValueError("Unexpected number of files")
    skill = files["SKILL.md"].decode()
    if not skill.startswith("---\n") or "\n---\n" not in skill[4:]:
        raise ValueError("SKILL.md frontmatter invalid")
    if not re.search(r"(?m)^name:\s*opstether-linux-ops\s*$", skill):
        raise ValueError("Do not rename the installed skill")
    if "https://opstether.m2g.pro/mcp" not in skill:
        raise ValueError("Hosted MCP endpoint missing")
    return files


def file_version(data: bytes) -> str:
    match = SKILL_VERSION.search(data.decode())
    if not match:
        raise ValueError("Expected version field in SKILL.md")
    return match.group(2)


def with_version(data: bytes, version: str) -> bytes:
    text = data.decode()
    if len(SKILL_VERSION.findall(text)) != 1:
        raise ValueError("Expected exactly one frontmatter version")
    return SKILL_VERSION.sub(lambda m: m.group(1) + version, text).encode()


def change_without_version(left: dict[str, bytes], right: dict[str, bytes]) -> bool:
    if set(left) != set(right):
        return True
    for name in left:
        a, b = left[name], right[name]
        if name == "SKILL.md":
            a, b = with_version(a, "0.0.0"), with_version(b, "0.0.0")
        if a != b:
            return True
    return False


def mirror(source: dict[str, bytes], destination: Path) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    for file in sorted(destination.rglob("*"), reverse=True):
        if file.is_symlink():
            raise ValueError(f"Unexpected symlink in mirror: {file}")
        if file.is_file() and file.relative_to(destination).as_posix() not in source:
            file.unlink()
    for name, raw in source.items():
        path = destination / name
        path.parent.mkdir(parents=True, exist_ok=True)
        if not path.exists() or path.read_bytes() != raw:
            path.write_bytes(raw)
    for folder in sorted(destination.rglob("*"), reverse=True):
        if folder.is_dir() and not any(folder.iterdir()):
            folder.rmdir()


def pack(source: dict[str, bytes], path: Path, prefix: str) -> dict:
    path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name, raw in sorted(source.items()):
            item = zipfile.ZipInfo(prefix + name, ZIP_DATE)
            item.compress_type = zipfile.ZIP_DEFLATED
            item.external_attr = (0o100644 << 16)
            archive.writestr(item, raw)
    with zipfile.ZipFile(path) as archive:
        assert set(archive.namelist()) == {prefix + f for f in source}
        assert all(not n.startswith("/") and ".." not in n for n in archive.namelist())
        assert archive.testzip() is None
    return {"filename": path.name, "bytes": path.stat().st_size, "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def main() -> int:
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--release", action="store_true", help="Bump version if canonical content changed and sync plugin copies")
    cli.add_argument("--check", action="store_true", help="Verify all mirrors and version consistency without changing files")
    cli.add_argument("--output", type=Path, help="Write versioned ZIPs and manifest to this folder")
    args = cli.parse_args()
    if args.check and args.release:
        cli.error("Choose --release or --check")

    source = read_files(SOURCE)
    manifest = json.loads(MANIFEST.read_text())
    if manifest.get("name") != "opstether":
        raise ValueError("Existing plugin identity must not change")
    previous = manifest.get("version", "")
    current = file_version(source["SKILL.md"])
    version_tuple(previous)
    version_tuple(current)

    packaged = read_files(PLUGIN)
    content_changed = change_without_version(source, packaged)
    if args.release:
        if version_tuple(current) < version_tuple(previous):
            raise ValueError("Refuse version downgrade")
        if content_changed and current == previous:
            major, minor, patch = version_tuple(previous)
            current = f"{major}.{minor}.{patch + 1}"
        source["SKILL.md"] = with_version(source["SKILL.md"], current)
        if (SOURCE / "SKILL.md").read_bytes() != source["SKILL.md"]:
            (SOURCE / "SKILL.md").write_bytes(source["SKILL.md"])
        if manifest["version"] != current:
            manifest["version"] = current
            MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
        mirror(source, PLUGIN)
        mirror(source, PROJECT)

    if not args.release and version_tuple(current) != version_tuple(previous):
        raise ValueError("Canonical skill version differs from plugin manifest")

    for name, dest in (("plugin", PLUGIN), ("Claude project", PROJECT)):
        other = read_files(dest)
        if other != source:
            raise ValueError(f"{name} copy does not match canonical skill; run --release")
    if file_version(source["SKILL.md"]) != manifest["version"]:
        raise ValueError("Version mismatch after synchronization")

    info = {"name": "opstether-linux-ops", "version": current, "count": len(source), "changed": content_changed, "release": args.release}
    if args.output:
        out = args.output.resolve()
        out.mkdir(parents=True, exist_ok=True)
        artifacts = [
            pack(source, out / f"opstether-linux-ops-{current}.zip", ""),
            pack(source, out / f"opstether-linux-ops-agensi-{current}.zip", "opstether-linux-ops/"),
            pack(source, out / "opstether-linux-ops-latest.zip", ""),
            pack(source, out / "opstether-linux-ops-agensi-latest.zip", "opstether-linux-ops/"),
        ]
        info["artifacts"] = artifacts
        (out / "release-manifest.json").write_text(json.dumps(info, indent=2) + "\n")
    print(json.dumps(info, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError, KeyError, AssertionError) as error:
        sys.stderr.write(f"RELEASE_VALIDATION_FAILED: {error}\n")
        sys.exit(1)
