"""
Logging related utilities used across all core parts of the architecture.
"""

import logging
from enum import StrEnum

default_formatter = logging.Formatter('[%(asctime)s] - %(name)s - %(levelname)s - %(message)s')


class LoggerName(StrEnum):
    """Logger names for the core parts of kiwii architecture."""

    SERVER = "server"
    API = "api"


class ExitOnCriticalLogHandler(logging.StreamHandler):
    """
    Custom logging stream handler which exits on log with critical log level.
    """

    def emit(self, record):
        super().emit(record)
        if record.levelno is logging.CRITICAL:
            raise SystemExit(-1)


def get_critical_exit_logger(name: LoggerName) -> logging.Logger:
    """
    Returns a logger for requested architecture entity with `ExitOnCriticalLogHandler` log handler installed.
    """

    logger = logging.getLogger(f"kiwii-{name.value}")
    critical_log_handler = ExitOnCriticalLogHandler()
    critical_log_handler.setFormatter(default_formatter)
    logger.addHandler(critical_log_handler)

    return logger
