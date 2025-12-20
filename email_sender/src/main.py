from faststream import FastStream
from faststream.rabbit import RabbitBroker, RabbitQueue
from src.email_sender import email_sender
from src.config import config
from src.schemas import SimpleTask
from src.exceptions import TemplateMismatch, TemplateNameNotFound


broker = RabbitBroker(config.rabbit.get_connection_path)
app = FastStream(broker)



@broker.subscriber(queue=RabbitQueue(config.rabbit.RABBIT_EMAIL_QUEUE, durable=True))
async def simple_email_task(event: SimpleTask):
    if event.text_name not in config.email.TEMPLATES:
        raise TemplateNameNotFound()
    t = config.email.TEMPLATES[event.text_name]
    try:
        text = t.format(**event.payload)
    except KeyError:
        raise TemplateMismatch()
    await email_sender.send_message(event.to, text)
