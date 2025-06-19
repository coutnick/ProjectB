from dataclasses import dataclass

from ..strategy.rules import Signal


@dataclass
class RiskSettings:
    max_position_usd: float
    stop_loss_pct: float


class RiskManager:
    def __init__(self, settings: RiskSettings):
        self.settings = settings
        self.position = 0.0

    def evaluate(self, signal: Signal) -> bool:
        # Simple check for max exposure
        proposed = self.position + signal.size * signal.price
        return proposed <= self.settings.max_position_usd

    def on_fill(self, signal: Signal):
        if signal.action == 'buy':
            self.position += signal.size * signal.price
        elif signal.action == 'sell':
            self.position -= signal.size * signal.price
