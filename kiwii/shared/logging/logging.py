"""
Logging related utilities used across all core parts of the architecture.
"""

import logging

from kiwii.shared.logging.componentloggername import ComponentLoggerName
from kiwii.shared.logging.consts import default_formatter
from kiwii.shared.logging.exitonexceptionhandler import ExitOnCriticalLogHandler

critical_log_handler = ExitOnCriticalLogHandler()
critical_log_handler.setFormatter(default_formatter)


def apply_kiwii_configuration(logger: logging.Logger) -> None:
    """Set default logging parameters to given logger"""

    logger.addHandler(critical_log_handler)


def get_logger(component: ComponentLoggerName) -> logging.Logger:
    """
    Returns a logger for requested architecture entity with `ExitOnCriticalLogHandler` log handler installed.
    """

    _logger = logging.getLogger(f"kiwii-{component.value}")
    apply_kiwii_configuration(_logger)

    return _logger
