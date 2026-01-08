from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse
from src.services.celery.tasks import import_anki_deck

from celery.result import AsyncResult
from src.services.celery.tasks import celery_app
 

router = APIRouter(prefix="/collection")


@router.post("/import/anki/")
async def import_deck(collection_id: int = Body(...)):
    res = import_anki_deck.apply_async(args=(collection_id, ), task_id=str(collection_id))
    return JSONResponse({"success_start": not res.failed})


@router.get("/import/anki/status/{collection_id}")
async def import_deck_status(collection_id: int):
    res = AsyncResult(str(collection_id), app=celery_app)
    return JSONResponse({"status": res.status})
