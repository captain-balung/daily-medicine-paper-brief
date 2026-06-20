"""One-off: regenerate all daily podcast videos that were rendered with the
old (CJK-less) font, so Chinese text is no longer garbled.

Skips the already-fixed 2026-06-19 podcast and the 2026-06-03 entry that never
had a video. Safe to re-run; each video is overwritten in place.
"""

import sys
import traceback

from workers.daily_pipeline.generate_podcast_video import generate_podcast_video

# (briefing_date, podcast_id) — every daily podcast that already had a video,
# except a874ec7c (2026-06-19) which was regenerated with the new font already.
TARGETS = [
    ("2026-06-03", "d0c4e456-12d2-460d-8b43-f27a97de14dc"),
    ("2026-06-05", "bdbf08e5-d7db-4626-8b38-20ba70dee09b"),
    ("2026-06-05", "b914118b-9917-43a7-8042-ea861b1727f8"),
    ("2026-06-06", "2d17f067-5736-4fa4-9c8c-5d323b0d1eb6"),
    ("2026-06-07", "7a6d7b5a-7874-41ca-b3a6-3d00e2efd63f"),
    ("2026-06-08", "165bb308-2b18-4497-8de3-06e05a8775d5"),
    ("2026-06-10", "2a50ffe5-346f-4b90-9065-e60426acbd70"),
    ("2026-06-11", "9ef8732d-459f-4004-ac5c-e6d61aecc4d7"),
    ("2026-06-12", "22068398-aaa9-4340-baa0-7bd457d16c62"),
    ("2026-06-13", "022fba49-6a04-4c15-b6c3-48c46840aa40"),
    ("2026-06-14", "837de7c1-48b1-4449-9e23-506f018c3919"),
    ("2026-06-15", "d1d7884f-98aa-4d11-ba56-a60fbf56ef51"),
    ("2026-06-16", "661ecedc-cd9f-41e8-a0d5-4ef7b17b3b63"),
    ("2026-06-17", "ad5adaad-ac27-4784-a0c7-0432e16bfdeb"),
    ("2026-06-18", "30524498-2c02-464f-adec-94292c5faa58"),
]


def main() -> int:
    ok, failed = [], []
    for i, (date, podcast_id) in enumerate(TARGETS, start=1):
        print(f"[{i}/{len(TARGETS)}] {date} {podcast_id} ...", flush=True)
        try:
            url = generate_podcast_video(podcast_id)
            print(f"    OK -> {url}", flush=True)
            ok.append(date)
        except Exception as exc:  # noqa: BLE001 - keep going on any single failure
            print(f"    FAILED: {exc}", flush=True)
            traceback.print_exc()
            failed.append((date, podcast_id, str(exc)))

    print("\n==== SUMMARY ====", flush=True)
    print(f"OK ({len(ok)}): {', '.join(ok)}", flush=True)
    if failed:
        print(f"FAILED ({len(failed)}):", flush=True)
        for date, pid, err in failed:
            print(f"  {date} {pid} -> {err}", flush=True)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
