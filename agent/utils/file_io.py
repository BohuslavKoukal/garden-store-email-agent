"""Utility helpers for reading/writing files."""
from __future__ import annotations

from pathlib import Path


def read_text_file(path: Path) -> str:
    """Return the UTF-8 content of *path*."""
    return path.read_text(encoding="utf-8")


def write_text_file(path: Path, content: str) -> None:
    """Write *content* to *path*, creating parent directories if needed."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def list_txt_files(folder: Path) -> list[Path]:
    """Return all *.txt files inside *folder* (non-recursive)."""
    if not folder.exists():
        return []
    return sorted(folder.glob("*.txt"))