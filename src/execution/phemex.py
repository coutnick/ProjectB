import asyncio
import logging

import ccxt.async_support as ccxt


class PhemexExecution:
    def __init__(self, api_key: str, api_secret: str, testnet: bool = True):
        params = {'enableRateLimit': True}
        if testnet:
            params['urls'] = {'api': {'public': 'https://testnet.phemex.com'} }
        self.exchange = ccxt.phemex({
            'apiKey': api_key,
            'secret': api_secret,
            **params,
        })

    async def place_order(self, symbol: str, side: str, amount: float):
        try:
            method = self.exchange.create_market_buy_order if side == 'buy' else self.exchange.create_market_sell_order
            return await method(symbol, amount)
        except Exception as e:
            logging.error(f'Order error: {e}')

    async def close(self):
        await self.exchange.close()
