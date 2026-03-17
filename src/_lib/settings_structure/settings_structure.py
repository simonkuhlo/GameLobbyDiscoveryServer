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
    heartbeat_frequency: float = Field(default=15000)

class HealthCheckSettings(BaseModel):
    enabled: bool = Field(default=True)
    frequency_seconds: float = Field(default=15.0)
    heartbeat_grace_period: float = Field(default=60.0)

class Settings(BaseModel):
    system: SystemSettings = SystemSettings()
    logging: LoggingSettings = LoggingSettings()
    lobby_manager: LobbyManagerSettings = LobbyManagerSettings()
    health_check: HealthCheckSettings = HealthCheckSettings()

def save_settings(path: str | Path, settings: Settings) -> None:
    path = Path(path)
    data = settings.model_dump()
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def load_settings(path: str | Path) -> Settings:
    path = Path(path)
    if not path.exists():
        save_settings(path, Settings())
    data = json.loads(path.read_text(encoding="utf-8"))
    return Settings(**data)