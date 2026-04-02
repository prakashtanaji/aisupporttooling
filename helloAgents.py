"""Minimal MCP server for Codex CLI over stdio.

This server is dependency-free and implements a small subset of the
Model Context Protocol sufficient for Codex CLI tool usage.

Example Codex CLI config snippet:

{
  "mcpServers": {
    "helloAgents": {
      "command": "python",
      "args": ["C:\\Users\\tgpra\\Documents\\code\\aisupporttooling\\helloAgents.py"]
    }
  }
}
"""

from __future__ import annotations

import json
import sys
import traceback
from typing import Any

SERVER_INFO = {
    "name": "helloAgents",
    "version": "0.1.0",
}

TOOLS = [
    {
        "name": "say_hello",
        "description": "Return a greeting for the provided name.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "Name to greet.",
                }
            },
            "required": ["name"],
            "additionalProperties": False,
        },
    },
    {
        "name": "echo",
        "description": "Echo a message back to the caller.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "message": {
                    "type": "string",
                    "description": "Text to echo.",
                }
            },
            "required": ["message"],
            "additionalProperties": False,
        },
    },
]


def read_message() -> dict[str, Any] | None:
    """Read one MCP message framed with Content-Length headers."""
    content_length = None

    while True:
        line = sys.stdin.buffer.readline()
        if not line:
            return None

        if line in (b"\r\n", b"\n"):
            break

        header = line.decode("utf-8").strip()
        if header.lower().startswith("content-length:"):
            content_length = int(header.split(":", 1)[1].strip())

    if content_length is None:
        raise ValueError("Missing Content-Length header")

    body = sys.stdin.buffer.read(content_length)
    if not body:
        return None

    return json.loads(body.decode("utf-8"))


def send_message(message: dict[str, Any]) -> None:
    """Write one MCP message framed with Content-Length headers."""
    payload = json.dumps(message, separators=(",", ":"), ensure_ascii=True).encode(
        "utf-8"
    )
    sys.stdout.buffer.write(f"Content-Length: {len(payload)}\r\n\r\n".encode("ascii"))
    sys.stdout.buffer.write(payload)
    sys.stdout.buffer.flush()


def make_text_result(text: str) -> dict[str, Any]:
    return {"content": [{"type": "text", "text": text}]}


def make_error(code: int, message: str) -> dict[str, Any]:
    return {"code": code, "message": message}


def handle_request(method: str, params: dict[str, Any] | None) -> dict[str, Any] | None:
    params = params or {}

    if method == "initialize":
        return {
            "protocolVersion": "2024-11-05",
            "capabilities": {"tools": {}},
            "serverInfo": SERVER_INFO,
        }

    if method == "notifications/initialized":
        return None

    if method == "ping":
        return {}

    if method == "tools/list":
        return {"tools": TOOLS}

    if method == "tools/call":
        name = params.get("name")
        arguments = params.get("arguments", {})

        if name == "say_hello":
            person = arguments.get("name", "").strip()
            if not person:
                raise ValueError("name is required")
            return make_text_result(f"Hello, {person}. MCP server is connected.")

        if name == "echo":
            message = arguments.get("message", "")
            return make_text_result(str(message))

        raise ValueError(f"Unknown tool: {name}")

    raise ValueError(f"Unsupported method: {method}")


def main() -> int:
    while True:
        try:
            request = read_message()
            if request is None:
                return 0

            method = request.get("method")
            request_id = request.get("id")
            params = request.get("params")

            result = handle_request(method, params)
            if request_id is not None and result is not None:
                send_message({"jsonrpc": "2.0", "id": request_id, "result": result})
        except Exception as exc:  # pragma: no cover
            request_id = None
            if "request" in locals() and isinstance(request, dict):
                request_id = request.get("id")

            error = make_error(-32000, f"{exc}")

            if request_id is not None:
                send_message({"jsonrpc": "2.0", "id": request_id, "error": error})
            else:
                traceback.print_exc(file=sys.stderr)
                return 1


if __name__ == "__main__":
    raise SystemExit(main())
