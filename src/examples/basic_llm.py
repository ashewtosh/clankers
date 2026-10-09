import asyncio
from clankers.config.settings import Settings
from clankers.core.http import HTTPClient
from clankers.core.types import Message, MessageRole
from clankers.llm.providers.nim import NIMProvider
from clankers.llm.providers.ollama import OllamaProvider
from clankers.llm.types import LLMRequest

async def main() -> None:
    settings = Settings()
    async with HTTPClient(timeout=120.0) as client:
        llm = NIMProvider(
            api_key = settings.nim_api_key,
            base_url= settings.nim_base_url,
            client=client
        )
        local_llm = OllamaProvider(
            base_url="http://localhost:11434",
            client=client
        )

        request = LLMRequest(
            model=settings.ollama_model,
            messages=(
                Message(
                    role=MessageRole.SYSTEM,
                    content="You are a helpful assistant. You respond only in English.",
                ),
                Message(
                    role=MessageRole.USER,
                    content="how does http and tls packaging work in a server client communication",
                ),
            ),
        )
        response = await local_llm.generate(request)
        print(response.content)

if __name__ == "__main__":
    asyncio.run(main())