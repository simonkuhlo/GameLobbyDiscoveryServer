from lobby_manager.game_lobby import GameLobby, ManagedGameLobby
from models.game_lobby import GameLobbyRead, GameLobbyCreate, PartialGameLobbyUpdate

def instance_from_create_model(model: GameLobbyCreate) -> GameLobby:
    return GameLobby(
        secret_key=model.secret_key,
        port=model.port,
        address=model.address,
        max_players=model.max_players,
        current_players=model.current_players,
        game_state=model.game_state,
        name=model.name,
        desc=model.desc
    )

def read_model_from_managed_instance(lobby: ManagedGameLobby) -> GameLobbyRead:
    return GameLobbyRead(
        lobby_id=lobby.lobby_id,
        port=lobby.port,
        address=lobby.address,
        max_players=lobby.max_players,
        current_players=lobby.current_players,
        game_state=lobby.game_state,
        name=lobby.name,
        desc=lobby.desc,
        last_heartbeat=lobby.last_heartbeat
    )

def update_game_lobby_with_model(lobby: ManagedGameLobby, update: PartialGameLobbyUpdate) -> None:
    if update.name is not None:
        lobby.name = update.name
    if update.desc is not None:
        lobby.desc = update.desc
    if update.port is not None:
        lobby.port = update.port
    if update.address is not None:
        lobby.address = update.address
    if update.max_players is not None:
        lobby.max_players = update.max_players
    if update.current_players is not None:
        lobby.current_players = update.current_players
    if update.game_state is not None:
        lobby.game_state = update.game_state