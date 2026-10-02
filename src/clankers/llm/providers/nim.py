from clankers.core.http import HTTPClient
from clankers.llm.types import LLMRequest, LLMResponse


class NIMProvider:
    def __init__(
        self,
        api_key: str,
        base_url: str,
        client: HTTPClient,
    ) -> None:
        self._api_key = api_key
        self._base_url = base_url
        self._client = client

    async def generate(
        self,
        request: LLMRequest,
    ) -> LLMResponse:
        payload = {
            "model": request.model,
            "messages": [
                {
                    "role": message.role.value,
                    "content": message.content,
                }
                for message in request.messages
            ],
            "temperature": request.temperature,
        }

        if request.max_tokens is not None:
            payload["max_tokens"] = request.max_tokens

        response = await self._client.post(
            f"{self._base_url}/chat/completions",
            headers={
                "Authorization": f"Bearer {self._api_key}",
                "Content-Type": "application/json",
            },
            json=payload,
        )

        response.raise_for_status()

        data = response.json()

        return LLMResponse(
            content=data["choices"][0]["message"]["content"],
            model=data.get("model", request.model),
            raw=data,
        )
