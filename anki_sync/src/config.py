from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel
from pathlib import Path


BASE_DIR = Path(__name__).parent.parent

class RabbitMQ(BaseSettings):
    RABBIT_HOST: str
    RABBIT_PORT: str
    RABBIT_USER: str
    RABBIT_PASS: str
    RABBIT_EMAIL_QUEUE: str

    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env", extra="allow")

    @property
    def get_connection_path(self) -> str:
        return f"amqp://{self.RABBIT_USER}:{self.RABBIT_PASS}@{self.RABBIT_HOST}:{self.RABBIT_PORT}/"


class Config(BaseModel):
    rabbit: RabbitMQ = RabbitMQ() # pyright: ignore


config = Config()
