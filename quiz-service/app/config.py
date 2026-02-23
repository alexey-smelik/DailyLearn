from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ollama_base_url: str = "http://ollama:11434"
    ollama_default_model: str = "phi3:mini"
    ollama_timeout: float = 120.0
    ollama_max_retries: int = 3
    ollama_retry_min_wait: float = 2.0
    ollama_retry_max_wait: float = 30.0

    web_api_url: str = "http://web-api:8000"

    # text chunking
    max_chunk_size: int = 3000
    chunk_overlap: int = 200

    log_level: str = "INFO"

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()
