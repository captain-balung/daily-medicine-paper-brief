from urllib.error import HTTPError
from urllib.request import Request, urlopen
import json

from workers.shared.config import Settings


class OpenAITTSClient:
    base_url = "https://api.openai.com/v1/audio/speech"

    def __init__(self, settings: Settings) -> None:
        if not settings.openai_api_key:
            raise RuntimeError("OPENAI_API_KEY is missing.")

        self.api_key = settings.openai_api_key
        self.model = settings.tts_model
        self.voice = settings.tts_voice

    def create_mp3(self, text: str) -> bytes:
        payload = {
            "model": self.model,
            "voice": self.voice,
            "input": _normalize_script_for_speech(text),
            "response_format": "mp3",
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
            line = line.lstrip("#").strip()
        line = line.replace("**", "")
        lines.append(line)

    return "\n\n".join(lines)
