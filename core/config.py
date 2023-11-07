from pydantic_settings import BaseSettings, SettingsConfigDict
from datetime import timedelta


class Settings(BaseSettings):
    # JWT
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_EXPIRE_TIME = timedelta(days=1)
    REFRESH_EXPIRE_TIME = timedelta(days=30)


settings = Settings()
