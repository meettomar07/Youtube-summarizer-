import json
import os
import subprocess
import tempfile
from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class VideoMetadata:
    video_id: str
    title: str
    duration_seconds: float
    description: Optional[str]
    audio_path: str
    transcript_events: List[Dict]


def _run(cmd: List[str]) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True, check=True)


def fetch_with_ytdlp(video_url: str, preferred_lang: str = "en") -> VideoMetadata:
    try:
        _run(["yt-dlp", "--version"])  # ensure available
    except Exception as exc:
        raise RuntimeError("yt-dlp is not installed. pip install yt-dlp") from exc

    # get id, title, duration, description using print
    info_cmd = [
        "yt-dlp",
        "--print", "%(id)s",
        "--print", "%(title)s",
        "--print", "%(duration)s",
        "--print", "%(description)s",
        "--skip-download",
        video_url,
    ]
    video_id = "unknown"
    title = "Unknown Title"
    duration_seconds = 0.0
    description: Optional[str] = None
    try:
        result = _run(info_cmd)
        lines = result.stdout.splitlines()
        video_id = (lines[0] if len(lines) > 0 else video_id).strip()
        title = (lines[1] if len(lines) > 1 else title).strip()
        try:
            duration_seconds = float((lines[2] if len(lines) > 2 else "0").strip() or 0)
        except Exception:
            duration_seconds = 0.0
        description = ("\n".join(lines[3:]).strip() or None) if len(lines) > 3 else None
    except subprocess.CalledProcessError:
        # Proceed without metadata; will still attempt audio download
        pass

    tmpdir = tempfile.mkdtemp(prefix=f"ys_{video_id}_")
    audio_out = os.path.join(tmpdir, f"{video_id}.m4a")

    # download best audio with fallback options
    audio_cmd = [
        "yt-dlp",
        "-f", "bestaudio[ext=m4a]/bestaudio/best",
        "-x",
        "--audio-format", "m4a",
        "--extractor-args", "youtube:player_client=android,web",
        "--user-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "-o", audio_out,
        video_url,
    ]
    try:
        _run(audio_cmd)
    except subprocess.CalledProcessError as exc:
        # Try fallback with different extractor args
        fallback_cmd = [
            "yt-dlp",
            "-f", "bestaudio",
            "-x",
            "--audio-format", "m4a",
            "--extractor-args", "youtube:player_client=android",
            "-o", audio_out,
            video_url,
        ]
        try:
            _run(fallback_cmd)
        except subprocess.CalledProcessError as exc2:
            raise RuntimeError(f"yt-dlp failed to download audio. Try a different video or check if it's available. Error: {exc2.stderr}") from exc2

    # subtitles json3 (auto if manual not present)
    sub_cmd = [
        "yt-dlp",
        "--write-auto-sub",
        "--sub-format", "json3",
        "--skip-download",
        "-o", os.path.join(tmpdir, video_id),
        "--sub-lang", preferred_lang,
        video_url,
    ]
    # best-effort: subtitles may not exist or fail; continue without error
    try:
        _run(sub_cmd)
    except subprocess.CalledProcessError:
        pass

    # locate json3
    sub_file_lang = os.path.join(tmpdir, f"{video_id}.{preferred_lang}.json3")
    sub_file_generic = os.path.join(tmpdir, f"{video_id}.json3")
    sub_file = sub_file_lang if os.path.exists(sub_file_lang) else sub_file_generic

    transcript_events: List[Dict] = []
    if os.path.exists(sub_file):
        with open(sub_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            transcript_events = data.get("events", []) or []

    return VideoMetadata(
        video_id=video_id,
        title=title,
        duration_seconds=duration_seconds,
        description=description,
        audio_path=audio_out,
        transcript_events=transcript_events,
    )


