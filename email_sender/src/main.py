from faststream.rabbit import RabbitRouter
from src.email_sender import email_sender
from src.config import config
from src.templates.read import TEMPLATES
from pydantic import BaseModel, EmailStr, ValidationError
from asyncio import create_task


router = RabbitRouter(config.rebbit.get_connection_path)


class Event(BaseModel):
    event_type: str
    to: EmailStr
    payload: dict


class ConfirmPayload(BaseModel):
    otp: str


TypesOfConfirmEmail = ["login_confirm_email", "register_confirm_email"]


async def confirm_email_task(msg: dict):
    try:
        event = Event.model_validate(msg)
    except ValidationError:
        return

    if event.event_type not in TypesOfConfirmEmail:
        return

    try:
        payload = ConfirmPayload.model_validate(event.payload)
    except ValidationError:
        return

    t = TEMPLATES[event.event_type]
    text = t.format(**payload.model_dump())
    await email_sender.send_message(event.to, text)


@router.subscriber(config.rebbit.REBBITMQ_EMAIL_QUEUE)
async def confirm_email(msg: dict):
    create_task(confirm_email_task(msg))
