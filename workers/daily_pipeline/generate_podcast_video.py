import argparse
import subprocess
import tempfile
from pathlib import Path
from urllib.request import urlopen

from PIL import Image, ImageDraw, ImageFont
import imageio_ffmpeg

from workers.shared.config import Settings, load_settings
from workers.shared.persistence import PipelineRepository
from workers.shared.supabase_rest import SupabaseRestClient


WIDTH = 1920
HEIGHT = 1080
MARGIN_X = 220
ACCENT = (15, 118, 110)
ACCENT_DARK = (17, 94, 89)
BACKGROUND = (247, 248, 250)
FOREGROUND = (24, 32, 42)
MUTED = (102, 112, 133)
SURFACE = (255, 255, 255)
BORDER = (216, 222, 230)
WARNING_BG = (255, 250, 242)
WARNING_TEXT = (107, 75, 22)


def generate_podcast_video(podcast_id: str) -> str:
    settings = load_settings()
    supabase = SupabaseRestClient(
        supabase_url=settings.supabase_url or "",
        secret_key=settings.supabase_secret_key or "",
    )
    repository = PipelineRepository(supabase)
    podcast = repository.get_podcast(podcast_id)
    if not podcast:
        raise RuntimeError(f"Podcast not found: {podcast_id}")
    if not podcast.get("audio_url"):
        raise RuntimeError(f"Podcast has no audio: {podcast_id}")

    daily_briefing_id = podcast.get("daily_briefing_id")
    if not daily_briefing_id:
        raise RuntimeError("Only daily podcast video is supported for now.")

    bundle = repository.get_daily_briefing_bundle(daily_briefing_id)
    if not bundle:
        raise RuntimeError(f"Daily briefing not found: {daily_briefing_id}")

    briefing_date = bundle["briefing"]["briefing_date"]
    object_path = f"podcasts/daily/{briefing_date}.mp4"

    with tempfile.TemporaryDirectory(prefix="daily-medicine-video-") as temp_dir:
        work_dir = Path(temp_dir)
        audio_path = work_dir / "audio.mp3"
        output_path = work_dir / "daily-video.mp4"
        _download(podcast["audio_url"], audio_path)
        slide_paths = _render_slides(work_dir, bundle, podcast, settings)
        _compose_video(
            audio_path=audio_path,
            slide_paths=slide_paths,
            output_path=output_path,
            duration_seconds=podcast.get("duration_seconds") or 420,
        )
        video_url = supabase.upload_storage_object(
            bucket=settings.podcast_video_bucket,
            object_path=object_path,
            data=output_path.read_bytes(),
            content_type="video/mp4",
        )

    repository.update_podcast_video(
        podcast_id,
        video_storage_path=object_path,
        video_url=video_url,
    )
    print(f"podcast_video={video_url}")
    return video_url


def _download(url: str, path: Path) -> None:
    with urlopen(url, timeout=60) as response:
        path.write_bytes(response.read())


def _render_slides(
    work_dir: Path, bundle: dict, podcast: dict, settings: Settings
) -> list[Path]:
    font_regular = _load_font(settings, 42)
    font_medium = _load_font(settings, 50)
    font_large = _load_font(settings, 76)
    font_small = _load_font(settings, 32)
    font_tiny = _load_font(settings, 26)

    briefing = bundle["briefing"]
    must_read_items = [
        item for item in bundle["items"] if item.get("section") == "must_read"
    ][:5]
    featured_items = must_read_items[:3]

    slides = []
    slides.append(
        _slide_title(
            work_dir / "01-title.png",
            briefing,
            font_large,
            font_medium,
            font_regular,
            font_small,
        )
    )
    slides.append(
        _slide_ranking(
            work_dir / "02-ranking.png",
            featured_items,
            font_medium,
            font_regular,
            font_small,
            font_tiny,
        )
    )

    for index, item in enumerate(featured_items, start=1):
        slides.append(
            _slide_article(
                work_dir / f"0{index + 2}-article-{index}.png",
                index,
                item,
                font_medium,
                font_regular,
                font_small,
                font_tiny,
            )
        )

    slides.append(
        _slide_notice(
            work_dir / "06-notice.png",
            podcast,
            font_medium,
            font_regular,
            font_small,
        )
    )
    return slides


def _slide_title(
    path: Path,
    briefing: dict,
    font_large: ImageFont.FreeTypeFont,
    font_medium: ImageFont.FreeTypeFont,
    font_regular: ImageFont.FreeTypeFont,
    font_small: ImageFont.FreeTypeFont,
) -> Path:
    image, draw = _base_slide()
    _brand(draw, font_small)
    draw.text((MARGIN_X, 250), briefing["title"], font=font_large, fill=FOREGROUND)
    _draw_wrapped(
        draw,
        _format_summary(briefing.get("summary") or ""),
        (MARGIN_X, 370),
        font_regular,
        MUTED,
        max_width=WIDTH - MARGIN_X * 2,
        line_gap=18,
        max_lines=4,
    )
    _draw_card(draw, (MARGIN_X, 610, WIDTH - MARGIN_X, 820))
    draw.text((MARGIN_X + 44, 655), "Source window", font=font_medium, fill=FOREGROUND)
    source_window = (
        f"{_format_timestamp(briefing.get('source_window_start'))} to "
        f"{_format_timestamp(briefing.get('source_window_end'))}"
    )
    _draw_wrapped(
        draw,
        source_window,
        (MARGIN_X + 44, 735),
        font_small,
        MUTED,
        max_width=WIDTH - MARGIN_X * 2 - 88,
    )
    image.save(path)
    return path


def _slide_ranking(
    path: Path,
    items: list[dict],
    font_medium: ImageFont.FreeTypeFont,
    font_regular: ImageFont.FreeTypeFont,
    font_small: ImageFont.FreeTypeFont,
    font_tiny: ImageFont.FreeTypeFont,
) -> Path:
    image, draw = _base_slide()
    _brand(draw, font_small)
    draw.text((MARGIN_X, 170), "Today's Top Ranking", font=font_medium, fill=FOREGROUND)
    y = 280
    for index, item in enumerate(items, start=1):
        article = item.get("article") or {}
        score = item.get("score") or {}
        title = article.get("title_zh") or article.get("title") or "Untitled"
        rationale = score.get("scoring_rationale") or item.get("item_summary") or ""
        _draw_card(draw, (MARGIN_X, y, WIDTH - MARGIN_X, y + 190))
        draw.text((MARGIN_X + 36, y + 38), str(index), font=font_medium, fill=ACCENT_DARK)
        draw.text(
            (MARGIN_X + 110, y + 34),
            f"Score {score.get('total_score', '-')}",
            font=font_tiny,
            fill=ACCENT_DARK,
        )
        _draw_wrapped(
            draw,
            title,
            (MARGIN_X + 110, y + 72),
            font_regular,
            FOREGROUND,
            max_width=600,
            max_lines=2,
        )
        _draw_wrapped(
            draw,
            rationale,
            (MARGIN_X + 760, y + 42),
            font_small,
            MUTED,
            max_width=700,
            max_lines=4,
            line_gap=10,
        )
        y += 220
    image.save(path)
    return path


def _slide_article(
    path: Path,
    index: int,
    item: dict,
    font_medium: ImageFont.FreeTypeFont,
    font_regular: ImageFont.FreeTypeFont,
    font_small: ImageFont.FreeTypeFont,
    font_tiny: ImageFont.FreeTypeFont,
) -> Path:
    image, draw = _base_slide()
    _brand(draw, font_small)
    article = item.get("article") or {}
    summary = item.get("summary") or {}
    score = item.get("score") or {}
    title = article.get("title_zh") or article.get("title") or "Untitled"

    draw.text(
        (MARGIN_X, 150),
        f"Featured Analysis #{index}",
        font=font_medium,
        fill=ACCENT_DARK,
    )
    _draw_wrapped(
        draw,
        title,
        (MARGIN_X, 235),
        font_medium,
        FOREGROUND,
        max_width=WIDTH - MARGIN_X * 2,
        max_lines=3,
        line_gap=16,
    )
    metadata = "  ".join(
        value
        for value in [
            article.get("journal"),
            f"PMID {article.get('pmid')}" if article.get("pmid") else None,
            f"DOI {article.get('doi')}" if article.get("doi") else None,
            f"Score {score.get('total_score')}" if score.get("total_score") else None,
        ]
        if value
    )
    _draw_wrapped(draw, metadata, (MARGIN_X, 430), font_tiny, MUTED, max_width=1450)
    _draw_card(draw, (MARGIN_X, 500, WIDTH - MARGIN_X, 835))
    _draw_wrapped(
        draw,
        summary.get("clinical_implications")
        or summary.get("one_sentence_summary")
        or item.get("item_summary")
        or "",
        (MARGIN_X + 44, 545),
        font_regular,
        FOREGROUND,
        max_width=WIDTH - MARGIN_X * 2 - 88,
        max_lines=5,
        line_gap=16,
    )
    limitation = summary.get("limitations")
    if limitation:
        draw.text((MARGIN_X + 44, 760), "Limitation", font=font_tiny, fill=ACCENT_DARK)
        _draw_wrapped(
            draw,
            limitation,
            (MARGIN_X + 220, 756),
            font_tiny,
            MUTED,
            max_width=980,
            max_lines=2,
        )
    image.save(path)
    return path


def _slide_notice(
    path: Path,
    podcast: dict,
    font_medium: ImageFont.FreeTypeFont,
    font_regular: ImageFont.FreeTypeFont,
    font_small: ImageFont.FreeTypeFont,
) -> Path:
    image, draw = _base_slide()
    _brand(draw, font_small)
    draw.text((MARGIN_X, 220), "Content and source notice", font=font_medium, fill=FOREGROUND)
    _draw_card(draw, (MARGIN_X, 330, WIDTH - MARGIN_X, 760), fill=WARNING_BG)
    notice = (
        "This video is an AI-assisted medical literature briefing based on "
        "article metadata, source links, and generated summaries. It is not "
        "a reproduction of publisher full text, and it is not medical advice. "
        "Please verify all findings using the original PMID, DOI, and publisher sources."
    )
    _draw_wrapped(
        draw,
        notice,
        (MARGIN_X + 48, 400),
        font_regular,
        WARNING_TEXT,
        max_width=WIDTH - MARGIN_X * 2 - 96,
        max_lines=6,
        line_gap=18,
    )
    if podcast.get("voice_name"):
        draw.text(
            (MARGIN_X + 48, 670),
            f"AI voice: {podcast['voice_name']}",
            font=font_small,
            fill=WARNING_TEXT,
        )
    image.save(path)
    return path


def _compose_video(
    *,
    audio_path: Path,
    slide_paths: list[Path],
    output_path: Path,
    duration_seconds: int,
) -> None:
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    slide_duration = max(10, duration_seconds / max(1, len(slide_paths)))
    list_path = output_path.with_suffix(".txt")
    lines = []
    for slide_path in slide_paths:
        lines.append(f"file '{slide_path.as_posix()}'")
        lines.append(f"duration {slide_duration:.3f}")
    lines.append(f"file '{slide_paths[-1].as_posix()}'")
    list_path.write_text("\n".join(lines) + "\n", encoding="ascii")

    command = [
        ffmpeg,
        "-hide_banner",
        "-loglevel",
        "warning",
        "-y",
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        str(list_path),
        "-i",
        str(audio_path),
        "-t",
        str(duration_seconds),
        "-vf",
        "scale=1920:1080,setsar=1,format=yuv420p",
        "-r",
        "30",
        "-c:v",
        "libx264",
        "-preset",
        "medium",
        "-crf",
        "23",
        "-c:a",
        "aac",
        "-b:a",
        "192k",
        str(output_path),
    ]
    subprocess.run(command, check=True)


def _base_slide() -> tuple[Image.Image, ImageDraw.ImageDraw]:
    image = Image.new("RGB", (WIDTH, HEIGHT), BACKGROUND)
    draw = ImageDraw.Draw(image)
    return image, draw


def _brand(draw: ImageDraw.ImageDraw, font: ImageFont.FreeTypeFont) -> None:
    draw.text((MARGIN_X, 70), "Daily Medicine Paper Brief", font=font, fill=FOREGROUND)
    draw.line((MARGIN_X, 120, WIDTH - MARGIN_X, 120), fill=BORDER, width=2)


def _draw_card(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    fill: tuple[int, int, int] = SURFACE,
) -> None:
    draw.rounded_rectangle(box, radius=18, fill=fill, outline=BORDER, width=2)


def _draw_wrapped(
    draw: ImageDraw.ImageDraw,
    text: str,
    xy: tuple[int, int],
    font: ImageFont.FreeTypeFont,
    fill: tuple[int, int, int],
    *,
    max_width: int,
    max_lines: int = 8,
    line_gap: int = 12,
) -> None:
    x, y = xy
    lines = _wrap_text(draw, text, font, max_width)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        lines[-1] = lines[-1].rstrip(".,;:，。；：") + "..."
    line_height = font.size + line_gap
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        y += line_height


def _wrap_text(
    draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont, max_width: int
) -> list[str]:
    text = " ".join(str(text).split())
    if not text:
        return []

    lines = []
    current = ""
    for chunk in _text_chunks(text):
        candidate = current + chunk
        if current and draw.textlength(candidate, font=font) > max_width:
            lines.append(current.rstrip())
            current = chunk.lstrip()
        else:
            current = candidate
    if current:
        lines.append(current.rstrip())
    return lines


def _text_chunks(text: str) -> list[str]:
    return list(text)


def _format_summary(summary: str) -> str:
    return summary.replace("Today:", "Today: ")


def _format_timestamp(value: str | None) -> str:
    if not value:
        return "-"
    return value.replace("T", " ").replace("+00:00", " UTC")


def _load_font(settings: Settings, size: int) -> ImageFont.FreeTypeFont:
    candidates = []
    if settings.video_font_path:
        candidates.append(Path(settings.video_font_path))
    candidates.extend(
        [
            Path("C:/Windows/Fonts/msjh.ttc"),
            Path("C:/Windows/Fonts/msjhbd.ttc"),
            Path("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"),
            Path("/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc"),
            Path("/usr/share/fonts/truetype/wqy/wqy-microhei.ttc"),
            Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
        ]
    )
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size=size)
    return ImageFont.load_default(size=size)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("podcast_id")
    args = parser.parse_args()
    generate_podcast_video(args.podcast_id)


if __name__ == "__main__":
    main()
