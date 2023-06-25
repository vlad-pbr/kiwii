from os.path import isfile
from dataclasses import asdict
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from ssl import PROTOCOL_TLS_SERVER, SSLContext
from typing import Optional

from kiwii.architecture.server.api import handle
from kiwii.architecture.server.shared.models import SSLCertChain, ServerAddress
from kiwii.shared.logging_utils import get_critical_exit_logger

_logger = get_critical_exit_logger("kiwii-server")


class KiwiiRequestHandler(BaseHTTPRequestHandler):

    def handle_request(self) -> None:
        status, body = handle(self.command, self.path)
        status_code = int(status)

        self.send_response(int(status_code))
        self.end_headers()
        if body:
            self.wfile.write(body.encode())

    def do_GET(self) -> None:
        self.handle_request()

    def do_POST(self) -> None:
        self.handle_request()


def start(server_address: ServerAddress, ssl_cert_chain: Optional[SSLCertChain], log_level: str):

    # set log level for server logger
    _logger.setLevel(log_level)
    _logger.info(f"log level is set to '{log_level}'")

    # prepare ssl context if cert chain was provided
    ssl_context: Optional[SSLContext] = None
    if ssl_cert_chain:

        # validate paths for certificate keys
        for _name, _path in asdict(ssl_cert_chain).items():
            if not isfile(_path):
                _logger.critical(f"path specified for '{_name}' is not a file: {_path}")

        ssl_context = SSLContext(PROTOCOL_TLS_SERVER)  # TODO ciphers
        ssl_context.load_cert_chain(**asdict(ssl_cert_chain))

    with ThreadingHTTPServer(server_address, KiwiiRequestHandler) as server:

        # apply ssl context if cert chain was provided
        if ssl_context:
            server.socket = ssl_context.wrap_socket(server.socket, server_side=True)
        else:
            _logger.warning("SSL certificate was not provided, but is very much recommended")

        _logger.info(f"server started at {server_address} (TLS {'secure' if ssl_context else 'insecure'})")
        server.serve_forever()
