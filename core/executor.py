class TradeExecutor:
    def __init__(self, broker, strategy):
        self.broker = broker
        self.strategy = strategy

    def run(self, market_data):
        signal = self.strategy.generate_signal(market_data)

        if signal == "BUY":
            self.broker.place_order("NIFTY", "BUY", 1)
        elif signal == "SELL":
            self.broker.place_order("NIFTY", "SELL", 1)
        else:
            print("[INFO] HOLD signal")
