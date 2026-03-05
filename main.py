from fastapi import FastAPI
from lobby_manager import LobbyManager
from models.game_lobby import GameLobbyRead, GameLobbyCreate
from lobby_manager.game_lobby import GameLobby
from game_lobby_factory import to_model, from_model

app = FastAPI()
lobby_manager = LobbyManager()

@app.get("/")
async def root() -> list[GameLobbyRead]:
    lobby_list: list[GameLobbyRead] = []
    for lobby in lobby_manager.managed_lobbies.values():
        lobby_list.append(to_model(lobby))
    return lobby_list


@app.get("/details/{lobby_id}")
async def lobby_details(lobby_id: int):
    return {"message": f"Details for: {lobby_id}"}

@app.post("/lobbies/register")
async def register_lobby(lobby_model: GameLobbyCreate) -> int:
    lobby_instance: GameLobby = GameLobby.create_from_model(lobby_model)
    lobby_id: int = lobby_manager.add_lobby(lobby_instance)
    return lobby_id
