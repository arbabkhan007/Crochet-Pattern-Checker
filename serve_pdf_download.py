#!/usr/bin/env python3
"""Serve the Coco PDF with a Content-Disposition: attachment so it downloads."""
import os
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output", "pdf")


class DownloadHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIR, **kwargs)

    def end_headers(self):
        if self.path.split("?")[0].lower().endswith(".pdf"):
            filename = os.path.basename(self.path.split("?")[0])
            self.send_header("Content-Disposition", f'attachment; filename="{filename}"')
            self.send_header("Content-Type", "application/octet-stream")
        super().end_headers()

    def log_message(self, fmt, *args):
        print(f"{self.address_string()} {fmt % args}", flush=True)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    print(f"Serving {DIR} on 0.0.0.0:{port}", flush=True)
    ThreadingHTTPServer(("0.0.0.0", port), DownloadHandler).serve_forever()
