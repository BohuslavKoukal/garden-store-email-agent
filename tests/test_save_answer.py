"""Tests for agent/nodes/save_answer.py"""
from pathlib import Path
from unittest.mock import patch
from agent.nodes.save_answer import save_answer_node
from agent.state import EmailState


def test_save_writes_file(tmp_path: Path) -> None:
    answers_dir = tmp_path / "answers"
    with patch("agent.nodes.save_answer.settings") as mock_settings:
        mock_settings.answers_folder = answers_dir
        state = EmailState(
            file_path="/some/path/email_001.txt",
            approved=True,
            final_answer="Here is your plant advice.",
        )
        result = save_answer_node(state)

    out = answers_dir / "email_001_answer.txt"
    assert out.exists()
    assert out.read_text() == "Here is your plant advice."
    assert result["output_file_path"] == str(out)


def test_save_skips_when_not_approved() -> None:
    state = EmailState(approved=False, final_answer="some text")
    result = save_answer_node(state)
    assert result == {}


def test_save_skips_on_error() -> None:
    state = EmailState(error="oops", approved=True, final_answer="text")
    result = save_answer_node(state)
    assert result == {}