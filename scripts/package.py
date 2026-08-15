#!/usr/bin/env python3
"""Build a deterministic, upload-ready Pressolve skill ZIP."""

from __future__ import annotations

import hashlib
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "pressolve"
DIST_DIR = ROOT / "dist"
FIXED_TIME = (2020, 1, 1, 0, 0, 0)
REQUIRED_FILES = (
    "SKILL.md",
    "agents/openai.yaml",
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


def build() -> Path:
    validate()
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    if not version:
        raise SystemExit("VERSION is empty")

    DIST_DIR.mkdir(exist_ok=True)
    archive = DIST_DIR / f"Pressolve-ChatGPT-Skill-v{version}.zip"

    with ZipFile(archive, "w", compression=ZIP_DEFLATED, compresslevel=9) as bundle:
        for source in sorted(path for path in SKILL_DIR.rglob("*") if path.is_file()):
            relative = source.relative_to(SKILL_DIR)
            info = ZipInfo(f"pressolve/{relative.as_posix()}", FIXED_TIME)
            info.compress_type = ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            bundle.writestr(info, source.read_bytes(), compress_type=ZIP_DEFLATED, compresslevel=9)

    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    checksum = archive.with_suffix(archive.suffix + ".sha256")
    checksum.write_text(f"{digest}  {archive.name}\n", encoding="utf-8")
    return archive


if __name__ == "__main__":
    output = build()
    print(output.relative_to(ROOT))
