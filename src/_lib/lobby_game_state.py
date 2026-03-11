from enum import Enum


class LobbyGameState(Enum):
    LOBBY = 0
    INGAME = 1
    CLOSED = 2