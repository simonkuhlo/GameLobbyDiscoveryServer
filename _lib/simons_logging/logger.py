from typing import List, Optional
from .log_level import LogLevel
from .logging_output import AbstractLoggingOutput
from .log_message import LogMessage

class Logger:
    def __init__(self, initial_outputs: Optional[List[AbstractLoggingOutput]] = None, initial_log_level: LogLevel = LogLevel.DEBUG):
        self._log_level: LogLevel = initial_log_level
        self.outputs: List[AbstractLoggingOutput] = []
        if initial_outputs:
            for output in initial_outputs:
                self.add_output(output)

    @property
    def log_level(self) -> LogLevel:
        return self._log_level

    @log_level.setter
    def log_level(self, new_log_level: LogLevel) -> None:
        self._log_level = new_log_level

    def add_output(self, output: AbstractLoggingOutput) -> None:
        if output.parent_logger:
            self.log_warning(f"Took over control of a logging output with a previous parent. Previous parent: {output.parent_logger}")
        output.parent_logger = self
        self.outputs.append(output)

    def remove_output(self, output: AbstractLoggingOutput) -> None:
        if output not in self.outputs:
            self.log_warning("Tried to remove an output that is not controlled by this logger.")
            return
        self.outputs.remove(output)
        output.parent_logger = None

    def log(self, msg:LogMessage) -> None:
        for output in self.outputs:
            output.log(msg)

    def log_debug(self, content: str) -> None:
        """Shortcut for logging events with LogLevel DEBUG"""
        message: LogMessage = LogMessage(level=LogLevel.DEBUG, message=content)
        self.log(message)

    def log_info(self, content: str) -> None:
        """Shortcut for logging events with LogLevel INFO"""
        message: LogMessage = LogMessage(level=LogLevel.INFO, message=content)
        self.log(message)

    def log_warning(self, content: str) -> None:
        """Shortcut for logging events with LogLevel WARNING"""
        message: LogMessage = LogMessage(level=LogLevel.WARNING, message=content)
        self.log(message)

    def log_error(self, content: str) -> None:
        """Shortcut for logging events with LogLevel ERROR"""
        message: LogMessage = LogMessage(level=LogLevel.ERROR, message=content)
        self.log(message)