from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException

from src.api.utils.depends import AuthDep, ScheduleDep


router = APIRouter(prefix="/schedule")


@router.post("/learn/{deck_id}")
async def start_learn(auth: AuthDep, Schedule: ScheduleDep, collection_id: int):
    user_id = auth.is_authorized()
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    await Schedule.add_to_learn(user_id, collection_id)


@router.get("/")
async def get_current_schedule():
    ...


@router.post("/result")
async def put_results():
    ...

