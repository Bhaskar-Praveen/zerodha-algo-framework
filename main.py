import datetime

from core.logging_setup import setup_logger
from core.trade_utils import get_quantity, get_stop_loss_pct
from core.state_manager import load_state, save_state
from core.summary import append_trade, generate_eod_summary
from core.version import BOT_VERSION
from core.constants import EXIT_REASONS
from config.config_loader import CONFIG
from strategies.smart_range import generate_signal

logger = setup_logger()
logger.info(f"Starting Bot Version {BOT_VERSION}")

state = load_state()

if not state["position"]["active"]:

    signal = generate_signal()

    if signal["action"] == "BUY":

        quantity = get_quantity()
        sl_pct = get_stop_loss_pct()

        entry_price = signal["entry_price"]
        exit_price = entry_price * (1 - sl_pct)

        pnl = (exit_price - entry_price) * quantity

        row = [
            datetime.datetime.now().strftime("%Y-%m-%d"),
            BOT_VERSION,
            signal["expiry"],
            signal["strike"],
            signal["type"],
            "10:32:14",
            "11:05:22",
            entry_price,
            exit_price,
            quantity,
            pnl,
            "HARD_SL"
        ]

        append_trade(row)

        logger.info("Trade executed and logged")

summary = generate_eod_summary()
print(summary)
