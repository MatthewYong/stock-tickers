from __future__ import annotations

import asyncio
from fastapi import FastAPI

from stock_ticker_api.sockets.stock_socket import register_stock_socket, start_broadcaster

app = FastAPI(title="Stock Ticker API")

register_stock_socket(app)

@app.on_event("startup")
async def _startup() -> None:
    app.state.broadcaster_task = asyncio.create_task(start_broadcaster(app))

@app.on_event("shutdown")
async def _shutdown() -> None:
    task = getattr(app.state, "broadcaster_task", None)
    if task:
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass