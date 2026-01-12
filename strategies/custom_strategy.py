from core.strategy_base import Strategy

class SampleStrategy(Strategy):
    def generate_signal(self, data):
        return "HOLD"
