from typing import Optional
from pydantic import BaseModel, Field
import json
from pathlib import Path

class BaseLoggingOutputSettings(BaseModel):
    active: bool = Field(default=True)
    log_level_override: Optional[int] = Field(default=None)

class ConsoleLoggingSettings(BaseLoggingOutputSettings):
    pass

class FileLoggingSettings(BaseLoggingOutputSettings):
    file_path: str = Field(default="")
    file_name: str = Field(default="_config/log.txt")

class LoggingSettings(BaseModel):
    level: int = Field(default=0)
    console: ConsoleLoggingSettings = ConsoleLoggingSettings()
    file: FileLoggingSettings = FileLoggingSettings()

class SystemSettings(BaseModel):
    pass

class LobbyManagerSettings(BaseModel):
    max_index: int = Field(default=10000)
    max_lobbies: int = Field(default=1000)
    health_check_frequency_seconds: int = Field(default=10)

class Settings(BaseModel):
    system: SystemSettings = SystemSettings()
    logging: LoggingSettings = LoggingSettings()
    lobby_manager: LobbyManagerSettings = LobbyManagerSettings()


def save_settings(path: str | Path, settings: Settings) -> None:
    path = Path(path)
    data = settings.model_dump()
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def load_settings(path: str | Path) -> Settings:
    path = Path(path)
    data = json.loads(path.read_text(encoding="utf-8"))
    return Settings(**data)