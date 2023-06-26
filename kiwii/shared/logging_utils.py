import logging
from enum import StrEnum

_default_formatter = logging.Formatter('[%(asctime)s] - %(name)s - %(levelname)s - %(message)s')


class LoggerName(StrEnum):
    SERVER = "server"
    API = "api"


class _ExitOnCriticalLogHandler(logging.StreamHandler):
    def emit(self, record):
        super().emit(record)
        if record.levelno is logging.CRITICAL:
            raise SystemExit(-1)


def get_critical_exit_logger(name: LoggerName) -> logging.Logger:
    logger = logging.getLogger(f"kiwii-{name.value}")
    critical_log_handler = _ExitOnCriticalLogHandler()
    critical_log_handler.setFormatter(_default_formatter)
    logger.addHandler(critical_log_handler)

    return logger
