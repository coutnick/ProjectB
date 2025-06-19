import pandas as pd
from ta.trend import EMAIndicator
from ta.momentum import RSIIndicator


def compute_indicators(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df['ema_20'] = EMAIndicator(close=df['close'], window=20).ema_indicator()
    df['rsi_14'] = RSIIndicator(close=df['close'], window=14).rsi()
    return df
