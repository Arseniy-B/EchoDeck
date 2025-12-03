from pydantic_settings import SettingsConfigDict, BaseSettings
from pydantic import BaseModel
from pathlib import Path


BASE_DIR = Path(__file__).parent.parent


class PostgresSettings(BaseSettings):
    POSTGRES_PASS: str
    POSTGRES_USER: str
    POSTGRES_DB: str
    POSTGRES_PORT: str
    POSTGRES_HOST: str

    db_echo: bool = True

    @property
    def DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASS}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"


    model_config = SettingsConfigDict(env_file=BASE_DIR.parent / ".env", extra="allow")


class Config(BaseModel):
    db: PostgresSettings = PostgresSettings() # pyright: ignore


config = Config()
