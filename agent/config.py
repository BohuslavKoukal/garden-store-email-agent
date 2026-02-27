"""Application configuration loaded from .env."""
from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


class Settings:
    openai_api_key: str = os.environ["OPENAI_API_KEY"]
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4o")
    emails_folder: Path = Path(os.getenv("EMAILS_FOLDER", "emails"))
    answers_folder: Path = Path(os.getenv("ANSWERS_FOLDER", "answers"))


settings = Settings()