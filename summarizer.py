import json
import time
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from .chunker import Chunk


@dataclass
class Chapter:
    title: str
    start: float
    end: float
    summary: str
    key_points: List[str]


def _retry(fn, retries: int = 3, backoff: float = 1.5):
    err: Optional[Exception] = None
    for i in range(retries):
        try:
            return fn()
        except Exception as e:
            err = e
            time.sleep(backoff * (2 ** i))
    if err:
        raise err
    raise RuntimeError("Retry failed without exception")


def summarize_chunks(
    chunks: List[Chunk],
    video_title: str,
    model: str,
    openai_api_key: Optional[str],
) -> List[Chapter]:
    try:
        from openai import OpenAI  # type: ignore
    except Exception as exc:
        raise RuntimeError("openai package not installed. pip install openai") from exc

    client = OpenAI(api_key=openai_api_key) if openai_api_key else OpenAI()

    chapters: List[Chapter] = []
    for idx, ch in enumerate(chunks, start=1):
        user_prompt = (
            f"Analyze this section from the video '{video_title}'.\n"
            "Return strict JSON with keys: title (5-8 words), summary (2-3 sentences), key_points (3-5 bullets as strings).\n\n"
            f"Transcript section:\n{ch.text}"
        )

        def call():
            resp = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are an expert video content analyzer producing structured outputs."},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.3,
                response_format={"type": "json_object"},
            )
            return resp

        try:
            resp = _retry(call)
            content = resp.choices[0].message.content
            data = json.loads(content)
            chapters.append(
                Chapter(
                    title=data.get("title", f"Chapter {idx}"),
                    start=ch.start,
                    end=ch.end,
                    summary=data.get("summary", ""),
                    key_points=list(data.get("key_points", [])),
                )
            )
        except Exception:
            chapters.append(
                Chapter(title=f"Chapter {idx}", start=ch.start, end=ch.end, summary="Summary unavailable", key_points=[])
            )

    return chapters


def synthesize_overview(chapters: List[Chapter], model: str, openai_api_key: Optional[str]) -> str:
    try:
        from openai import OpenAI  # type: ignore
    except Exception as exc:
        raise RuntimeError("openai package not installed. pip install openai") from exc
    client = OpenAI(api_key=openai_api_key) if openai_api_key else OpenAI()

    summaries = " ".join(c.summary for c in chapters if c.summary)
    if not summaries:
        return "This video covers multiple topics and key insights."

    def call():
        return client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "Create a brief, engaging overview from chapter summaries."},
                {"role": "user", "content": f"Synthesize into a 3-4 sentence overview:\n{summaries}"},
            ],
            temperature=0.3,
            max_tokens=200,
        )

    try:
        resp = _retry(call)
        return resp.choices[0].message.content.strip()
    except Exception:
        return "This video covers multiple topics and key insights."


def to_json(video_title: str, chapters: List[Chapter]) -> Dict[str, Any]:
    def fmt(ts: float) -> str:
        h = int(ts // 3600)
        m = int((ts % 3600) // 60)
        s = int(ts % 60)
        return f"{h:02d}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"

    return {
        "video_title": video_title,
        "chapters": [
            {
                "start": fmt(c.start),
                "end": fmt(c.end),
                "title": c.title,
                "summary": c.summary,
                "key_points": c.key_points,
            }
            for c in chapters
        ],
    }


def to_markdown(video_title: str, overview: str, chapters: List[Chapter]) -> str:
    def fmt(ts: float) -> str:
        h = int(ts // 3600)
        m = int((ts % 3600) // 60)
        s = int(ts % 60)
        return f"{h:02d}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"

    lines: List[str] = [f"# {video_title}", "", "## Video Summary", "", overview, "", "## Chapters", ""]
    for i, c in enumerate(chapters, start=1):
        lines.append(f"### {i}. {c.title} [{fmt(c.start)}]")
        lines.append("")
        if c.summary:
            lines.append(c.summary)
            lines.append("")
        if c.key_points:
            lines.append("Key Points:")
            for kp in c.key_points:
                lines.append(f"- {kp}")
            lines.append("")
    return "\n".join(lines).strip() + "\n"


