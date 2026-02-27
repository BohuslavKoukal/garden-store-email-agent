"""Node: writes the final approved answer to the answers/ folder."""
from __future__ import annotations

from pathlib import Path

from agent.config import settings
from agent.state import EmailState
from agent.utils.file_io import write_text_file


def save_answer_node(state: EmailState) -> dict:
    """Save final_answer to answers/<original_stem>_answer.txt."""
    if state.error or not state.approved or not state.final_answer:
        return {}

    stem = Path(state.file_path).stem
    out_path = settings.answers_folder / f"{stem}_answer.txt"
    write_text_file(out_path, state.final_answer)

    print(f"\n✅  Answer saved to: {out_path}")
    return {"output_file_path": str(out_path)}