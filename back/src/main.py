from fastapi import FastAPI
from src.endpoints.auth import router as AuthRouter


app = FastAPI()
app.include_router(router=AuthRouter)

