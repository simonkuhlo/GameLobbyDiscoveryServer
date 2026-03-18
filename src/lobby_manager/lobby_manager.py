from typing import Optional

from lobby_manager.health_monitor import HealthMonitor
from .filters.lobby_filter import LobbyFilter
from .game_lobby import ManagedGameLobby, GameLobby
from _project import settings, logger


class LobbyManager:
    def __init__(self) -> None:
        self._id_index: int = 0
        self.managed_lobbies: dict[int, ManagedGameLobby] = {}
        if settings.health_check.enabled:
            self.health_monitor = HealthMonitor(self)

    @property
    def id_index(self) -> int:
        return self._id_index

    @id_index.setter
    def id_index(self, new_value: int) -> None:
        if new_value > settings.lobby_manager.max_index:
            message: str = "Tried to set the lobby id index to a higher number than allowed."
            logger.log_error(message)
            raise Exception(message)
        self._id_index = new_value

    def _check_lobby_health_on_request(self, lobby: ManagedGameLobby) -> bool:
        if not settings.health_check.enabled:
            return True
        if not settings.health_check.on_request:
            return True
        if self.health_monitor.check_lobby_health(lobby):
            return True
        return False

    def get_lobby(self, lobby_id: int) -> ManagedGameLobby:
        lobby = self.managed_lobbies.get(lobby_id)
        if not self._check_lobby_health_on_request(lobby):
            lobby = None
        if not lobby:
            message: str = "Tried to fetch a lobby with non existing ID."
            logger.log_error(message)
            raise Exception(message)
        return lobby

    def get_all_lobbies(self) -> list[ManagedGameLobby]:
        return list(self.managed_lobbies.values())

    def get_lobbies(self, lobby_filter: Optional[LobbyFilter] = None) -> list[ManagedGameLobby]:
        returned_lobbies = []
        for lobby in self.get_all_lobbies():
            if lobby_filter:
                if lobby_filter.check(lobby):
                    continue
            if not self._check_lobby_health_on_request(lobby):
                continue
            returned_lobbies.append(lobby)
        return returned_lobbies

    def add_lobby(self, lobby: GameLobby) -> ManagedGameLobby:
        if len(self.managed_lobbies) >= settings.lobby_manager.max_lobbies:
            message: str = "Tried to add a Lobby but configured maximum is already reached."
            logger.log_error(message)
            raise Exception(message)
        if lobby in self.managed_lobbies.values():
            message: str = "Tried to add a Lobby that is already managed by this manager."
            logger.log_error(message)
            raise Exception(message)
        self.id_index += 1
        lobby_id = self.id_index
        self.managed_lobbies[lobby_id] = ManagedGameLobby(lobby, lobby_id)
        logger.log_info(f"Added lobby {lobby.name} to the monitored lobbies pool.")
        return self.managed_lobbies[lobby_id]

    def remove_lobby(self, lobby_id: int) -> None:
        lobby: ManagedGameLobby = self.managed_lobbies.pop(lobby_id, None)
        logger.log_info(f"Removed lobby {lobby.name} from the monitored lobbies pool.")

    def clear(self) -> None:
        logger.log_info("Clearing lobby manager...")
        for lobby_id in self.managed_lobbies.keys():
            self.remove_lobby(lobby_id)
        self.id_index = 0
        logger.log_info("Lobby manager successfully cleared.")