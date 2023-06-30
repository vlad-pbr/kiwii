from http import HTTPMethod
from http.server import BaseHTTPRequestHandler

from kiwii.architecture.server.api import handle
from kiwii.architecture.server.shared.models import Request, Endpoint


class KiwiiHTTPRequestHandler(BaseHTTPRequestHandler):
    """
    Custom mode `BaseHTTPRequestHandler` which implements compatibility between kiwii API and the
    `BaseHTTPRequestHandler`:
    - handles requests by building a `Request` model and delegating the request handling to the API
    - reading the API `Response` model and returning an actual response to the client by interfacing with the
      `BaseHTTPRequestHandler`
    """

    def handle_request(self) -> None:
        response = handle(
            Request(
                endpoint=Endpoint(
                    method=HTTPMethod[self.command],
                    path=self.path
                ),
                headers=self.headers
            )
        )

        self.send_response(int(response.status))
        self.end_headers()
        if response.body:
            self.wfile.write(response.body.encode())

    def do_GET(self) -> None:
        self.handle_request()

    def do_POST(self) -> None:
        self.handle_request()