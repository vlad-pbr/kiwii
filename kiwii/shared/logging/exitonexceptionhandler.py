import logging


class ExitOnCriticalLogHandler(logging.StreamHandler):
    """
    Custom logging stream handler which exits on log with critical log level.
    """

    def emit(self, record):
        super().emit(record)
        if record.levelno is logging.CRITICAL:
            raise SystemExit(-1)
