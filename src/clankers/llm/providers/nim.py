from clankers.core.http import HTTPClient
from clankers.llm.types import LLMRequest, LLMResponse, LLMChunk
from collections.abc import AsyncIterator
import json

class NIMProvider:
    def __init__(self, api_key: str, base_url: str, client: HTTPClient) -> None:
        self.api_key = api_key
        self.base_url = base_url
        self.client = client

    async def generate(self, request: LLMRequest) -> LLMResponse:
        payload = {
            "model": request.model,
            "messages": [
                {
                    "role": message.role.value,
                    "content": message.content,
                } for message in request.messages
            ],
            "temperature": request.temperature
        }
        if request.max_tokens is not None:
            payload["max_tokens"] = request.max_tokens

        response = await self.client.post(
            f"{self.base_url}/chat/completions",
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            },
            json=payload
        )
        response.raise_for_status()

        data = response.json()
        return LLMResponse(
            content=data["choices"][0]["message"]["content"],
            model=data.get("model", request.model),
            raw=data
        )

    async def stream(self, request: LLMRequest) -> AsyncIterator[LLMChunk]:
        payload = {
            "model": request.model,
            "messages": [
                {"role": message.role.value, "content": message.content} for message in request.messages
            ],
            "temperature": request.temperature,
            "stream": True,
        }
        if request.max_tokens is not None:
            payload["max_tokens"] = request.max_tokens

        async with self.client.stream_post(
            f"{self.base_url}/chat/completions",
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            },
            json=payload
        ) as response:
            response.raise_for_status()
            async for line in response.aiter_lines():
                if not line:
                    continue
                if not line.startswith("data:"):
                    continue
                data = line[5:].strip()
                if data == "[DONE]":
                    yield LLMChunk(
                        content="",
                        model=request.model,
                        done=True
                    )
                    break
                chunk = json.loads(data)
                choice = chunk["choices"][0]
                delta = choice.get("delta", {})

                yield LLMChunk(
                    content=delta.get("content", ""),
                    model=chunk.get("model", request.model),
                    done=choice.get("finish_reason") is not None,
                    raw=chunk
                )