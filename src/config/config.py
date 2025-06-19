from dataclasses import dataclass
from pathlib import Path
from typing import List

from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=Path('.') / '.env')

@dataclass
class ExchangeConfig:
    name: str
    api_key: str
    api_secret: str
    use_testnet: bool = True

@dataclass
class TradingConfig:
    markets: List[str]
    max_position_usd: float = 1000.0
    stop_loss_pct: float = 0.02
    daily_loss_limit_pct: float = 0.05

@dataclass
class AgentConfig:
    enable_sentiment: bool = True
    enable_tuner: bool = True
    openai_api_key: str = ''

@dataclass
class RLConfig:
    enable: bool = False
    policy_path: str = ''

@dataclass
class DeFiConfig:
    enable: bool = False
    strategy: str = 'aave'
    defi_private_key: str = ''
    rpc_url: str = ''

@dataclass
class Config:
    exchange: ExchangeConfig
    trading: TradingConfig
    agents: AgentConfig
    rl: RLConfig
    defi: DeFiConfig


def load_config() -> Config:
    exchange = ExchangeConfig(
        name=os.getenv('EXCHANGE_NAME', 'phemex'),
        api_key=os.getenv('PHEMEX_API_KEY', ''),
        api_secret=os.getenv('PHEMEX_API_SECRET', ''),
        use_testnet=os.getenv('USE_TESTNET', 'true').lower() == 'true',
    )
    trading = TradingConfig(
        markets=os.getenv('MARKETS', 'BTC/USD').split(','),
        max_position_usd=float(os.getenv('MAX_POSITION_USD', 1000)),
        stop_loss_pct=float(os.getenv('STOP_LOSS_PCT', 0.02)),
        daily_loss_limit_pct=float(os.getenv('DAILY_LOSS_LIMIT_PCT', 0.05)),
    )
    agents = AgentConfig(
        enable_sentiment=os.getenv('ENABLE_SENTIMENT', 'true').lower() == 'true',
        enable_tuner=os.getenv('ENABLE_TUNER', 'true').lower() == 'true',
        openai_api_key=os.getenv('OPENAI_API_KEY', ''),
    )
    rl = RLConfig(
        enable=os.getenv('ENABLE_RL', 'false').lower() == 'true',
        policy_path=os.getenv('POLICY_PATH', ''),
    )
    defi = DeFiConfig(
        enable=os.getenv('ENABLE_DEFI', 'false').lower() == 'true',
        strategy=os.getenv('DEFI_STRATEGY', 'aave'),
        defi_private_key=os.getenv('DEFI_PRIVATE_KEY', ''),
        rpc_url=os.getenv('RPC_URL', ''),
    )
    return Config(exchange, trading, agents, rl, defi)
