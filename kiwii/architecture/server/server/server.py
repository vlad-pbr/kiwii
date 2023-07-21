"""
Kiwii server static class. Not actually a class as static classes are not pythonic.
"""

from dataclasses import asdict
from http.server import ThreadingHTTPServer
from os.path import isfile
from ssl import PROTOCOL_TLS_SERVER, SSLContext
from typing import Optional

from kiwii.architecture.server.api import initialize as initialize_api
from kiwii.architecture.server.api.auth import initialize as initialize_auth
from kiwii.architecture.server.data.data import initialize as initialize_data
from kiwii.architecture.shared.models import ServerAddress, UserCredentials
from kiwii.architecture.server.server.kiwii_http_request_handler import KiwiiHTTPRequestHandler
from kiwii.architecture.server.shared.models import SSLCertChain
from kiwii.shared.logging.logging import get_logger
from kiwii.shared.logging.componentloggername import ComponentLoggerName

logger = get_logger(ComponentLoggerName.SERVER)


def start(
        server_address: ServerAddress,
        ssl_cert_chain: SSLCertChain,
        log_level: str,
        expose_doc: bool,
        credentials: Optional[UserCredentials]):
    """Starts the kiwii server using provided parameters."""

    # set log level for server
    logger.setLevel(log_level)
    logger.info(f"log level is set to '{log_level}'")

    # prepare ssl context
    for _name, _path in asdict(ssl_cert_chain).items():
        if not isfile(_path):
            logger.critical(f"path specified for '{_name}' is not a file: {_path}")
    ssl_context = SSLContext(PROTOCOL_TLS_SERVER)
    ssl_context.load_cert_chain(**asdict(ssl_cert_chain))

    logger.info("initializing server data layer...")
    initialize_data("server.json", log_level)

    logger.info("initializing authentication/authorization layer...")
    if not initialize_auth(credentials, log_level):
        logger.critical("user credentials are not present in storage, please provide them via CLI")

    logger.info("initializing API and registering routes...")
    initialize_api(log_level, expose_doc)

    with ThreadingHTTPServer(server_address.as_tuple(), KiwiiHTTPRequestHandler) as server:

        # apply ssl context
        server.socket = ssl_context.wrap_socket(server.socket, server_side=True)

        # start server
        logger.info(f"server started at {server_address}")
        try:
            server.serve_forever()
        except KeyboardInterrupt as e:
            logger.info(f"received '{e.__class__.__name__}', shutting down...")
