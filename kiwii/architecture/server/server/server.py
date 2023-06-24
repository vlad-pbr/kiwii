from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler

from kiwii.architecture.server.api import handle


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


def start(host: str, port: int):
    with ThreadingHTTPServer((host, port), KiwiiRequestHandler) as server:
        server.serve_forever()
