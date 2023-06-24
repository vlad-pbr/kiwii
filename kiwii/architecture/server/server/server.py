from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler


class KiwiiRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self) -> None:
        self.send_response(200)
        self.end_headers()
        self.wfile.write("its alive!".encode())


def start(host: str, port: int):
    with ThreadingHTTPServer((host, port), KiwiiRequestHandler) as server:
        server.serve_forever()
