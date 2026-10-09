from typing import Protocol
from clankers.llm.types import LLMRequest, LLMResponse, LLMChunk
from collections.abc import AsyncIterator

class LLMProvider(Protocol):
    async def generate(
            self,
            request: LLMRequest
    ) -> LLMResponse:
        ...

    def stream(self, request: LLMRequest) -> AsyncIterator[LLMChunk]:
        ...