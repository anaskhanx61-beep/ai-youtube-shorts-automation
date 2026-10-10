import os
from pathlib import Path


class Settings:
    def __init__(self) -> None:
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self.default_topic = os.getenv("DEFAULT_TOPIC", "AI productivity mistakes")
        self.output_dir = Path(os.getenv("OUTPUT_DIR", "output")).resolve()


def get_settings() -> Settings:
    return Settings()
