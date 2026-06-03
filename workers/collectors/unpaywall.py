from dataclasses import dataclass
from urllib.error import HTTPError
from urllib.parse import quote, urlencode
from urllib.request import urlopen
import json

from workers.shared.config import Settings


@dataclass(frozen=True)
class AccessStatus:
    access_status: str
    is_open_access: bool
    license: str | None = None
    best_oa_url: str | None = None
    oa_status: str | None = None
    raw_metadata: dict | None = None


class UnpaywallChecker:
    source_name = "Unpaywall"
    base_url = "https://api.unpaywall.org/v2"

    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def check(self, doi: str | None) -> AccessStatus:
        if not doi:
            return AccessStatus(access_status="ABSTRACT_ONLY", is_open_access=False)

        if not self.settings.unpaywall_email:
            return AccessStatus(access_status="UNKNOWN", is_open_access=False)

        params = urlencode({"email": self.settings.unpaywall_email})
        url = f"{self.base_url}/{quote(doi, safe='')}?{params}"

        try:
            with urlopen(url, timeout=30) as response:
                payload = json.loads(response.read().decode("utf-8"))
        except HTTPError as exc:
            if exc.code == 404:
                return AccessStatus(access_status="UNKNOWN", is_open_access=False)
            raise

        best_location = payload.get("best_oa_location") or {}
        is_oa = bool(payload.get("is_oa"))
        oa_status = payload.get("oa_status")

        return AccessStatus(
            access_status=_access_status(is_oa=is_oa, oa_status=oa_status),
            is_open_access=is_oa,
            license=best_location.get("license"),
            best_oa_url=best_location.get("url_for_pdf")
            or best_location.get("url")
            or best_location.get("url_for_landing_page"),
            oa_status=oa_status,
            raw_metadata={
                "is_oa": is_oa,
                "oa_status": oa_status,
                "best_oa_location": best_location,
            },
        )


def _access_status(is_oa: bool, oa_status: str | None) -> str:
    if is_oa:
        return "OPEN_ACCESS"
    if oa_status == "closed":
        return "INSTITUTIONAL_ACCESS_NEEDED"
    return "UNKNOWN"
