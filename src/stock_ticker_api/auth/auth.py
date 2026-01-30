from __future__ import annotations

import secrets
from fastapi import Depends, HTTPException, WebSocket, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

security = HTTPBasic()

_USERS = {
    "admin": "changeme",
}



def verify_credentials(credentials: HTTPBasicCredentials) -> None:
    correct_password = _USERS.get(credentials.username)
    if not correct_password or not secrets.compare_digest(
            credentials.password, correct_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )


def require_basic_auth(
        credentials: HTTPBasicCredentials = Depends(security),
) -> None:
    verify_credentials(credentials)


async def require_ws_auth(websocket: WebSocket) -> None:
    auth_header = websocket.headers.get("authorization")
    if not auth_header:
        raise Exception("Missing Authorization header")

    try:
        scheme, encoded = auth_header.split(" ", 1)
        if scheme.lower() != "basic":
            raise Exception("Invalid auth scheme")

        import base64

        decoded = base64.b64decode(encoded).decode()
        username, password = decoded.split(":", 1)

    except Exception:
        raise Exception("Invalid Authorization header")

    credentials = HTTPBasicCredentials(
        username=username,
        password=password,
    )

    verify_credentials(credentials)
