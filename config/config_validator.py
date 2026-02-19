# config/config_validator.py

EXPECTED_CONFIG_VERSION = "v4.1"


def _validate_positive_int(value, name):
    if not isinstance(value, int) or value <= 0:
        raise ValueError(f"[CONFIG ERROR] {name} must be positive integer.")


def _validate_percentage(value, name):
    if not isinstance(value, (int, float)) or not (0 < value < 1):
        raise ValueError(f"[CONFIG ERROR] {name} must be between 0 and 1.")


def _validate_number(value, name):
    if not isinstance(value, (int, float)):
        raise ValueError(f"[CONFIG ERROR] {name} must be numeric.")


def validate_config(config):
    """
    Structural + type + schema version validation.
    No mutation.
    No behavior change.
    """

    # ---- VERSION LOCK ----
    if not hasattr(config, "config_version"):
        raise ValueError("[CONFIG ERROR] Missing 'config_version'.")

    if config.config_version != EXPECTED_CONFIG_VERSION:
        raise ValueError(
            f"[CONFIG ERROR] Config version mismatch. "
            f"Expected {EXPECTED_CONFIG_VERSION}, "
            f"found {config.config_version}"
        )

    # ---- TRADE ----
    if not hasattr(config, "trade"):
        raise ValueError("[CONFIG ERROR] Missing 'trade' section.")

    _validate_positive_int(config.trade.lot_size, "trade.lot_size")
    _validate_positive_int(config.trade.lots, "trade.lots")

    # ---- RISK ----
    if not hasattr(config, "risk"):
        raise ValueError("[CONFIG ERROR] Missing 'risk' section.")

    _validate_percentage(config.risk.hard_sl_pct, "risk.hard_sl_pct")
    _validate_percentage(config.risk.early_sl_pct, "risk.early_sl_pct")
    _validate_number(config.risk.max_daily_loss, "risk.max_daily_loss")

    # ---- FILTERS ----
    if not hasattr(config, "filters"):
        raise ValueError("[CONFIG ERROR] Missing 'filters' section.")

    required_filters = [
        "volume_filter",
        "momentum_filter",
        "ema_separation",
        "correlation_filter",
        "extreme_move"
    ]

    for f in required_filters:
        if not hasattr(config.filters, f):
            raise ValueError(f"[CONFIG ERROR] Missing filters.{f}")

    return True
