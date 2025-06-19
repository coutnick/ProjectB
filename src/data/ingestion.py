import asyncio
from typing import Dict, Any

import ccxt.async_support as ccxt


class MarketDataStreamer:
    """Fetches market data from the exchange."""

    def __init__(self, exchange: ccxt.Exchange, markets):
        self.exchange = exchange
        self.markets = markets

    async def fetch_ticker(self, symbol: str) -> Dict[str, Any]:
        return await self.exchange.fetch_ticker(symbol)

    async def stream(self):
        while True:
            data = {}
            for market in self.markets:
                ticker = await self.fetch_ticker(market)
                data[market] = ticker
            yield data
            await asyncio.sleep(1)
