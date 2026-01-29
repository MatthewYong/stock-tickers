from __future__ import annotations

import asyncio

from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from stock_ticker_api.models.stock_model import Stock
from stock_ticker_api.services.stock_service import StockService
from stock_ticker_api.auth.auth import require_ws_auth


class ConnectionManager:
    def __init__(self) -> None:
        self._connections: set[WebSocket] = set()
        self._lock = asyncio.Lock()

    async def connect(self, websocket: WebSocket) -> None:
        async with self._lock:
            self._connections.add(websocket)

    async def disconnect(self, websocket: WebSocket) -> None:
        async with self._lock:
            self._connections.discard(websocket)

    async def broadcast(self, message: Stock) -> None:
        async with self._lock:
            conns = list(self._connections)

        for ws in conns:
            try:
                await ws.send_json(message)
            except Exception:
                await self.disconnect(ws)


async def start_broadcaster(app: FastAPI) -> None:
    manager: ConnectionManager = app.state.ws_manager
    service: StockService = app.state.stock_service

    try:
        while True:
            update = service.next_update()
            payload = update.model_dump(mode="json")
            await manager.broadcast(payload)
            await asyncio.sleep(2)
    except asyncio.CancelledError:
        return


def register_stock_socket(app: FastAPI) -> None:
    app.state.ws_manager = ConnectionManager()
    app.state.stock_service = StockService()

    @app.websocket("/ws/ticker")
    async def ws_ticker(websocket: WebSocket) -> None:
        await websocket.accept()

        try:
            await require_ws_auth(websocket)
        except Exception:
            await websocket.close(code=1008)
            return

        manager: ConnectionManager = app.state.ws_manager
        await manager.connect(websocket)

        try:
            while True:
                await asyncio.sleep(60)
        except WebSocketDisconnect:
            pass
        finally:
            await manager.disconnect(websocket)
