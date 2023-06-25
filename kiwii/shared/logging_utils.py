import logging
from typing import Optional

_default_formatter = logging.Formatter('[%(asctime)s] - %(name)s - %(levelname)s - %(message)s')


class _ExitOnCriticalLogHandler(logging.StreamHandler):
    def emit(self, record):
        super().emit(record)
        if record.levelno is logging.CRITICAL:
            raise SystemExit(-1)


def get_critical_exit_logger(name: Optional[str]) -> logging.Logger:
    logger = logging.getLogger(name)
    critical_log_handler = _ExitOnCriticalLogHandler()
    critical_log_handler.setFormatter(_default_formatter)
    logger.addHandler(critical_log_handler)

    return logger
