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


def resolve_remote_server_connection(provided_server_params: Optional[RemoteServerParams]):
    """
    Resolves the following:
    - If no parameters were provided, checks that the agent is already registered with a server
    - If parameters were provided (assuming re-registration is enabled), registers with the new server
    """

    # TODO restructure, separate to functions
    existing_remote_connection = get_data_layer().retrieve(RemoteServerStructure)
    connection_exists: bool = existing_remote_connection is not None
    remote_connection: Optional[RemoteServerStructure] = None
    if not connection_exists:
        if provided_server_params is None:
            logger.critical("remote server parameters were not provided and do not exist in storage")
        else:
            # using provided parameters
            remote_connection = RemoteServerStructure(
                address=provided_server_params.address,
                credentials=provided_server_params.credentials
            )
    else:
        if provided_server_params is None:
            pass  # using parameters from storage
        else:
            if provided_server_params.re_register:
                # perform re-registration - go with provided parameters
                connection_exists = False
                remote_connection = RemoteServerStructure(
                    address=provided_server_params.address,
                    credentials=provided_server_params.credentials
                )
            else:
                logger.critical("agent is already registered with a server, use CLI to re-register")

    if connection_exists:
        logger.info(f"using existing remote connection with {existing_remote_connection.address}")
    else:
        logger.info(f"registering with the remote server at {remote_connection.address}...")

        # register with the server
        register_response: Optional[HTTPResponse] = None
        connection = HTTPSConnection(
            host=remote_connection.address.host,
            port=remote_connection.address.port,
            timeout=5,
        )
        try:
            connection.request(
                method=HTTPMethod.POST,
                url=AGENT_POST_ROUTE.path,
                headers=remote_connection.credentials.as_authorization_basic_header()
            )
            register_response = connection.getresponse()
        except ConnectionError as e:
            logger.critical(f"could not connect to the remote server: {e}")
        except ResponseNotReady as e:
            logger.critical(f"an unexpected HTTP client error has occurred: {e}")

        if register_response.getcode() != HTTPStatus.CREATED:
            logger.critical(f"received an error from remote server during registration: {register_response.reason}")

        # TODO store


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

    resolve_remote_server_connection(remote_server_params)
