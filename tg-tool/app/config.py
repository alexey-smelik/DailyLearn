from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    bot_token: str
    web_api_url: str = "http://web-api:8000"
    host: str = "0.0.0.0"
    port: int = 8001


settings = Settings()
