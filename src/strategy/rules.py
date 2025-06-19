from dataclasses import dataclass
from typing import Optional

import pandas as pd


@dataclass
class Signal:
    action: str  # 'buy', 'sell', 'hold'
    price: float
    size: float


def simple_moving_average_strategy(df: pd.DataFrame) -> Optional[Signal]:
    if len(df) < 21:
        return None
    last = df.iloc[-1]
    prev = df.iloc[-2]

    if prev['close'] < prev['ema_20'] and last['close'] > last['ema_20']:
        return Signal('buy', last['close'], size=1)
    if prev['close'] > prev['ema_20'] and last['close'] < last['ema_20']:
        return Signal('sell', last['close'], size=1)
    return None
