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


class EmailSettings(BaseSettings):
    EMAIL_ADDRESS: str
    EMAIL_PASSWORD: str
    SMTP_SERVER: str

    def get_otp_content(self, otp) -> str:
        return f"Your login code: {otp}"

    def get_welcome_content(self) -> str:
        return "welcome"

    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env", extra="allow")


class RedisSettings(BaseSettings):
    REDIS_HOST: str
    REDIS_PORT: str

    @property
    def get_url(self):
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/0"

    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env", extra="allow")


class Config(BaseModel):
    db: PostgresSettings = PostgresSettings() # pyright: ignore
    jwt: JWT = JWT()
    email: EmailSettings = EmailSettings() # pyright: ignore
    redis: RedisSettings = RedisSettings() # pyright: ignore


config = Config()
