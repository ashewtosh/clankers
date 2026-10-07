from clankers.core.http import HTTPClient
from clankers.llm.types import LLMRequest, LLMResponse


class OllamaProvider:
    def __init__(
        self,
        base_url: str,
        client: HTTPClient,
    ) -> None:
        self._base_url = base_url.rstrip("/")
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
            "stream": False,
        }

        if request.temperature != 0.0:
            payload["options"] = {
                "temperature": request.temperature,
            }

        if request.max_tokens is not None:
            payload.setdefault("options", {})["num_predict"] = request.max_tokens

        response = await self._client.post(
            f"{self._base_url}/api/chat",
            json=payload,
        )

        response.raise_for_status()

        data = response.json()

        return LLMResponse(
            content=data["message"]["content"],
            model=data.get("model", request.model),
            raw=data,
        )
