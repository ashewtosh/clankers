import asyncio
from clankers.config.settings import Settings
from clankers.core.types import Message, MessageRole
from clankers.llm.providers.nim import NIMProvider
from clankers.llm.types import LLMRequest

async def main() -> None:
    settings = Settings()

    llm = NIMProvider(
        api_key = settings.nim_api_key,
        base_url= settings.nim_base_url
    )

    request = LLMRequest(
        model=settings.nim_model,
        messages=(
            Message(
                role=MessageRole.SYSTEM,
                content="You are a helpful assistant.",
            ),
            Message(
                role=MessageRole.USER,
                content="Explain binary search in simple terms.",
            ),
        ),
    )
    response = await llm.generate(request)
    print(response.content)

if __name__ == "__main__":
    asyncio.run(main())