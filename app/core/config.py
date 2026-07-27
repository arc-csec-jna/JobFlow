from pydantic_settings import BaseSettings,SettingsConfigDict

class Settings(BaseSettings):
    MAX_WORKERS: int
    SCHEDULER_POLL_INTERVAL: int = 5
    SCHEDULER_ENABLED: bool=True

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()