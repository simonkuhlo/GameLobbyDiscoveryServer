from os import PathLike
from typing import Optional
from _lib.simons_logging.log_level import LogLevel
from _lib.simons_logging.log_message import LogMessage
from .abstract_logging_output import AbstractLoggingOutput
import os


class SimpleFileOutput(AbstractLoggingOutput):
    def __init__(self, log_level_override: Optional[LogLevel] = None, log_file_path: PathLike[str] = "", file_name: str = "log.txt"):
        self.log_file_path: PathLike[str] = log_file_path
        self.file_name: str = file_name
        super().__init__(log_level_override=log_level_override)

    def _format_message(self, msg: LogMessage) -> str:
        return f"{msg.timestamp} - [{msg.level.name}] {msg.message}"

    @property
    def _full_path(self):
        if self.log_file_path:
            os.makedirs(self.log_file_path, exist_ok=True)
            return os.path.join(self.log_file_path, self.file_name)
        return self.file_name

    def _handle_log(self, msg: LogMessage):
        line = self._format_message(msg)
        with open(self._full_path, "a", encoding="utf-8") as f:
            f.write(line + "\n")