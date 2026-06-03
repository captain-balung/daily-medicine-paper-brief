from datetime import UTC, datetime, timedelta, timezone
from zoneinfo import ZoneInfo

from workers.shared.models import PipelineWindow


def daily_window(timezone: str = "Asia/Taipei") -> PipelineWindow:
    tz = _timezone(timezone)
    now = datetime.now(tz)
    end = now.replace(hour=6, minute=0, second=0, microsecond=0)
    if now < end:
        end = end - timedelta(days=1)

    return PipelineWindow(start=end - timedelta(days=1), end=end)


def _timezone(value: str):
    try:
        return ZoneInfo(value)
    except Exception:
        if value == "Asia/Taipei":
            return timezone(timedelta(hours=8), name="Asia/Taipei")
        return UTC
