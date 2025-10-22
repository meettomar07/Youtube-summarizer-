import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class Settings:
    openai_api_key: Optional[str]
    openai_model: str
    transcription_backend: str  # "openai" or "whisper_local" or "auto"
    transcription_model: str
    max_chunk_tokens: int
    chunk_max_seconds: int
    chunk_gap_seconds: float
    output_dir: str


def load_settings() -> Settings:
    # Optional: load from .env if present without hard dependency
    try:
        from dotenv import load_dotenv  # type: ignore
        load_dotenv()
    except Exception:
        pass

    return Settings(
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        openai_model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        transcription_backend=os.getenv("TRANSCRIPTION_BACKEND", "auto"),
        transcription_model=os.getenv("TRANSCRIPTION_MODEL", "whisper-1"),
        max_chunk_tokens=int(os.getenv("MAX_CHUNK_TOKENS", "1800")),
        chunk_max_seconds=int(os.getenv("CHUNK_MAX_SECONDS", "480")),
        chunk_gap_seconds=float(os.getenv("CHUNK_GAP_SECONDS", "2.0")),
        output_dir=os.getenv("OUTPUT_DIR", os.path.abspath("outputs")),
    )


