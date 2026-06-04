from urllib.error import HTTPError
from urllib.request import Request, urlopen
import json
import time

from workers.shared.config import Settings
from workers.shared.podcast_style import (
    FAST_OPENING_SPEED,
    FIXED_DAILY_PODCAST_OPENING,
    NORMAL_PODCAST_SPEED,
)


class OpenAITTSClient:
    base_url = "https://api.openai.com/v1/audio/speech"

    def __init__(self, settings: Settings) -> None:
        if not settings.openai_api_key:
            raise RuntimeError("OPENAI_API_KEY is missing.")

        self.api_key = settings.openai_api_key
        self.model = settings.tts_model
        self.voice = settings.tts_voice

    def create_mp3(self, text: str) -> bytes:
        segments = _speech_segments(text)
        audio_parts = []
        is_first_chunk = True
        for segment_text, speed in segments:
            chunks = _chunk_text(segment_text)
            for chunk in chunks:
                if not is_first_chunk:
                    time.sleep(0.5)
                audio_parts.append(self._create_mp3_chunk(chunk, speed=speed))
                is_first_chunk = False

        return b"".join(audio_parts)

    def _create_mp3_chunk(self, text: str, *, speed: float) -> bytes:
        payload = {
            "model": self.model,
            "voice": self.voice,
            "input": text,
            "response_format": "mp3",
            "speed": speed,
        }
        request = Request(
            self.base_url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )

        try:
            with urlopen(request, timeout=180) as response:
                return response.read()
        except HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"OpenAI TTS error {exc.code}: {body}") from exc


def _normalize_script_for_speech(script: str) -> str:
    lines = []
    for raw_line in script.splitlines():
        line = raw_line.strip()
        if not line or line == "---":
            continue
        if line.startswith("#"):
            continue
        line = line.replace("**", "")
        lines.append(line)

    return "\n\n".join(lines)


def _speech_segments(script: str) -> list[tuple[str, float]]:
    normalized = _normalize_script_for_speech(script)
    opening = FIXED_DAILY_PODCAST_OPENING.strip()

    if normalized.startswith(opening):
        rest = normalized[len(opening) :].strip()
        segments = [(opening, FAST_OPENING_SPEED)]
        if rest:
            segments.append((rest, NORMAL_PODCAST_SPEED))
        return segments

    return [(normalized, NORMAL_PODCAST_SPEED)] if normalized else []


def _chunk_text(text: str, max_chars: int = 900) -> list[str]:
    paragraphs = [paragraph.strip() for paragraph in text.split("\n\n") if paragraph.strip()]
    chunks = []
    current = ""

    for paragraph in paragraphs:
        if len(paragraph) > max_chars:
            if current:
                chunks.append(current)
                current = ""
            chunks.extend(_split_long_paragraph(paragraph, max_chars=max_chars))
            continue

        candidate = f"{current}\n\n{paragraph}".strip() if current else paragraph
        if len(candidate) > max_chars:
            if current:
                chunks.append(current)
            current = paragraph
        else:
            current = candidate

    if current:
        chunks.append(current)

    return chunks


def _split_long_paragraph(paragraph: str, max_chars: int) -> list[str]:
    pieces = []
    current = ""
    for sentence in paragraph.replace("。", "。\n").replace("；", "；\n").splitlines():
        sentence = sentence.strip()
        if not sentence:
            continue
        candidate = current + sentence
        if len(candidate) > max_chars and current:
            pieces.append(current)
            current = sentence
        else:
            current = candidate
    if current:
        pieces.append(current)
    return pieces
