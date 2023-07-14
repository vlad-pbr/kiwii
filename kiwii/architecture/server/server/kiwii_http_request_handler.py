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

        # handle request
        response = handle(
            Request(
                endpoint=Endpoint(
                    method=HTTPMethod[self.command],
                    path=self.path
                ),
                headers=self.headers
            )
        )

        # set response status code
        self.send_response(int(response.status))

        # attach response headers if specified
        if response.headers:
            for header, value in response.headers.items():
                self.send_header(header, value)
        self.end_headers()

        # attach body is specified
        if response.body:
            if isinstance(response.body, str):
                response.body = response.body.encode()
            self.wfile.write(response.body)

    def do_GET(self) -> None:
        self.handle_request()

    def do_POST(self) -> None:
        self.handle_request()
