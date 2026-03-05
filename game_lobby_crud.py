from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from lobby_manager.lobby_manager import LobbyManager
from models.game_lobby import (
    Authorization, GameLobbyCreate, GameLobbyRead, GameLobbyDelete, PartialGameLobbyUpdate
)
from lobby_manager.game_lobby import GameLobby
from model_translation_layer.game_lobby import instance_from_create_model, read_model_from_managed_instance, update_game_lobby_with_model

lobby_manager = LobbyManager()


# Dependency to verify secret_key (simple API key auth)
async def verify_authorization(auth: Authorization):
    # In production, validate against DB or secret service
    if not auth.secret_key or auth.secret_key != "your_secret_key":  # Replace with real validation
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid secret_key"
        )
    return auth


router = APIRouter(prefix="/lobbies", tags=["lobbies"])


@router.post("/", response_model=dict)
async def create_lobby(lobby: GameLobbyCreate) -> GameLobbyRead:
    """Create a new game lobby."""
    lobby_instance = instance_from_create_model(lobby)
    managed_instance = lobby_manager.add_lobby(lobby_instance)
    return read_model_from_managed_instance(managed_instance)

@router.get("/", response_model=List[dict])
async def list_lobbies():
    """List all game lobbies."""
    managed_lobbies = lobby_manager.get_lobbies()


@router.get("/{lobby_id}", response_model=dict)
async def read_lobby(lobby_id: int):
    """Read a specific game lobby."""


@router.patch("/{lobby_id}", response_model=dict)
async def partial_update_lobby(
        lobby_id: int,
        update_data: PartialGameLobbyUpdate = Depends()
):
    """Partially update a game lobby (authorized)."""
    lobby = lobby_manager.get_lobby()



@router.delete("/{lobby_id}")
async def delete_lobby(action: GameLobbyDelete = Depends()):
    """Delete a game lobby (authorized)."""

