from typing import Protocol
from clankers.llm.types import LLMRequest, LLMResponse

class LLMProvider(Protocol):
    async def generate(
            self,
            request: LLMRequest
    ) -> LLMResponse:
        ...