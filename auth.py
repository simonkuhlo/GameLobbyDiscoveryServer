from lobby_manager.game_lobby import ManagedGameLobby


def check_key(key: str, lobby: ManagedGameLobby) -> bool:
    if key == lobby.secret_key:
        return True
    return False