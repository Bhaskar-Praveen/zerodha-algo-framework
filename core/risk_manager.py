from datetime import datetime

class RiskManager:

    def __init__(self, config):
        self.config = config

    def calculate_pnl_pct(self, entry_price, current_price):
        return ((current_price - entry_price) / entry_price) * 100

    def check_early_stop(self, position, pnl_pct):
        if not self.config.ENABLE_EARLY_SL:
            return False

        time_in_trade = (datetime.now() - position["entry_time"]).total_seconds()

        if time_in_trade <= self.config.EARLY_SL_DURATION_SECONDS:
            if pnl_pct <= -self.config.EARLY_SL_PCT * 100:
                return True

        return False

    def check_hard_stop(self, pnl_pct, sl_pct):
        return pnl_pct <= -sl_pct * 100

    def check_profit_locks(self, peak_profit_pct, pnl_pct):
        for threshold, lock in self.config.PROFIT_LOCK_THRESHOLDS:
            if peak_profit_pct >= threshold * 100:
                if pnl_pct <= lock * 100:
                    return True, lock
        return False, None
