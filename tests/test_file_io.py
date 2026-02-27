"""Tests for agent/utils/file_io.py"""
import pytest
from pathlib import Path
from agent.utils.file_io import read_text_file, write_text_file, list_txt_files


def test_write_and_read_roundtrip(tmp_path: Path) -> None:
    p = tmp_path / "hello.txt"
    write_text_file(p, "Hello, garden!")
    assert read_text_file(p) == "Hello, garden!"


def test_write_creates_parent_dirs(tmp_path: Path) -> None:
    p = tmp_path / "a" / "b" / "c.txt"
    write_text_file(p, "deep")
    assert p.read_text() == "deep"


def test_list_txt_files_returns_sorted(tmp_path: Path) -> None:
    (tmp_path / "b.txt").write_text("b")
    (tmp_path / "a.txt").write_text("a")
    (tmp_path / "c.md").write_text("ignored")
    files = list_txt_files(tmp_path)
    assert [f.name for f in files] == ["a.txt", "b.txt"]


def test_list_txt_files_missing_folder(tmp_path: Path) -> None:
    assert list_txt_files(tmp_path / "nonexistent") == []