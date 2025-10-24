import argparse
import json
import os
from typing import Optional

from config import load_settings
from downloader import fetch_with_ytdlp
from transcriber import transcribe
from chunker import chunk_segments
from summarizer import summarize_chunks, synthesize_overview, to_json, to_markdown


def run(url: str, out_json: Optional[str], out_md: Optional[str], language: Optional[str]) -> None:
    settings = load_settings()
    os.makedirs(settings.output_dir, exist_ok=True)

    meta = fetch_with_ytdlp(url, preferred_lang=language or "en")

    segments = transcribe(
        audio_path=meta.audio_path,
        transcript_events=meta.transcript_events,
        backend=settings.transcription_backend,
        model=settings.transcription_model,
        language=language,
    )

    chunks = chunk_segments(
        segments,
        max_tokens=settings.max_chunk_tokens,
        gap_seconds=settings.chunk_gap_seconds,
        max_duration_seconds=settings.chunk_max_seconds,
    )

    chapters = summarize_chunks(
        chunks=chunks,
        video_title=meta.title,
        model=settings.huggingface_model,
        huggingface_api_key=settings.huggingface_api_key,
    )

    overview = synthesize_overview(chapters, settings.huggingface_model, settings.huggingface_api_key)
    result_json = to_json(meta.title, chapters)
    result_md = to_markdown(meta.title, overview, chapters)

    if out_json is None:
        out_json = os.path.join(settings.output_dir, f"{meta.video_id}.summary.json")
    if out_md is None:
        out_md = os.path.join(settings.output_dir, f"{meta.video_id}.summary.md")

    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(result_json, f, ensure_ascii=False, indent=2)
    with open(out_md, "w", encoding="utf-8") as f:
        f.write(result_md)

    print(f"Saved JSON to {out_json}")
    print(f"Saved Markdown to {out_md}")


def cli():
    p = argparse.ArgumentParser(description="YouTube Summarization Agent")
    p.add_argument("url", help="YouTube video URL")
    p.add_argument("--json", dest="json_out", default=None, help="Output JSON path")
    p.add_argument("--md", dest="md_out", default=None, help="Output Markdown path")
    p.add_argument("--lang", dest="language", default=None, help="Language code (e.g., en, es)")
    args = p.parse_args()
    run(args.url, args.json_out, args.md_out, args.language)


if __name__ == "__main__":
    cli()


