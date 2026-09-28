import http.server
import os
import socketserver

HOST = os.environ.get("BIND_ADDRESS", "127.0.0.1")
PORT = int(os.environ.get("PORT", "10000"))


class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != "/":
            self.send_response(404)
            self.end_headers()
            return
        body = b"ok\n"
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        return


class Server(socketserver.ThreadingTCPServer):
    allow_reuse_address = True


print(f"LISTENING {HOST}:{PORT}", flush=True)
with Server((HOST, PORT), Handler) as server:
    server.serve_forever()
