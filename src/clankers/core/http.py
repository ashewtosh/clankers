from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
import httpx

class HTTPClient:
    def __init__(self, *, timeout: float = 120.0) -> None:
        self.client = httpx.AsyncClient(timeout= timeout)

    async def post(self, url: str, *, headers: dict[str, str] | None = None, json: dict | None = None) -> httpx.Response:
        return await self.client.post(url, headers = headers, json = json)

    @asynccontextmanager
    async def stream_post(self, url: str, *, headers: dict[str, str] | None = None, json: dict | None = None) -> AsyncIterator[httpx.response]:
        async with self.client.stream("POST", url, headers=headers, json=json) as response:
            yield response
    
    async def close(self) -> None:
        return await self.client.aclose()

    async def __aenter__(self) -> "HTTPClient":
        return self

    async def __aexit__(self, *args: object) -> None:
        await self.close()