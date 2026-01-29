from __future__ import annotations

import random
from datetime import datetime, timezone

from stock_ticker_api.models.stock_model import Stock


class StockService:
    def __init__(self):
        self.symbols = ["EURPGBP", "TSLA", "MSFT", "EURUSD"]
        self._prices: dict[str, float] = {s: random.uniform(50, 300) for s in self.symbols}

    def next_update(self) -> Stock:
        symbol = random.choice(self.symbols)

        old = self._prices[symbol]
        delta = random.uniform(-1.0, 1.0)
        new = max(0.01, old + delta)

        self._prices[symbol] = new

        change = new - old
        percent_change = (change / old) * 100 if old else 0.0

        return Stock(
            symbol=symbol,
            price=round(new, 5),
            change=round(change, 5),
            percent_change=round(percent_change, 5),
            last_updated=datetime.now(timezone.utc)
        )
