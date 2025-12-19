from faststream import FastStream
from faststream.rabbit import RabbitBroker, RabbitQueue
from src.email_sender import email_sender
from src.config import config
from pydantic import BaseModel, EmailStr, ValidationError


broker = RabbitBroker(config.rabbit.get_connection_path)
app = FastStream(broker)



class Event(BaseModel):
    event_type: str
    to: EmailStr
    payload: dict


class ConfirmPayload(BaseModel):
    otp: str


TypesOfConfirmEmail = ["login_confirm_email", "register_confirm_email"]


@broker.subscriber(queue=RabbitQueue(config.rabbit.RABBIT_EMAIL_QUEUE, durable=True))
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

    t = config.email.TEMPLATES[event.event_type]
    text = t.format(**payload.model_dump())
    await email_sender.send_message(event.to, text)

