from time import time
from _lib.lobby_game_state import LobbyGameState

class GameLobby:
    def __init__(self,
                 secret_key: str,
                 port: int,
                 address: str,
                 max_players: int,
                 current_players: int,
                 game_state: LobbyGameState,
                 name: str = "Game Lobby",
                 desc: str = ""
                 ):
        self.secret_key: str = secret_key
        self.port: int = port
        self.address: str = address
        self.max_players: int = max_players
        self.current_players: int = current_players
        self.game_state: LobbyGameState = game_state
        self.name: str = name
        self.desc: str = desc
        self.last_heartbeat: float = time()

    def heartbeat(self) -> None:
        self.last_heartbeat = time()

class ManagedGameLobby(GameLobby):
    def __init__(self,
                 lobby: GameLobby,
                 lobby_id: int
                 ):
        self.lobby_id: int = lobby_id
        super().__init__(
            secret_key = lobby.secret_key,
            port = lobby.port,
            address = lobby.address,
            max_players = lobby.max_players,
            current_players = lobby.current_players,
            game_state = lobby.game_state,
            name = lobby.name,
            desc = lobby.desc
        )