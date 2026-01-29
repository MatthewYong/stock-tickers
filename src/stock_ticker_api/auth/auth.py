from __future__ import annotations

import base64
from typing import Final

from fastapi import HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets
from fastapi import Depends
from fastapi.websockets import WebSocket

security: Final = HTTPBasic()

USERS: Final[dict[str, str]] = {
    "admin": "changeme",
}


def verify_credentials(username: str, password: str) -> None:
    expected = USERS.get(username)
    ok = expected is not None and secrets.compare_digest(password, expected)
    if not ok:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")


def require_http_basic(creds: HTTPBasicCredentials = Depends(security)) -> str:
    verify_credentials(creds.username, creds.password)
    return creds.username


def _parse_basic_auth_header(value: str) -> tuple[str, str] | None:
    parts = value.split(" ", 1)
    if len(parts) != 2 or parts[0].lower() != "basic":
        return None

    try:
        raw = base64.b64decode(parts[1]).decode("utf-8")
    except Exception:
        return None

    if ":" not in raw:
        return None
    username, password = raw.split(":", 1)
    return username, password


async def require_ws_auth(websocket: WebSocket) -> str:
    auth = websocket.headers.get("authorization")
    if auth:
        parsed = _parse_basic_auth_header(auth)
        if parsed:
            username, password = parsed
            verify_credentials(username, password)
            return username

    username = websocket.query_params.get("username")
    password = websocket.query_params.get("password")
    if username and password:
        verify_credentials(username, password)
        return username

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing/invalid WebSocket auth")
