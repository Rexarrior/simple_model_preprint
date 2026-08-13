import json
import os
import sqlite3
import uuid
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


DB_PATH = os.environ.get("DB_PATH", "/data/shared-calculations.sqlite3")
MAX_REQUEST_BYTES = 300_000
MAX_STORED_JSON_BYTES = 280_000


def connect() -> sqlite3.Connection:
    connection = sqlite3.connect(DB_PATH, timeout=10)
    connection.execute("PRAGMA journal_mode=WAL")
    connection.execute("PRAGMA busy_timeout=10000")
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS shared_calculations (
            id TEXT PRIMARY KEY NOT NULL,
            created_at TEXT NOT NULL,
            schema_version TEXT NOT NULL,
            project_name TEXT NOT NULL,
            consent_version TEXT NOT NULL,
            config_json TEXT NOT NULL,
            result_json TEXT NOT NULL
        )
        """
    )
    connection.execute(
        "CREATE INDEX IF NOT EXISTS idx_shared_calculations_created_at "
        "ON shared_calculations(created_at)"
    )
    return connection


class Handler(BaseHTTPRequestHandler):
    server_version = "m4-api"
    sys_version = ""

    def log_message(self, _format: str, *_args: object) -> None:
        # Do not write visitor IP addresses or request bodies to application logs.
        return

    def send_json(self, payload: dict[str, object], status: int = 200) -> None:
        body = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        if self.path == "/api/health":
            self.send_json({"status": "ok", "persistence": "opt-in-only"})
            return
        self.send_json({"error": "not_found"}, 404)

    def do_POST(self) -> None:
        if self.path != "/api/share":
            self.send_json({"error": "not_found"}, 404)
            return

        try:
            content_length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            self.send_json({"error": "invalid_content_length"}, 400)
            return
        if content_length <= 0 or content_length > MAX_REQUEST_BYTES:
            self.send_json({"error": "payload_too_large"}, 413)
            return

        try:
            body = json.loads(self.rfile.read(content_length))
        except (json.JSONDecodeError, UnicodeDecodeError):
            self.send_json({"error": "invalid_json"}, 400)
            return

        if not isinstance(body, dict):
            self.send_json({"error": "invalid_json"}, 400)
            return
        if body.get("consent") is not True or body.get("consentVersion") != "v1":
            self.send_json({"error": "explicit_consent_required"}, 403)
            return

        config = body.get("config")
        result = body.get("result")
        if (
            not isinstance(config, dict)
            or not isinstance(result, dict)
            or config.get("schemaVersion") != "m4-calculator/v1"
        ):
            self.send_json({"error": "invalid_calculation"}, 400)
            return

        config_json = json.dumps(config, ensure_ascii=False, separators=(",", ":"))
        result_json = json.dumps(result, ensure_ascii=False, separators=(",", ":"))
        if len(config_json.encode()) + len(result_json.encode()) > MAX_STORED_JSON_BYTES:
            self.send_json({"error": "payload_too_large"}, 413)
            return

        calculation_id = str(uuid.uuid4())
        created_at = datetime.now(timezone.utc).isoformat()
        project_name = str(config.get("projectName", "Без названия"))[:200]
        with connect() as connection:
            connection.execute(
                """
                INSERT INTO shared_calculations
                    (id, created_at, schema_version, project_name,
                     consent_version, config_json, result_json)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    calculation_id,
                    created_at,
                    "m4-calculator/v1",
                    project_name,
                    "v1",
                    config_json,
                    result_json,
                ),
            )

        self.send_json({"id": calculation_id, "saved": True}, 201)


if __name__ == "__main__":
    with connect():
        pass
    ThreadingHTTPServer(("0.0.0.0", 8000), Handler).serve_forever()
