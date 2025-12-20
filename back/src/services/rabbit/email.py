from faststream.rabbit.fastapi import RabbitRouter
from src.config import config
import logging
from pydantic import BaseModel, EmailStr
from enum import StrEnum


class TEMPLATES(StrEnum):
    LOGIN_CONFIRM_EMAIL = "login_confirm_email"
    REGISTER_CONFIRM_EMAIL = "register_confirm_email"
    WELLCOME_EMAIL = "wellcome"


class SimpleTask(BaseModel):
    to: EmailStr
    payload: dict
    text_name: str


logger = logging.getLogger(__name__)
router = RabbitRouter(config.rabbit.get_connection_path)


@router.publisher(config.rabbit.RABBIT_EMAIL_QUEUE)
async def email_publisher(task: SimpleTask):
    logger.info(
        "a message was sent to rabbit",
        extra={"email": task.to, "text_name": task.text_name},
    )
    return task
