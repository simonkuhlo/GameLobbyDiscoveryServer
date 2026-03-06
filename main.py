from fastapi import FastAPI
from game_lobby_crud import router as game_lobby_crud_router

app = FastAPI()

app.include_router(game_lobby_crud_router)