#!/usr/bin/env python3
from http.server import BaseHTTPRequestHandler, HTTPServer
import json, socket
from datetime import datetime, timezone

SERVICE_NAME = "auth-service"
PORT = 8101

class Handler(BaseHTTPRequestHandler):
    def send_json(self, payload, code=200):
        data = json.dumps(payload, indent=2).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        base = {
            "service": SERVICE_NAME,
            "status": "healthy",
            "hostname": socket.gethostname(),
            "private_subnet": True,
            "publicly_exposed": False,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

        if self.path in ["/", "/health", "/api/status"]:
            self.send_json(base)
        elif self.path.startswith("/api/demo"):
            payload = dict(base)
            payload["demo"] = "Handles login, MFA, sessions, and token validation."
            payload["note"] = "Training data only. No real banking data."
            self.send_json(payload)
        else:
            self.send_json({"error": "not found", "service": SERVICE_NAME}, 404)

if __name__ == "__main__":
    print(f"{SERVICE_NAME} listening on port {PORT}")
    HTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
