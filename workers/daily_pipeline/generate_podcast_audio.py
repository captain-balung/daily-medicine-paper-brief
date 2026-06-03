import argparse

from workers.shared.config import load_settings
from workers.shared.persistence import PipelineRepository, _estimated_duration_seconds
from workers.shared.supabase_rest import SupabaseRestClient
from workers.tts.openai_client import OpenAITTSClient


def generate_podcast_audio(podcast_id: str) -> str:
    settings = load_settings()
    if settings.tts_provider != "openai":
        raise RuntimeError(f"Unsupported TTS_PROVIDER: {settings.tts_provider}")

    supabase = SupabaseRestClient(
        supabase_url=settings.supabase_url or "",
        secret_key=settings.supabase_secret_key or "",
    )
    repository = PipelineRepository(supabase)
    podcast = repository.get_podcast(podcast_id)
    if not podcast:
        raise RuntimeError(f"Podcast not found: {podcast_id}")

    script = podcast.get("script")
    if not script:
        raise RuntimeError(f"Podcast has no script: {podcast_id}")

    daily_briefing_id = podcast.get("daily_briefing_id")
    if not daily_briefing_id:
        raise RuntimeError("Only daily podcast audio is supported for now.")

    bundle = repository.get_daily_briefing_bundle(daily_briefing_id)
    if not bundle:
        raise RuntimeError(f"Daily briefing not found: {daily_briefing_id}")

    briefing_date = bundle["briefing"]["briefing_date"]
    object_path = f"podcasts/daily/{briefing_date}.mp3"
    audio = OpenAITTSClient(settings).create_mp3(script)
    audio_url = supabase.upload_storage_object(
        bucket=settings.podcast_audio_bucket,
        object_path=object_path,
        data=audio,
        content_type="audio/mpeg",
    )
    repository.update_podcast_audio(
        podcast_id,
        audio_storage_path=object_path,
        audio_url=audio_url,
        voice_name=settings.tts_voice,
        tts_provider=settings.tts_provider,
        duration_seconds=_estimated_duration_seconds(script),
    )
    print(f"podcast_audio={audio_url}")
    return audio_url


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("podcast_id")
    args = parser.parse_args()
    generate_podcast_audio(args.podcast_id)


if __name__ == "__main__":
    main()
