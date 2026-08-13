from __future__ import annotations

import hashlib
from pathlib import Path
import subprocess


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def git_provenance(project_root: Path) -> dict[str, str | bool | None]:
    def run(*args: str) -> str | None:
        result = subprocess.run(
            ("git", "-C", str(project_root), *args),
            check=False,
            capture_output=True,
            text=True,
        )
        return result.stdout.strip() if result.returncode == 0 else None

    commit = run("rev-parse", "HEAD")
    status = run("status", "--porcelain", "--untracked-files=no")
    return {
        "git_commit": commit,
        "git_dirty": None if status is None else bool(status),
    }


def implementation_records(project_root: Path) -> list[dict[str, str]]:
    source_root = project_root / "src" / "experiments"
    return [
        {
            "path": str(path.relative_to(project_root)),
            "sha256": _sha256(path),
        }
        for path in sorted(source_root.glob("*.py"))
    ]
