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


    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env", extra="allow")


class JWT(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_minutes: int = 60 * 24 * 30



class RedisSettings(BaseSettings):
    REDIS_HOST: str
    REDIS_PORT: str

    @property
    def get_url(self):
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/0"

    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env", extra="allow")


class Otp(BaseSettings):
    expire_minutes: int = 5


class RebbitMQ(BaseSettings):
    REBBITMQ_HOST: str
    REBBITMQ_PORT: str
    REBBITMQ_USER: str
    REBBITMQ_PASS: str
    REBBITMQ_EMAIL_QUEUE: str

    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env", extra="allow")

    @property
    def get_connection_path(self) -> str:
        return "amqp://user:pass@host:port/"


class Config(BaseModel):
    db: PostgresSettings = PostgresSettings() # pyright: ignore
    jwt: JWT = JWT()
    redis: RedisSettings = RedisSettings() # pyright: ignore
    otp: Otp = Otp()


config = Config()
