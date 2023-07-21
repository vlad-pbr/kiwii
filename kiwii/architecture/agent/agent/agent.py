"""
Kiwii agent static class. Not actually a class as static classes are not pythonic.
"""
from http import HTTPMethod, HTTPStatus
from http.client import HTTPSConnection, HTTPResponse, ResponseNotReady
from typing import Optional

from kiwii.architecture.agent.data.data import initialize as initialize_data, get_data_layer
from kiwii.architecture.agent.data.data_structures.remote_server import RemoteServerStructure
from kiwii.architecture.agent.shared.models import RemoteServerParams
from kiwii.architecture.shared.routes import AGENT_POST_ROUTE
from kiwii.shared.logging.componentloggername import ComponentLoggerName
from kiwii.shared.logging.logging import get_logger

logger = get_logger(ComponentLoggerName.AGENT)


def register_with_remote_server(provided_server_params: Optional[RemoteServerParams]):

    # set-up connection with remote server
    register_response: Optional[HTTPResponse] = None
    connection = HTTPSConnection(
        host=provided_server_params.address.host,
        port=provided_server_params.address.port,
        timeout=5,
    )

    # send registration request
    try:
        connection.request(
            method=HTTPMethod.POST,
            url=AGENT_POST_ROUTE.path,
            headers=provided_server_params.credentials.as_authorization_basic_header()
        )
        register_response = connection.getresponse()
    except ConnectionError as e:
        logger.critical(f"could not connect to the remote server: {e}")
    except ResponseNotReady as e:
        logger.critical(f"an unexpected HTTP client error has occurred: {e}")

    # parse response
    if register_response.getcode() != HTTPStatus.CREATED:
        logger.critical(f"received an error from remote server during registration: {register_response.reason}")

    # TODO store


def resolve_remote_server_connection(provided_server_params: Optional[RemoteServerParams]) -> bool:
    """
    Resolves the following:
    - If no parameters were provided, checks that the agent is already registered with a server and if so, returns True
    - If parameters were provided (assuming re-registration is enabled), returns False
    """

    if get_data_layer().retrieve(RemoteServerStructure) is None:
        if provided_server_params is None:
            logger.critical("remote server parameters were not provided and do not exist in storage")
        else:
            return False
    else:
        if provided_server_params is None:
            return True
        else:
            if provided_server_params.re_register:
                return False
            else:
                logger.critical("agent is already registered with a server, use CLI to re-register")


def start(
        remote_server_params: Optional[RemoteServerParams],
        log_level: str
):
    """Starts the kiwii agent using provided parameters."""

    # set log level for server
    logger.setLevel(log_level)
    logger.info(f"log level is set to '{log_level}'")

    logger.info("initializing agent data layer...")
    initialize_data("agent.json", log_level)

    if not resolve_remote_server_connection(remote_server_params):
        logger.info(f"registering with the remote server at {remote_server_params.address}...")
        register_with_remote_server(remote_server_params)
    else:
        logger.info("using existing remote connection")
