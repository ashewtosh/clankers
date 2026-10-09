from clankers.core.http import HTTPClient
from clankers.llm.types import LLMRequest, LLMResponse, LLMChunk
import json
from collections.abc import AsyncIterator

class OllamaProvider:
    def __init__(self, base_url: str, client: HTTPClient) -> None:
        self.base_url = base_url
        self.client = client

    async def generate(self, request: LLMRequest) -> LLMResponse:
        payload = {
            "model": request.model,
            "messages": [
                {"role": message.role.value, "content": message.content} for message in request.messages
            ],
            "stream": False
        }
        if request.temperature != 0.0:
            payload["options"] = {
                "temperature": request.temperature
            }
        if request.max_tokens is not None:
            payload.setdefault("options", {})["num_predict"] = request.max_tokens

        response = await self.client.post(
            f"{self.base_url}/api/chat",
            json=payload
        )
        response.raise_for_status()
        data = response.json()
        return LLMResponse(
            content=data["message"]["content"],
            model=data.get("model", request.model),
            raw=data
        )
    async def stream(self, request: LLMRequest) -> AsyncIterator[LLMChunk]:
        payload = {
            "model": request.model,
            "messages": [
                {"role": message.role.value, "content": message.content} for message in request.messages
            ],
            "stream": True,
        }
        if request.temperature != 0.0:
            payload["options"] = {
                "temperature": request.temperature
            }
        if request.max_tokens is not None:
            payload.setdefault("options", {})["num_predict"] = request.max_tokens

        async with self.client.stream_post(f"{self.base_url}/api/chat", json=payload) as response:
            response.raise_for_status()
            async for line in response.aiter_lines():
                if not line:
                    continue
                data = json.loads(line)

                yield LLMChunk(
                    content=data.get("message", {}).get("content", ""),
                    model=data.get("model", request.model),
                    done=data.get("done", False),
                    raw=data
                )