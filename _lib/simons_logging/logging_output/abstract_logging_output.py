from typing import Optional, TYPE_CHECKING
from _lib.simons_logging.log_level import LogLevel
from _lib.simons_logging.log_message import LogMessage
from abc import ABC, abstractmethod
if TYPE_CHECKING:
    from ..logger import Logger


class AbstractLoggingOutput(ABC):
    def __init__(self, parent_logger: Optional["Logger"] = None, log_level_override: Optional[LogLevel] = None):
        self.parent_logger: Optional["Logger"] = parent_logger
        self.log_level_override: LogLevel = log_level_override

    @property
    def effective_log_level(self) -> LogLevel:
        if self.log_level_override:
            return self.log_level_override
        if self.parent_logger:
            return self.parent_logger.log_level
        return LogLevel.DEBUG

    def should_log(self, msg: LogMessage) -> bool:
        return msg.level.value <= self.effective_log_level.value

    def log(self, msg: LogMessage):
        if self.should_log(msg):
            self._handle_log(msg)

    @abstractmethod
    def _handle_log(self, msg: LogMessage):
        raise NotImplementedError

    def _format_message(self, msg: LogMessage) -> str:
        return f"[{msg.level.name}] {msg.message}"