import time
from datetime import datetime
import asyncio
from _project import logger, settings
from typing import TYPE_CHECKING, Optional
if TYPE_CHECKING:
    from lobby_manager.game_lobby import ManagedGameLobby
    from lobby_manager.lobby_manager import LobbyManager

class HealthMonitor:
    def __init__(self, parent_lobby_manager: "LobbyManager") -> None:
        self.parent_lobby_manager: "LobbyManager" = parent_lobby_manager
        if settings.health_check.periodic_check:
            loop = asyncio.get_event_loop()
            loop.create_task(self.run())

    async def on_lobby_health_check_failed(self, lobby: "ManagedGameLobby") -> None:
        logger.log_info(f"Removing broken lobby from lobby manager:  [{lobby.lobby_id}]{lobby.name}")
        self.parent_lobby_manager.remove_lobby(lobby.lobby_id)

    async def check_lobby_health(self, lobby: "ManagedGameLobby") -> bool:
        logger.log_debug(f"Starting health check for a specific lobby: [{lobby.lobby_id}]{lobby.name}")
        deadline: float = lobby.last_heartbeat + settings.health_check.heartbeat_frequency_sec + settings.health_check.heartbeat_grace_period_sec
        logger.log_debug(f"[{lobby.lobby_id}]{lobby.name}: "
                         f"Last heartbeat: {datetime.fromtimestamp(lobby.last_heartbeat)}\n"
                         f"Deadline: {datetime.fromtimestamp(deadline)}\n"
                         f"Current time: {datetime.fromtimestamp(time.time())}")
        if deadline < time.time():
            await self.on_lobby_health_check_failed(lobby)
            return False
        return True

    async def check_all_lobbies(self) -> None:
        logger.log_info("Starting scheduled health check for all registered lobbies...")
        tasks = [asyncio.create_task(self.check_lobby_health(lobby)) for lobby in self.parent_lobby_manager.get_lobbies()]
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)

    async def run(self) -> None:
        while True:
            await asyncio.sleep(settings.health_check.periodic_check_frequency_sec)
            await self.check_all_lobbies()