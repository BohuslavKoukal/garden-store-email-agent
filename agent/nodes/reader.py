"""Node: reads an email .txt file and populates the state."""
from __future__ import annotations

from pathlib import Path

from agent.state import EmailState
from agent.utils.file_io import read_text_file


def reader_node(state: EmailState) -> dict:
    """Read the email file and return updated state fields."""
    path = Path(state.file_path)
    if not path.exists():
        return {"error": f"File not found: {path}"}

    body = read_text_file(path)

    # Very simple heuristic: look for "My name is X" or just use "Customer"
    sender_name = "Customer"
    for line in body.splitlines():
        low = line.lower()
        if "my name is" in low:
            parts = line.split("is", 1)
            if len(parts) == 2:
                sender_name = parts[1].strip().rstrip(".,!").strip()
            break

    return {"email_body": body, "sender_name": sender_name}