from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file="../.env")

    anthropic_api_key: str
    voyage_api_key: str
    max_tokens: int
    model: str = "claude-sonnet-4-5"
    request_timeout: float = 30.0
    log_level: str = "INFO"
    

settings = Settings()