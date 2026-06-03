from urllib.error import HTTPError
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen
import json

from workers.shared.config import Settings
from workers.shared.models import CandidateArticle


class CrossrefEnricher:
    source_name = "Crossref"
    base_url = "https://api.crossref.org/works"

    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def enrich(self, article: CandidateArticle) -> CandidateArticle:
        return article

    def fetch_metadata(self, doi: str | None) -> dict:
        if not doi:
            return {}

        params = {}
        if self.settings.crossref_mailto:
            params["mailto"] = self.settings.crossref_mailto

        query = f"?{urlencode(params)}" if params else ""
        request = Request(
            f"{self.base_url}/{quote(doi, safe='')}{query}",
            headers={"User-Agent": self._user_agent()},
        )

        try:
            with urlopen(request, timeout=30) as response:
                payload = json.loads(response.read().decode("utf-8"))
                return payload.get("message", {})
        except HTTPError as exc:
            if exc.code == 404:
                return {}
            raise

    def _user_agent(self) -> str:
        email = self.settings.crossref_mailto or "unknown"
        return f"daily-medicine-paper-brief/0.1 (mailto:{email})"
