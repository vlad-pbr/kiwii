"""
Kiwii agent static class. Not actually a class as static classes are not pythonic.
"""
from http import HTTPMethod, HTTPStatus
from http.client import HTTPSConnection, HTTPResponse, ResponseNotReady
from ssl import SSLError
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
        logger.critical(f"an unexpected HTTP client error has occurred while connecting to the remote server: {e}")
    except Exception as e:
        logger.critical(f"an unexpected error has occurred while connecting to the remote server: {e}")

    # parse response
    if register_response.getcode() != HTTPStatus.CREATED:
        logger.critical(f"received an error from remote server during registration: {register_response.code} {register_response.reason}")

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

    # handle server registration
    existing_server_connection = get_data_layer().retrieve(RemoteServerStructure)
    match (remote_server_params is not None, existing_server_connection is not None, remote_server_params is not None and remote_server_params.re_register is True):
        case (True, True, True):
            logger.info(f"re-registering with a new remote server at {remote_server_params.address}...")
            register_with_remote_server(remote_server_params)
        case (True, True, False):
            logger.critical("agent is already registered with a server, use CLI to re-register")
        case (True, False, True):
            logger.critical("re-registration flag was provided, but the agent is not registered with any server")
        case (True, False, _):
            logger.info(f"registering with the remote server at {remote_server_params.address}...")
            register_with_remote_server(remote_server_params)
        case (False, True, _):
            logger.info(f"using existing remote connection with {existing_server_connection.address}...")
        case (False, False, _):
            logger.critical("remote server parameters were not provided and do not exist in storage")
