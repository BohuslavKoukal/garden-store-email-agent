"""Tests for agent/nodes/reader.py"""
from pathlib import Path
from agent.nodes.reader import reader_node
from agent.state import EmailState


def test_reader_extracts_body(tmp_path: Path) -> None:
    email = tmp_path / "test.txt"
    email.write_text("Hello from the garden!")
    state = EmailState(file_path=str(email))
    result = reader_node(state)
    assert result["email_body"] == "Hello from the garden!"


def test_reader_extracts_sender_name(tmp_path: Path) -> None:
    email = tmp_path / "named.txt"
    email.write_text("Hi,\nMy name is Alice.\nI have a question.")
    state = EmailState(file_path=str(email))
    result = reader_node(state)
    assert result["sender_name"] == "Alice"


def test_reader_missing_file() -> None:
    state = EmailState(file_path="/nonexistent/path/email.txt")
    result = reader_node(state)
    assert "error" in result
    assert result["error"] != ""


def test_reader_default_sender_name(tmp_path: Path) -> None:
    email = tmp_path / "anon.txt"
    email.write_text("No name here.")
    state = EmailState(file_path=str(email))
    result = reader_node(state)
    assert result["sender_name"] == "Customer"