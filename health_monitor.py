from lobby_manager.lobby_manager import LobbyManager

class HealthMonitor:
    def __init__(self, lobby_manager: LobbyManager, interval: int = 10) -> None:
        self.lobby_manager: LobbyManager = lobby_manager
        self.interval: float = interval

    async def task(self):
        pass