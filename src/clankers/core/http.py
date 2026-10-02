import httpx


class HTTPClient:
    def __init__(
        self,
        *,
        timeout: float = 120.0,
    ) -> None:
        self._client = httpx.AsyncClient(timeout=timeout)

    async def post(
        self,
        url: str,
        *,
        headers: dict[str, str] | None = None,
        json: dict | None = None,
    ) -> httpx.Response:
        return await self._client.post(
            url,
            headers=headers,
            json=json,
        )

    async def close(self) -> None:
        await self._client.aclose()

    async def __aenter__(self) -> "HTTPClient":
        return self

    async def __aexit__(self, *args: object) -> None:
        await self.close()
