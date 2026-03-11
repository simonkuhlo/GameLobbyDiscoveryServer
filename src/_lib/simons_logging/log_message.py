import datetime
from typing import Optional
from .log_level import LogLevel

class LogMessage:
    def __init__(self, source: Optional[str] = None, level: LogLevel = LogLevel.INFO, message: str = ""):
        self.timestamp = datetime.datetime.now().timestamp()
        self.source: str = source
        self.level: LogLevel = level
        self.message: str = message

    def __str__(self) -> str:
        output: str = f"{self.level.name} {self.source}: {self.message}"
        return output