import io
import json
import os
import sys
import streamlit as st

# Ensure project root is on sys.path when launched via "streamlit run"
_CURR = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_CURR)
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

# Support running via package or direct script
try:
    from .config import load_settings
    from .downloader import fetch_with_ytdlp
    from .transcriber import transcribe
    from .chunker import chunk_segments
    from .summarizer import summarize_chunks, synthesize_overview, to_json, to_markdown
except Exception:
    # Absolute imports after adding root to sys.path
    from youtube_summarizer.config import load_settings
    from youtube_summarizer.downloader import fetch_with_ytdlp
    from youtube_summarizer.transcriber import transcribe
    from youtube_summarizer.chunker import chunk_segments
    from youtube_summarizer.summarizer import (
        summarize_chunks,
        synthesize_overview,
        to_json,
        to_markdown,
    )


def app():
    st.set_page_config(page_title="YouTube Summarizer", page_icon="🎬", layout="centered")
    st.title("🎬 YouTube Summarization Agent")
    st.caption("Summarize videos into structured, chaptered summaries")

    settings = load_settings()

    # API key is loaded from env or Streamlit secrets; never hardcoded or shown
    url = st.text_input("YouTube URL", placeholder="https://www.youtube.com/watch?v=...")
    lang = st.text_input("Language code (optional)", value="en")
    go = st.button("Summarize")

    if go and url:
        # Load key only from environment or Streamlit secrets
        api_key = os.getenv("OPENAI_API_KEY") or (
            (st.secrets.get("OPENAI_API_KEY") if hasattr(st, "secrets") else None)
        )
        if not api_key:
            st.error(
                "Missing OpenAI API key. Set OPENAI_API_KEY as an environment variable or add it to .streamlit/secrets.toml"
            )
            return
        settings.openai_api_key = api_key

        with st.status("Fetching metadata and audio via yt-dlp...", expanded=False):
            meta = fetch_with_ytdlp(url, preferred_lang=lang or "en")
        st.success(f"Fetched: {meta.title}")

        with st.status("Transcribing...", expanded=False):
            segments = transcribe(
                audio_path=meta.audio_path,
                transcript_events=meta.transcript_events,
                backend=settings.transcription_backend,
                model=settings.transcription_model,
                language=lang or None,
            )
        st.success(f"Transcript segments: {len(segments)}")

        with st.status("Chunking...", expanded=False):
            chunks = chunk_segments(
                segments,
                max_tokens=settings.max_chunk_tokens,
                gap_seconds=settings.chunk_gap_seconds,
                max_duration_seconds=settings.chunk_max_seconds,
            )
        st.success(f"Chunks: {len(chunks)}")

        with st.status("Summarizing with GPT...", expanded=False):
            chapters = summarize_chunks(
                chunks=chunks,
                video_title=meta.title,
                model=settings.openai_model,
                openai_api_key=settings.openai_api_key,
            )
        st.success("Chapters generated")

        overview = synthesize_overview(chapters, settings.openai_model, settings.openai_api_key)
        result_json = to_json(meta.title, chapters)
        result_md = to_markdown(meta.title, overview, chapters)

        st.subheader("Overview")
        st.write(overview)

        st.subheader("Chapters")
        for ch in result_json["chapters"]:
            st.markdown(f"**{ch['title']}** [{ch['start']} - {ch['end']}]")
            st.write(ch["summary"])
            if ch.get("key_points"):
                st.write("Key Points:")
                for kp in ch["key_points"]:
                    st.write(f"- {kp}")
            st.divider()

        st.download_button(
            "Download JSON",
            data=json.dumps(result_json, ensure_ascii=False, indent=2).encode("utf-8"),
            file_name=f"{meta.video_id}.summary.json",
            mime="application/json",
        )

        st.download_button(
            "Download Markdown",
            data=result_md.encode("utf-8"),
            file_name=f"{meta.video_id}.summary.md",
            mime="text/markdown",
        )


if __name__ == "__main__":
    app()


