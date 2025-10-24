from dataclasses import dataclass
from typing import List

from transcriber import TranscriptSegment


@dataclass
class Chunk:
    text: str
    start: float
    end: float
    token_estimate: int


def _estimate_tokens(text: str) -> int:
    # rough: 1 token ~= 4 chars
    return max(1, len(text) // 4)


def chunk_segments(
    segments: List[TranscriptSegment],
    max_tokens: int = 1800,
    gap_seconds: float = 2.0,
    max_duration_seconds: int = 480,
) -> List[Chunk]:
    chunks: List[Chunk] = []
    if not segments:
        return chunks

    current_text: List[str] = []
    current_start = segments[0].start
    current_end = segments[0].end
    current_tokens = 0

    def flush():
        nonlocal current_text, current_start, current_end, current_tokens
        if not current_text:
            return
        chunks.append(
            Chunk(text=" ".join(current_text).strip(), start=current_start, end=current_end, token_estimate=current_tokens)
        )
        current_text = []
        current_tokens = 0

    for i, seg in enumerate(segments):
        if i > 0:
            gap = seg.start - segments[i - 1].end
            long_gap = gap > gap_seconds
        else:
            long_gap = False

        seg_tokens = _estimate_tokens(seg.text)
        would_exceed_tokens = current_tokens + seg_tokens > max_tokens
        would_exceed_duration = (seg.end - current_start) > max_duration_seconds

        if long_gap or would_exceed_tokens or would_exceed_duration:
            flush()
            current_start = seg.start
            current_end = seg.end
            current_text = [seg.text]
            current_tokens = seg_tokens
        else:
            current_text.append(seg.text)
            current_tokens += seg_tokens
            current_end = seg.end

    flush()
    return chunks


