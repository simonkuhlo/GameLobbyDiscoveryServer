from typing import List
from _lib.simons_logging.logger import Logger
from _lib.simons_logging.logging_output import SimpleFileOutput, SimplePrintOutput, AbstractLoggingOutput
from .settings import settings

file_output: SimpleFileOutput = SimpleFileOutput(
    log_level_override=settings.logging.file.log_level_override,
    log_file_path=settings.logging.file.file_path,
    file_name=settings.logging.file.file_name
)

console_output: SimplePrintOutput = SimplePrintOutput(
    log_level_override=settings.logging.console.log_level_override
)

outputs: List[AbstractLoggingOutput] = [file_output, console_output]
logger = Logger(outputs)