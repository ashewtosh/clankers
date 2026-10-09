import asyncio
from clankers.core.http import HTTPClient
from clankers.core.types import Message, MessageRole
from clankers.llm.providers.ollama import OllamaProvider
from clankers.llm.types import LLMRequest

async def main() -> None:
    request = LLMRequest(
        model="qwen2.5:3b",
        messages=(
            Message(
                role=MessageRole.SYSTEM, content="You are a helpful assistant. You only respond in English."
            ),
            Message(
                role=MessageRole.USER, content="Explain how do I define binary search system in python!"
            )
        ),
    )

    async with HTTPClient(timeout=120.0) as client:
        llm = OllamaProvider(
            base_url="http://localhost:11434",
            client=client
        )

        async for chunk in llm.stream(request):
            print(chunk.content, end="", flush=True)
        print()

if __name__ == "__main__":
    asyncio.run(main())