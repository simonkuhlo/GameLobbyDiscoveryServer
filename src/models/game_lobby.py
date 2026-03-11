from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from _lib.lobby_game_state import LobbyGameState

class GameLobbyBaseModel(BaseModel):
    name: str = Field(default="Unnamed Lobby")
    desc: str = Field(default="")
    port: int
    address: str
    max_players: int
    current_players: int
    game_state: LobbyGameState

class Authorization(BaseModel):
    secret_key: str

class LobbyAction(BaseModel):
    lobby_id: int

class AuthorizedAction(LobbyAction, Authorization):
    pass

class GameLobbyCreate(GameLobbyBaseModel, Authorization):
    pass

class GameLobbyRead(LobbyAction, GameLobbyBaseModel):
    pass

class GameLobbyDelete(AuthorizedAction):
    pass

class PartialGameLobbyUpdate(AuthorizedAction, GameLobbyBaseModel):
    model_config = ConfigDict(extra="forbid")  # Strict beyond these fields

    name: Optional[str] = Field(default=None)
    desc: Optional[str] = Field(default=None)
    port: Optional[int] = Field(default=None)
    address: Optional[str] = Field(default=None)
    max_players: Optional[int] = Field(default=None)
    current_players: Optional[int] = Field(default=None)
    game_state: Optional[LobbyGameState] = Field(default=None)
