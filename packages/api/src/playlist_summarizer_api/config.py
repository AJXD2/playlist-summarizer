from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)

    ollama_host: str | None = None
    ollama_api_key: str | None = None
    default_model: str = "gemma3:4b"


settings = Settings()
