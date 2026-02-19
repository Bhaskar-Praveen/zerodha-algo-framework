from datetime import datetime
import logging
import threading

# ------------------------------------------------------------
# 1. LOAD YAML CONFIG
# ------------------------------------------------------------
from config.config_adapter import load_yaml_config
load_yaml_config()

# ------------------------------------------------------------
# 2. VALIDATE CONFIG (NEW SAFE LAYER)
# ------------------------------------------------------------
from config.config_loader import CONFIG
from config.config_validator import validate_config

try:
    validate_config(CONFIG)
    logging.info("✅ Config validation passed.")
except Exception as e:
    logging.error(str(e))
    raise SystemExit(1)

# ------------------------------------------------------------
# 3. IMPORT LIVE ENGINE AFTER VALIDATION
# ------------------------------------------------------------
from live_engine import (
    Config,
    KiteAPIManager,
    TradingStrategy,
    get_next_expiry,
    wait_until_market_open,
    exit_if_market_closed,
    load_state,
    save_state
)

# ============================================================
# MAIN ENTRY POINT
# ============================================================

def main():

    logging.info("="*80)
    logging.info("🚀 STARTING 4.7.5.1 LIVE ENGINE")
    logging.info("="*80)

    # --------------------------------------------------------
    # 1. ACCESS TOKEN INPUT (LIVE MODE)
    # --------------------------------------------------------
    Config.ACCESS_TOKEN = input("🔑 Paste Zerodha Access Token: ").strip()

    if not Config.ACCESS_TOKEN:
        logging.error("❌ Access token missing.")
        return

    # --------------------------------------------------------
    # 2. WAIT FOR MARKET OPEN
    # --------------------------------------------------------
    wait_until_market_open()

    # --------------------------------------------------------
    # 3. INITIALIZE KITE API
    # --------------------------------------------------------
    kite_manager = KiteAPIManager()

    instruments = kite_manager.load_instruments()
    if instruments is None:
        logging.error("❌ Failed to load instruments.")
        return

    expiry = get_next_expiry(instruments)
    if not expiry:
        logging.error("❌ Could not determine expiry.")
        return

    # --------------------------------------------------------
    # 4. INITIALIZE STRATEGIES (INDEPENDENT CE & PE)
    # --------------------------------------------------------
    ce_strategy = TradingStrategy(kite_manager, instruments, expiry, "CE")
    pe_strategy = TradingStrategy(kite_manager, instruments, expiry, "PE")

    # Restore state
    load_state(ce_strategy, "CE")
    load_state(pe_strategy, "PE")

    # Force initial strike selection
    ce_strategy.update_strike_if_needed(force=True)
    pe_strategy.update_strike_if_needed(force=True)

    # --------------------------------------------------------
    # 5. MAIN LOOP
    # --------------------------------------------------------
    logging.info("✅ Engine running...")

    while True:

        now = datetime.now()

        # Exit if market closed
        if now.hour == 15 and now.minute >= 25:
            logging.info("🛑 Market closing. Exiting positions.")

            if ce_strategy.position:
                ce_strategy.exit_position("EOD")
            if pe_strategy.position:
                pe_strategy.exit_position("EOD")

            save_state(ce_strategy, "CE")
            save_state(pe_strategy, "PE")

            break

        # Update strikes dynamically
        ce_strategy.update_strike_if_needed()
        pe_strategy.update_strike_if_needed()

        # Check CE Entry
        if not ce_strategy.position:
            if ce_strategy.check_entry_conditions():
                ce_strategy.enter_position()

        # Check PE Entry
        if not pe_strategy.position:
            if pe_strategy.check_entry_conditions():
                pe_strategy.enter_position()

        # Monitor CE
        if ce_strategy.position:
            ce_strategy.monitor_position()

        # Monitor PE
        if pe_strategy.position:
            pe_strategy.monitor_position()

        # Save state every loop
        save_state(ce_strategy, "CE")
        save_state(pe_strategy, "PE")

        # Loop delay
        threading.Event().wait(5)


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    main()
