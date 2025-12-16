from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel
from src.templates.read import TEMPLATES
from pathlib import Path


BASE_DIR = Path(__name__).parent.parent

class Email(BaseSettings):
    EMAIL_ADDRESS: str
    EMAIL_PASSWORD: str
    SMTP_SERVER: str

    TEMPLATES: dict[str, str] = TEMPLATES

    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env", extra="allow")


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
    email: Email = Email() # pyright: ignore
    rebbit: RebbitMQ = RebbitMQ() # pyright: ignore

config = Config() 
