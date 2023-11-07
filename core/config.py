from pydantic_settings import BaseSettings, SettingsConfigDict
from datetime import timedelta


class Settings(BaseSettings):
    # JWT
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_EXPIRE_TIME: timedelta = timedelta(days=1)
    REFRESH_EXPIRE_TIME: timedelta = timedelta(days=30)

    # Redis
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int

    class Config:
        env_file = "/home/samane/Documents/MaktabSharif/FinalProject/Authorization-Microservice-FastAPI/.env"


settings = Settings()
