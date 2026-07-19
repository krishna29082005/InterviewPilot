from app.ai.providers.gemini import GeminiProvider


class ProviderFactory:

    @staticmethod
    def get_provider(name: str):

        if name == "gemini":
            return GeminiProvider()

        raise ValueError(f"Unknown provider: {name}")