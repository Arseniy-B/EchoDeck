from faststream import FastStream
from faststream.rabbit import RabbitBroker, RabbitQueue
from src.config import config


broker = RabbitBroker(config.rabbit.get_connection_path)
app = FastStream(broker)



@broker.subscriber(queue=RabbitQueue(config.rabbit.RABBIT_EMAIL_QUEUE, durable=True))
async def import_apkg(msg):
    ...


@broker.subscriber(queue=RabbitQueue(config.rabbit.RABBIT_EMAIL_QUEUE, durable=True))
async def export_apkg(msg):
    ...
