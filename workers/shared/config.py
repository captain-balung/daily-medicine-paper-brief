from dataclasses import dataclass
import os
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    supabase_url: str | None
    supabase_secret_key: str | None
    anthropic_api_key: str | None
    anthropic_model: str
    ncbi_api_key: str | None
    unpaywall_email: str | None
    crossref_mailto: str | None
    database_url: str | None
    publication_mode: str
    mvp_sources: tuple[str, ...]
    timezone: str

    def health_checks(self) -> dict[str, bool]:
        return {
            "supabase_url": bool(self.supabase_url),
            "supabase_secret_key": bool(self.supabase_secret_key),
            "anthropic_api_key": bool(self.anthropic_api_key),
            "unpaywall_email": bool(self.unpaywall_email),
            "crossref_mailto": bool(self.crossref_mailto),
            "publication_mode_auto_publish": self.publication_mode == "auto_publish",
            "core_sources": set(self.mvp_sources) == {"pubmed", "crossref", "unpaywall"},
        }


def _split_csv(value: str | None) -> tuple[str, ...]:
    if not value:
        return ("pubmed", "crossref", "unpaywall")

    return tuple(item.strip() for item in value.split(",") if item.strip())


def load_settings() -> Settings:
    _load_dotenv()

    return Settings(
        supabase_url=os.getenv("SUPABASE_URL"),
        supabase_secret_key=os.getenv("SUPABASE_SECRET_KEY")
        or os.getenv("SUPABASE_SERVICE_ROLE_KEY"),
        anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"),
        anthropic_model=os.getenv("ANTHROPIC_MODEL", "claude-haiku-4-5-20251001"),
        ncbi_api_key=os.getenv("NCBI_API_KEY"),
        unpaywall_email=os.getenv("UNPAYWALL_EMAIL"),
        crossref_mailto=os.getenv("CROSSREF_MAILTO"),
        database_url=os.getenv("DATABASE_URL"),
        publication_mode=os.getenv("PUBLICATION_MODE", "auto_publish"),
        mvp_sources=_split_csv(os.getenv("MVP_SOURCES")),
        timezone=os.getenv("TZ", "Asia/Taipei"),
    )


def _load_dotenv(path: str = ".env") -> None:
    env_path = Path(path)
    if not env_path.exists():
        return

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()
        if (
            (value.startswith('"') and value.endswith('"'))
            or (value.startswith("'") and value.endswith("'"))
        ):
            value = value[1:-1]

        os.environ.setdefault(key, value)
