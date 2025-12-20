from fastapi import FastAPI
from src.api.auth import router as AuthRouter
from fastapi.middleware.cors import CORSMiddleware
from src.services.rabbit.email import router as EmailRabbitRouter


app = FastAPI()

origins = [
    "http://127.0.0.1",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router=AuthRouter)
app.include_router(router=EmailRabbitRouter)
