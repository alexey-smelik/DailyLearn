from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/dailylearn"
    tg_tool_url: str = "http://tg-tool:8001"

    # How often the scheduler checks for due cards (minutes)
    check_interval_minutes: int = 60


settings = Settings()
