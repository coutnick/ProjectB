import asyncio
import logging
from datetime import datetime

import ccxt.async_support as ccxt
import pandas as pd

from src.config.config import load_config
from src.data.ingestion import MarketDataStreamer
from src.features.technical import compute_indicators
from src.strategy.rules import simple_moving_average_strategy
from src.risk.manager import RiskManager, RiskSettings
from src.execution.phemex import PhemexExecution
from src.rl.policy import RLPolicy
from src.agents.sentiment import SentimentAgent


logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')


def empty_df():
    return pd.DataFrame(columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])


def append_ticker(df: pd.DataFrame, ticker: dict) -> pd.DataFrame:
    return df.append({'timestamp': datetime.utcnow(),
                      'open': ticker['open'],
                      'high': ticker['high'],
                      'low': ticker['low'],
                      'close': ticker['close'],
                      'volume': ticker.get('baseVolume', 0)}, ignore_index=True)


async def main():
    cfg = load_config()

    exchange = ccxt.phemex({'apiKey': cfg.exchange.api_key, 'secret': cfg.exchange.api_secret})
    if cfg.exchange.use_testnet:
        exchange.set_sandbox_mode(True)

    streamer = MarketDataStreamer(exchange, cfg.trading.markets)
    executor = PhemexExecution(cfg.exchange.api_key, cfg.exchange.api_secret, cfg.exchange.use_testnet)
    risk = RiskManager(RiskSettings(cfg.trading.max_position_usd, cfg.trading.stop_loss_pct))
    rl_policy = RLPolicy(cfg.rl.policy_path) if cfg.rl.enable else None
    sentiment_agent = SentimentAgent(cfg.agents.openai_api_key) if cfg.agents.enable_sentiment else None

    history = {market: empty_df() for market in cfg.trading.markets}

    async for data in streamer.stream():
        for market, ticker in data.items():
            history[market] = append_ticker(history[market], ticker)
            df = compute_indicators(history[market])
            signal = simple_moving_average_strategy(df)

            if signal and risk.evaluate(signal):
                await executor.place_order(market, signal.action, signal.size)
                risk.on_fill(signal)

        await asyncio.sleep(1)

    await executor.close()


if __name__ == '__main__':
    asyncio.run(main())
