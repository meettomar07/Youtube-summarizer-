import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class Settings:
    huggingface_api_key: Optional[str]
    huggingface_model: str
    transcription_backend: str  # "huggingface" or "whisper_local" or "auto"
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
        huggingface_api_key=os.getenv("HUGGINGFACE_API_KEY"),
        huggingface_model=os.getenv("HUGGINGFACE_MODEL", "facebook/bart-large-cnn"),
        transcription_backend=os.getenv("TRANSCRIPTION_BACKEND", "huggingface"),
        transcription_model=os.getenv("TRANSCRIPTION_MODEL", "openai/whisper-large"),
        max_chunk_tokens=int(os.getenv("MAX_CHUNK_TOKENS", "800")),
        chunk_max_seconds=int(os.getenv("CHUNK_MAX_SECONDS", "480")),
        chunk_gap_seconds=float(os.getenv("CHUNK_GAP_SECONDS", "2.0")),
        output_dir=os.getenv("OUTPUT_DIR", os.path.abspath("outputs")),
    )


