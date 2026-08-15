#!/usr/bin/env python3
"""Build deterministic Pressolve skill and Connector ZIPs."""

from __future__ import annotations

import hashlib
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "pressolve"
CONNECTOR_DIR = SKILL_DIR / "assets" / "pressolve-connector"
DIST_DIR = ROOT / "dist"
FIXED_TIME = (2020, 1, 1, 0, 0, 0)
REQUIRED_FILES = (
    "SKILL.md",
    "agents/openai.yaml",
    "scripts/analyze_report.py",
    "scripts/build_blueprint.py",
    "references/diagnostics-lab.md",
    "references/update-guard.md",
    "references/connector.md",
    "assets/pressolve-connector/pressolve-connector.php",
    "assets/pressolve-connector/readme.txt",
    "references/troubleshooting.md",
)


def validate() -> None:
    if not SKILL_DIR.is_dir():
        raise SystemExit("Missing installable skill directory: pressolve/")

    for relative_path in REQUIRED_FILES:
        if not (SKILL_DIR / relative_path).is_file():
            raise SystemExit(f"Missing required skill file: {relative_path}")

    skill_text = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    if not skill_text.startswith("---\nname: pressolve\n"):
        raise SystemExit("SKILL.md must begin with valid Pressolve frontmatter")

    for reference in (SKILL_DIR / "references").glob("*.md"):
        marker = f"references/{reference.name}"
        if marker not in skill_text:
            raise SystemExit(f"Unreferenced skill resource: {marker}")

    if "Version: 2.0.0" not in (CONNECTOR_DIR / "pressolve-connector.php").read_text(encoding="utf-8"):
        raise SystemExit("Connector plugin version does not match the Pressolve 2.0 release")


def write_archive(source_dir: Path, root_name: str, archive: Path) -> Path:
    with ZipFile(archive, "w", compression=ZIP_DEFLATED, compresslevel=9) as bundle:
        for source in sorted(path for path in source_dir.rglob("*") if path.is_file()):
            relative = source.relative_to(source_dir)
            info = ZipInfo(f"{root_name}/{relative.as_posix()}", FIXED_TIME)
            info.compress_type = ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            bundle.writestr(info, source.read_bytes(), compress_type=ZIP_DEFLATED, compresslevel=9)

    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    checksum = archive.with_suffix(archive.suffix + ".sha256")
    checksum.write_text(f"{digest}  {archive.name}\n", encoding="utf-8")
    return archive


def build() -> list[Path]:
    validate()
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    if not version:
        raise SystemExit("VERSION is empty")

    DIST_DIR.mkdir(exist_ok=True)
    skill_archive = DIST_DIR / f"Pressolve-ChatGPT-Skill-v{version}.zip"
    connector_archive = DIST_DIR / f"Pressolve-Connector-v{version}.zip"

    return [
        write_archive(SKILL_DIR, "pressolve", skill_archive),
        write_archive(CONNECTOR_DIR, "pressolve-connector", connector_archive),
    ]


if __name__ == "__main__":
    for output in build():
        print(output.relative_to(ROOT))
