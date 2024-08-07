from typing import Optional
from fastapi import WebSocket, status, Query


def validate_token(websocket: WebSocket, token: Optional[str] = Query(None)):
    if token is None or token == "":
        websocket.close(code=status.WS_1008_POLICY_VIOLATION)

    return token
