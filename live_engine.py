import logging
from datetime import datetime, timedelta
from kiteconnect import KiteConnect
from core.risk_manager import RiskManager


# ============================================================
# CONFIG
# ============================================================

class Config:
    API_KEY = "yn0licyrd92p1d1k"
    ACCESS_TOKEN = None

    NIFTY_LOT_SIZE = 65

    ENABLE_EARLY_SL = True
    EARLY_SL_PCT = 0.03
    EARLY_SL_DURATION_SECONDS = 180

    STOP_LOSS_PCT = 0.05

    PROFIT_LOCK_THRESHOLDS = [
        (0.15, 0.14),
        (0.20, 0.18),
        (0.30, 0.28),
    ]


# ============================================================
# KITE WRAPPER
# ============================================================

class KiteAPIManager:

    def __init__(self):
        self.kite = KiteConnect(api_key=Config.API_KEY)
        self.kite.set_access_token(Config.ACCESS_TOKEN)

    def get_ltp(self, symbol):
        data = self.kite.ltp(symbol)
        return list(data.values())[0]["last_price"]


# ============================================================
# STRATEGY
# ============================================================

class TradingStrategy:

    def __init__(self, kite):
        self.kite = kite
        self.position = None
        self.peak_profit_pct = 0
        self.risk = RiskManager(Config)

    def enter_position(self, symbol, price):
        self.position = {
            "symbol": symbol,
            "entry_price": price,
            "entry_time": datetime.now()
        }
        self.peak_profit_pct = 0
        logging.info(f"Entered at {price}")

    def check_exit_conditions(self, current_price):

        if not self.position:
            return

        entry_price = self.position["entry_price"]

        pnl_pct = self.risk.calculate_pnl_pct(entry_price, current_price)

        if pnl_pct > self.peak_profit_pct:
            self.peak_profit_pct = pnl_pct

        if self.risk.check_early_stop(self.position, pnl_pct):
            self.exit_position("Early SL", current_price)
            return

        if self.risk.check_hard_stop(pnl_pct, Config.STOP_LOSS_PCT):
            self.exit_position("Hard SL", current_price)
            return

        hit, lock_pct = self.risk.check_profit_locks(
            self.peak_profit_pct,
            pnl_pct
        )

        if hit:
            self.exit_position("Profit Lock", current_price)
            return

    def exit_position(self, reason, price):
        entry = self.position["entry_price"]
        pnl = ((price - entry) / entry) * 100
        logging.info(f"Exit: {reason} | PnL: {pnl:.2f}%")
        self.position = None
        self.peak_profit_pct = 0


# ============================================================
# MAIN
# ============================================================

def main():

    logging.basicConfig(level=logging.INFO)

    Config.ACCESS_TOKEN = input("Paste Access Token: ").strip()

    kite = KiteAPIManager()
    strategy = TradingStrategy(kite)

    print("Engine Booted Successfully")

    # Demo loop (replace with your signal logic)
    while True:
        symbol = "NSE:NIFTY 50"
        ltp = kite.get_ltp(symbol)

        if not strategy.position:
            strategy.enter_position(symbol, ltp)
        else:
            strategy.check_exit_conditions(ltp)


if __name__ == "__main__":
    main()
