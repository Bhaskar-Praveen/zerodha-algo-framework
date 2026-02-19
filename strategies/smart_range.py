import pandas as pd
import datetime


class SmartRangeEngine:

    def __init__(self, kite, config, option_type):
        self.kite = kite
        self.config = config
        self.option_type = option_type
        self.last_signal_state = False  # prevents repeated triggers

    def get_nifty_ema_separation(self):
        try:
            now = datetime.datetime.now()
            from_date = now - datetime.timedelta(days=10)

            data = self.kite.historical_data(
                instrument_token=self.config.nifty.instrument_token,
                from_date=from_date,
                to_date=now,
                interval="15minute"
            )

            df = pd.DataFrame(data)

            if len(df) < 63:
                return None

            df["ema21"] = df["close"].ewm(span=21, adjust=False).mean()
            df["ema63"] = df["close"].ewm(span=63, adjust=False).mean()

            latest = df.iloc[-1]
            sep = ((latest["ema21"] - latest["ema63"]) / latest["ema63"]) * 100

            return sep

        except Exception:
            return None

    def check_trend_direction(self):
        sep = self.get_nifty_ema_separation()
        if sep is None:
            return False

        threshold = self.config.strategy.ema_sep_threshold

        if self.option_type == "CE":
            return sep >= threshold
        else:
            return sep <= -threshold

    def evaluate(self):

        trend_now = self.check_trend_direction()

        # 🔥 Only trigger on transition
        if trend_now and not self.last_signal_state:
            self.last_signal_state = True
            return {
                "action": "BUY",
                "type": self.option_type
            }

        # Reset when trend disappears
        if not trend_now:
            self.last_signal_state = False

        return None
