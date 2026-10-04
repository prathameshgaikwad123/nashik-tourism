#!/usr/bin/env python3
"""
Static server for QA that behaves like the production host would:

  * /path/  -> /path/index.html
  * unknown -> the real 404.html, with a real 404 status
  * .json / .xml / .webmanifest get correct types, no caching (-c-1 equivalent)

    python3 tools/qa/serve.py [port]        # default 8099, serves ./nashiktourism
"""
import http.server
import os
import socketserver
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                     "..", "..", "nashiktourism"))
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8099


class Handler(http.server.SimpleHTTPRequestHandler):
    extensions_map = {
        **http.server.SimpleHTTPRequestHandler.extensions_map,
        ".json": "application/json", ".xml": "application/xml",
        ".webmanifest": "application/manifest+json", ".js": "text/javascript",
    }

    def __init__(self, *a, **kw):
        super().__init__(*a, directory=ROOT, **kw)

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def send_head(self):
        path = self.translate_path(self.path)
        if os.path.isdir(path) and not self.path.split("?")[0].endswith("/"):
            return super().send_head()  # let the base class issue its 301
        if not os.path.exists(path) and not os.path.isdir(path):
            self.path = "/404.html"
            f = open(os.path.join(ROOT, "404.html"), "rb")
            body = f.read()
            f.close()
            self.send_response(404)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            import io
            return io.BytesIO(body)
        return super().send_head()

    def log_message(self, *a):
        pass


class Server(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True
    allow_reuse_address = True


if __name__ == "__main__":
    with Server(("127.0.0.1", PORT), Handler) as srv:
        print("serving %s on http://127.0.0.1:%d" % (ROOT, PORT), flush=True)
        srv.serve_forever()
