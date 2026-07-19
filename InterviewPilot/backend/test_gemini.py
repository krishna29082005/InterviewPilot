import asyncio

from app.ai.providers.factory import ProviderFactory


async def main():
    provider = ProviderFactory.get_provider("gemini")

    response = await provider.generate(
        "Reply with exactly: Hello Krishna!"
    )

    print(response)


asyncio.run(main())