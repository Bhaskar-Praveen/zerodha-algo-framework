import time
import datetime
import sys

from core.logging_setup import setup_logger
from core.state_manager import load_state, save_state
from core.trade_utils import get_quantity, get_stop_loss_pct
from core.summary import append_trade, generate_eod_summary
from core.version import BOT_VERSION
from config.config_loader import CONFIG

from broker.kite_client import get_kite
from broker.execution import place_market_order
from core.order_manager import wait_for_completion

from strategies.smart_range import generate_signal


# -----------------------------
# INITIALIZATION
# -----------------------------

logger = setup_logger()
logger.info(f"Starting Bot Version {BOT_VERSION}")

state = load_state()

# Initialize Kite
# Replace with your real key/token source
API_KEY = "YOUR_API_KEY"
ACCESS_TOKEN = "YOUR_ACCESS_TOKEN"

kite = get_kite(API_KEY, ACCESS_TOKEN)


# -----------------------------
# MAIN LOOP
# -----------------------------

def market_open():
    now = datetime.datetime.now().time()
    return now >= datetime.time(9, 15) and now <= datetime.time(15, 25)


def is_eod():
    now = datetime.datetime.now().time()
    return now >= datetime.time(15, 25)


try:

    while True:

        if not market_open():
            time.sleep(10)
            continue

        # -------------------------
        # ENTRY LOGIC
        # -------------------------

        if not state["position"]["active"]:

            signal = generate_signal()

            if signal and signal["action"] == "BUY":

                quantity = get_quantity()

                logger.info(f"Placing order: {signal}")

                order_id = place_market_order(
                    kite,
                    signal["symbol"],
                    quantity,
                    "BUY"
                )

                order_details = wait_for_completion(kite, order_id)

                entry_price = order_details["average_price"]

                state["position"] = {
                    "active": True,
                    "symbol": signal["symbol"],
                    "expiry": signal["expiry"],
                    "strike": signal["strike"],
                    "type": signal["type"],
                    "qty": quantity,
                    "entry_price": entry_price,
                    "order_id": order_id,
                    "entry_time": datetime.datetime.now().isoformat()
                }

                save_state(state)

                logger.info("Position opened successfully")

        # -------------------------
        # POSITION MONITORING
        # -------------------------

        if state["position"]["active"]:

            # Fetch LTP
            ltp = kite.ltp(state["position"]["symbol"])
            current_price = list(ltp.values())[0]["last_price"]

            entry_price = state["position"]["entry_price"]
            sl_pct = get_stop_loss_pct()
            sl_price = entry_price * (1 - sl_pct)

            # HARD SL
            if current_price <= sl_price:

                logger.info("Hard SL triggered")

                order_id = place_market_order(
                    kite,
                    state["position"]["symbol"],
                    state["position"]["qty"],
                    "SELL"
                )

                exit_details = wait_for_completion(kite, order_id)

                exit_price = exit_details["average_price"]

                pnl = (exit_price - entry_price) * state["position"]["qty"]

                append_trade([
                    datetime.datetime.now().strftime("%Y-%m-%d"),
                    BOT_VERSION,
                    state["position"]["expiry"],
                    state["position"]["strike"],
                    state["position"]["type"],
                    state["position"]["entry_time"],
                    datetime.datetime.now().isoformat(),
                    entry_price,
                    exit_price,
                    state["position"]["qty"],
                    pnl,
                    "HARD_SL"
                ])

                state["position"]["active"] = False
                save_state(state)

                logger.info(f"Position closed. PnL: {pnl}")

        # -------------------------
        # EOD FORCED EXIT
        # -------------------------

        if is_eod() and state["position"]["active"]:

            logger.info("EOD exit triggered")

            order_id = place_market_order(
                kite,
                state["position"]["symbol"],
                state["position"]["qty"],
                "SELL"
            )

            exit_details = wait_for_completion(kite, order_id)

            exit_price = exit_details["average_price"]

            pnl = (exit_price - state["position"]["entry_price"]) * state["position"]["qty"]

            append_trade([
                datetime.datetime.now().strftime("%Y-%m-%d"),
                BOT_VERSION,
                state["position"]["expiry"],
                state["position"]["strike"],
                state["position"]["type"],
                state["position"]["entry_time"],
                datetime.datetime.now().isoformat(),
                state["position"]["entry_price"],
                exit_price,
                state["position"]["qty"],
                pnl,
                "EOD"
            ])

            state["position"]["active"] = False
            save_state(state)

            summary = generate_eod_summary()
            logger.info(summary)
            print(summary)

            break

        time.sleep(1)

except Exception as e:
    logger.exception("Fatal error occurred")
    sys.exit(1)
