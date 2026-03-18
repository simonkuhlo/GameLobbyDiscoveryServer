from typing import Optional
from _lib.lobby_game_state import LobbyGameState
from lobby_manager.game_lobby import ManagedGameLobby


class LobbyFilter:
    def check(self, lobby: ManagedGameLobby) -> bool:
        return True

class LobbyFilterCollection:
    def __init__(self, filters: list[LobbyFilter]) -> None:
        self.filters: list[LobbyFilter] = filters

    def check(self, lobby: ManagedGameLobby) -> bool:
        for lobby_filter in self.filters:
            if not lobby_filter.check(lobby):
                return False
        return True

class LobbyGameStateFilter(LobbyFilter):
    def __init__(self,
                 allowed_game_states: Optional[list[LobbyGameState]],
                 disallowed_game_states: Optional[list[LobbyGameState]]
                 ) -> None:
        self.allowed_game_states = allowed_game_states
        self.disallowed_game_states = disallowed_game_states

    def check(self, lobby: ManagedGameLobby) -> bool:
        if self.allowed_game_states:
            if lobby.game_state not in self.allowed_game_states:
                return False
        if self.disallowed_game_states:
            if lobby.game_state in self.disallowed_game_states:
                return False
        return True
