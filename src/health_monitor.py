import aiohttp
import asyncio
from lobby_manager.game_lobby import ManagedGameLobby
from lobby_manager.lobby_manager import LobbyManager
from _project import logger

async def send_health_check(address: str, timeout_secs: float = 3.0) -> None:
    timeout = aiohttp.ClientTimeout(total=timeout_secs)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.get(address) as response:
            if response.status != 200:
                raise ValueError(f"Health check failed with status {response.status}")

class HealthMonitor:
    def __init__(self, lobby_manager: LobbyManager, interval: float = 15, timeout: float = 3) -> None:
        self.lobby_manager: LobbyManager = lobby_manager
        self.interval: float = interval
        self.health_check_timeout: float = timeout
        self.task_timeout: float = self.health_check_timeout + 1.0
        loop = asyncio.get_event_loop()
        loop.create_task(self.run())

    async def on_lobby_failed_health_check(self, lobby: ManagedGameLobby) -> None:
        logger.log_info(f"Removing broken lobby from lobby manager:  [{lobby.lobby_id}]{lobby.name}")
        self.lobby_manager.remove_lobby(lobby.lobby_id)

    async def check_lobby_connectivity(self, lobby: ManagedGameLobby) -> None:
        logger.log_debug(f"Starting scheduled health check for a specific lobby: [{lobby.lobby_id}]{lobby.name}")
        try:
            await asyncio.wait_for(send_health_check(lobby.address, self.health_check_timeout), timeout=self.task_timeout)
        except (asyncio.TimeoutError, aiohttp.ClientError, ValueError) as e:
            logger.log_info(f"Health check failed for lobby [{lobby.lobby_id}]{lobby.name}: {str(e)}")
            await self.on_lobby_failed_health_check(lobby)

    async def check_all_lobbies(self) -> None:
        logger.log_info("Starting scheduled health check for all registered lobbies...")
        tasks = [asyncio.create_task(self.check_lobby_connectivity(lobby)) for lobby in self.lobby_manager.get_lobbies()]
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)

    async def run(self) -> None:
        while True:
            await asyncio.sleep(self.interval)
            await self.check_all_lobbies()