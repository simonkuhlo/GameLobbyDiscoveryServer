from fastapi import APIRouter, HTTPException, status
from typing import List
from lobby_manager.game_lobby import ManagedGameLobby
from lobby_manager.lobby_manager import LobbyManager
from models.game_lobby import GameLobbyCreate, GameLobbyRead, GameLobbyDelete, PartialGameLobbyUpdate, RegisterResponse, AuthorizedAction
from model_translation_layer.game_lobby import instance_from_create_model, read_model_from_managed_instance, update_game_lobby_with_model
from _project import settings

lobby_manager = LobbyManager()

async def get_lobby(lobby_id: int) -> ManagedGameLobby:
    try:
        lobby = lobby_manager.get_lobby(lobby_id)
    except Exception as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(e))
    return lobby


async def verify_authorization(lobby: ManagedGameLobby, secret_key:str):
    if secret_key != lobby.secret_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid secret key"
        )


router = APIRouter(prefix="/lobbies", tags=["lobbies"])


@router.post("/", response_model=RegisterResponse)
async def create_lobby(lobby: GameLobbyCreate) -> RegisterResponse:
    """Create a new game lobby."""
    lobby_instance = instance_from_create_model(lobby)
    managed_instance = lobby_manager.add_lobby(lobby_instance)
    read_model: GameLobbyRead = read_model_from_managed_instance(managed_instance)
    response: RegisterResponse = RegisterResponse(
        lobby_object = read_model,
        heartbeat_freq = settings.health_check.heartbeat_frequency_sec
    )
    return response

@router.post("/heartbeat")
async def heartbeat(action: AuthorizedAction):
    lobby = await get_lobby(action.lobby_id)
    await verify_authorization(lobby, action.secret_key)
    lobby.heartbeat()
    return {"message" : "OK"}

@router.get("/", response_model=List[GameLobbyRead])
async def list_lobbies():
    """List all game lobbies."""
    managed_lobbies = lobby_manager.get_lobbies()
    returned_models: list[GameLobbyRead] = []
    for lobby in managed_lobbies:
        returned_models.append(read_model_from_managed_instance(lobby))
    return returned_models

@router.get("/{lobby_id}", response_model=GameLobbyRead)
async def read_lobby(lobby_id: int):
    """Read a specific game lobby."""
    lobby = await get_lobby(lobby_id)
    return read_model_from_managed_instance(lobby)

@router.patch("/", response_model=dict)
async def partial_update_lobby(
        action: PartialGameLobbyUpdate
):
    """Partially update a game lobby (authorized)."""
    lobby = await get_lobby(action.lobby_id)
    await verify_authorization(lobby, action.secret_key)
    update_game_lobby_with_model(lobby, action)
    return read_model_from_managed_instance(lobby)

@router.delete("/", response_model=dict)
async def delete_lobby(action: GameLobbyDelete):
    """Delete a game lobby (authorized)."""
    lobby = await get_lobby(action.lobby_id)
    await verify_authorization(lobby, action.secret_key)
    lobby_manager.remove_lobby(action.lobby_id)
    return {"message": "Lobby deleted!"}

