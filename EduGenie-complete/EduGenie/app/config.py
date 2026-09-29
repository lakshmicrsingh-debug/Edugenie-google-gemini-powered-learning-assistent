from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "EduGenie"
    app_version: str = "1.0.0"
    gemini_api_key: str = ""
    gemini_model: str = "gemini-2.5-flash"
    use_local_explainer: bool = False
    local_explainer_model: str = "MBZUAI/LaMini-Flan-T5-783M"
    max_input_chars: int = 12000
    max_summary_chars: int = 16000
    cors_origins: str = "*"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def cors_origin_list(self) -> list[str]:
        return [item.strip() for item in self.cors_origins.split(",") if item.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
