from urllib.parse import urlencode
from urllib.error import HTTPError
from urllib.request import Request, urlopen
import json


class SupabaseRestClient:
    def __init__(self, supabase_url: str, secret_key: str) -> None:
        self.base_url = supabase_url.rstrip("/")
        self.secret_key = secret_key

    def get(self, table: str, params: dict[str, str]) -> list[dict]:
        url = f"{self.base_url}/rest/v1/{table}?{urlencode(params)}"
        request = Request(url, headers=self._headers())
        return self._send(request)

    def insert(self, table: str, payload: dict, returning: bool = True) -> list[dict]:
        url = f"{self.base_url}/rest/v1/{table}"
        headers = self._headers()
        headers["Prefer"] = "return=representation" if returning else "return=minimal"
        request = Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
            method="POST",
        )
        return self._send(request)

    def upsert(
        self,
        table: str,
        payload: dict,
        on_conflict: str,
        returning: bool = True,
    ) -> list[dict]:
        url = f"{self.base_url}/rest/v1/{table}?{urlencode({'on_conflict': on_conflict})}"
        headers = self._headers()
        headers["Prefer"] = (
            "resolution=merge-duplicates,return=representation"
            if returning
            else "resolution=merge-duplicates,return=minimal"
        )
        request = Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
            method="POST",
        )
        return self._send(request)

    def patch(
        self,
        table: str,
        filters: dict[str, str],
        payload: dict,
        returning: bool = False,
    ) -> list[dict]:
        url = f"{self.base_url}/rest/v1/{table}?{urlencode(filters)}"
        headers = self._headers()
        headers["Prefer"] = "return=representation" if returning else "return=minimal"
        request = Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
            method="PATCH",
        )
        return self._send(request)

    def upload_storage_object(
        self,
        bucket: str,
        object_path: str,
        data: bytes,
        content_type: str,
        upsert: bool = True,
    ) -> str:
        url = f"{self.base_url}/storage/v1/object/{bucket}/{object_path}"
        headers = self._headers()
        headers["Content-Type"] = content_type
        headers["Cache-Control"] = "3600"
        if upsert:
            headers["x-upsert"] = "true"
        request = Request(
            url,
            data=data,
            headers=headers,
            method="POST",
        )
        self._send(request)
        return f"{self.base_url}/storage/v1/object/public/{bucket}/{object_path}"

    def _headers(self) -> dict[str, str]:
        return {
            "apikey": self.secret_key,
            "Authorization": f"Bearer {self.secret_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def _send(self, request: Request) -> list[dict]:
        try:
            with urlopen(request, timeout=30) as response:
                body = response.read().decode("utf-8")
                if not body:
                    return []
                parsed = json.loads(body)
                return parsed if isinstance(parsed, list) else [parsed]
        except HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"Supabase REST error {exc.code}: {body}") from exc
