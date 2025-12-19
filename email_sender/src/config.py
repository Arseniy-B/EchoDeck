from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel
from src.templates.read import read_templates
from pathlib import Path


BASE_DIR = Path(__name__).parent.parent

class Email(BaseSettings):
    EMAIL_ADDRESS: str
    EMAIL_PASSWORD: str
    SMTP_SERVER: str

    TEMPLATES_DIR: Path = BASE_DIR / "src" / "templates"
    TEMPLATES: dict[str, str] = read_templates(TEMPLATES_DIR)

    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env", extra="allow")


class RabbitMQ(BaseSettings):
    RABBIT_HOST: str
    RABBIT_PORT: str
    RABBIT_USER: str
    RABBIT_PASS: str
    RABBIT_EMAIL_QUEUE: str

    @property
    def get_connection_path(self) -> str:
        return f"amqp://{self.RABBIT_USER}:{self.RABBIT_PASS}@{self.RABBIT_HOST}:{self.RABBIT_PORT}/"

    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env", extra="allow")


class Config(BaseModel):
    email: Email = Email() # pyright: ignore
    rabbit: RabbitMQ = RabbitMQ() # pyright: ignore

config = Config() 
