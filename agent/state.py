"""LangGraph state shared between all nodes."""
from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, Field

Intent = Literal["plant_instructions", "other"]


class EmailState(BaseModel):
    """Immutable snapshot flowing through the graph for a single email."""

    # --- input ---
    file_path: str = Field(default="", description="Absolute path to the source .txt file")
    email_body: str = Field(default="", description="Raw email text")
    sender_name: str = Field(default="Customer", description="Extracted or inferred sender name")

    # --- classifier output ---
    intent: Optional[Intent] = Field(default=None)
    topic: str = Field(default="", description="Short topic extracted by the classifier")

    # --- generated reply ---
    draft_answer: str = Field(default="", description="LLM-generated draft response")

    # --- human-in-the-loop ---
    approved: Optional[bool] = Field(default=None)
    human_feedback: str = Field(default="", description="Optional feedback / edited text")

    # --- final answer ---
    final_answer: str = Field(default="", description="Answer that will be saved to disk")

    # --- metadata ---
    output_file_path: str = Field(default="", description="Where the answer was saved")
    error: str = Field(default="", description="Non-empty when a node encountered an error")