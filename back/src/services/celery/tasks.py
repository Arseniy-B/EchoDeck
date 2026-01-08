from celery import Celery
from src.config import config


celery_app = Celery(
    __name__, backend=config.redis.get_url, broker=config.rabbit.get_connection_path
)

celery_app.conf.update(task_serializer="json", result_serializer="json")


anki_url_downloads = "https://ankiweb.net/svc/shared/download-deck/{deck_id}"


@celery_app.task
def import_anki_deck(deck_id: int) -> int: ...

