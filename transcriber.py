import json
import os
from dataclasses import dataclass
from typing import Dict, List, Literal, Optional


@dataclass
class TranscriptSegment:
    start: float
    end: float
    text: str


def _segments_from_json3(events: List[Dict]) -> List[TranscriptSegment]:
    segments: List[TranscriptSegment] = []
    for ev in events:
        if "segs" not in ev:
            continue
        start = float(ev.get("tStartMs", 0)) / 1000.0
        dur = float(ev.get("dDurationMs", ev.get("dDurationMs", 0))) / 1000.0
        end = start + (dur if dur > 0 else 0)
        text = "".join(seg.get("utf8", "") for seg in ev.get("segs", []))
        if text.strip():
            segments.append(TranscriptSegment(start=start, end=end, text=text.strip()))
    return segments


def transcribe(
    audio_path: str,
    transcript_events: Optional[List[Dict]],
    backend: Literal["auto", "openai", "whisper_local", "huggingface"] = "huggingface",
    model: str = "openai/whisper-large",
    language: Optional[str] = None,
) -> List[TranscriptSegment]:
    # Prefer provided json3 events when available
    if transcript_events:
        return _segments_from_json3(transcript_events)

    selected = backend
    if backend == "auto":
        selected = "huggingface" if os.getenv("HUGGINGFACE_API_KEY") else "whisper_local"

    if selected == "openai":
        try:
            from openai import OpenAI  # type: ignore
        except Exception as exc:
            raise RuntimeError("openai package not installed. pip install openai") from exc

        client = OpenAI()
        with open(audio_path, "rb") as f:
            resp = client.audio.transcriptions.create(
                model=model,
                file=f,
                language=language,
                response_format="verbose_json",
                timestamp_granularities=["segment"],
            )
        segments: List[TranscriptSegment] = []
        for seg in resp.segments or []:
            segments.append(
                TranscriptSegment(start=float(seg.get("start", 0)), end=float(seg.get("end", 0)), text=seg.get("text", "").strip())
            )
        return segments

    # ---------------- Hugging Face transcription ----------------
    if selected == "huggingface":
        try:
            from transformers import pipeline
        except Exception as exc:
            raise RuntimeError("transformers package not installed. pip install transformers") from exc

        hf_transcriber = pipeline("automatic-speech-recognition", model="openai/whisper-large")
        result = hf_transcriber(audio_path)
        segments: List[TranscriptSegment] = [
            TranscriptSegment(start=0.0, end=0.0, text=result["text"].strip())
        ]
        return segments

    # whisper local
    try:
        import whisper  # type: ignore
    except Exception as exc:
        raise RuntimeError("Local whisper not installed. pip install openai-whisper") from exc

    wmodel = whisper.load_model("medium" if model == "whisper-1" else model)
    result = wmodel.transcribe(audio_path, language=language, verbose=False)
    segments: List[TranscriptSegment] = []
    for seg in result.get("segments", []):
        segments.append(
            TranscriptSegment(start=float(seg.get("start", 0)), end=float(seg.get("end", 0)), text=seg.get("text", "").strip())
        )
    return segments


