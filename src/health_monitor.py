import time
import asyncio
from lobby_manager.game_lobby import ManagedGameLobby
from lobby_manager.lobby_manager import LobbyManager
from _project import logger

class HealthMonitor:
    def __init__(self, lobby_manager: LobbyManager, interval: float = 15, max_heartbeat_interval: float = 30) -> None:
        self.lobby_manager: LobbyManager = lobby_manager
        self.interval: float = interval
        self.max_heartbeat_interval: float = max_heartbeat_interval
        loop = asyncio.get_event_loop()
        loop.create_task(self.run())

    async def on_lobby_health_check_failed(self, lobby: ManagedGameLobby) -> None:
        logger.log_info(f"Removing broken lobby from lobby manager:  [{lobby.lobby_id}]{lobby.name}")
        self.lobby_manager.remove_lobby(lobby.lobby_id)

    async def check_lobby_health(self, lobby: ManagedGameLobby) -> None:
        logger.log_debug(f"Starting scheduled health check for a specific lobby: [{lobby.lobby_id}]{lobby.name}")
        if lobby.last_heartbeat + self.max_heartbeat_interval < time.time():
            await self.on_lobby_health_check_failed(lobby)

    async def check_all_lobbies(self) -> None:
        logger.log_info("Starting scheduled health check for all registered lobbies...")
        tasks = [asyncio.create_task(self.check_lobby_health(lobby)) for lobby in self.lobby_manager.get_lobbies()]
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)

    async def run(self) -> None:
        while True:
            await asyncio.sleep(self.interval)
            await self.check_all_lobbies()