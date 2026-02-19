import yaml
from live_engine import Config


def load_yaml_config():

    with open("config/config.yaml", "r") as f:
        data = yaml.safe_load(f) or {}

    # -----------------------------
    # SAFE ACCESS HELPER
    # -----------------------------

    def get(d, *keys, default=None):
        for key in keys:
            if not isinstance(d, dict):
                return default
            d = d.get(key, {})
        return d if d != {} else default

    # -----------------------------
    # TRADE SETTINGS
    # -----------------------------

    Config.LOT_SIZE = get(data, "trade", "lot_size", default=Config.LOT_SIZE)
    Config.LOTS = get(data, "trade", "lots", default=Config.LOTS)

    # -----------------------------
    # RISK SETTINGS
    # -----------------------------

    Config.HARD_SL_PCT = get(data, "risk", "hard_sl_pct", default=Config.HARD_SL_PCT)
    Config.EARLY_SL_PCT = get(data, "risk", "early_sl_pct", default=Config.EARLY_SL_PCT)
    Config.MAX_DAILY_LOSS = get(data, "risk", "max_daily_loss", default=Config.MAX_DAILY_LOSS)

    # -----------------------------
    # FILTERS
    # -----------------------------

    Config.ENABLE_VOLUME_FILTER = get(data, "filters", "volume_filter", "enabled", default=Config.ENABLE_VOLUME_FILTER)
    Config.VOLUME_SPIKE_THRESHOLD = get(data, "filters", "volume_filter", "spike_threshold", default=Config.VOLUME_SPIKE_THRESHOLD)

    Config.ENABLE_MOMENTUM_FILTER = get(data, "filters", "momentum_filter", "enabled", default=Config.ENABLE_MOMENTUM_FILTER)
    Config.MOMENTUM_THRESHOLD = get(data, "filters", "momentum_filter", "threshold", default=Config.MOMENTUM_THRESHOLD)

    Config.ENABLE_EMA_SEPARATION = get(data, "filters", "ema_separation", "enabled", default=Config.ENABLE_EMA_SEPARATION)
    Config.EMA_SEPARATION_THRESHOLD = get(data, "filters", "ema_separation", "threshold_pct", default=Config.EMA_SEPARATION_THRESHOLD)

    Config.ENABLE_CORRELATION_FILTER = get(data, "filters", "correlation_filter", "enabled", default=Config.ENABLE_CORRELATION_FILTER)

    Config.ENABLE_EXTREME_MOVE = get(data, "filters", "extreme_move", "enabled", default=Config.ENABLE_EXTREME_MOVE)
    Config.EXTREME_MOVE_EMA_THRESHOLD = get(data, "filters", "extreme_move", "ema_threshold", default=Config.EXTREME_MOVE_EMA_THRESHOLD)
    Config.EXTREME_MOVE_MOMENTUM_THRESHOLD = get(data, "filters", "extreme_move", "momentum_threshold", default=Config.EXTREME_MOVE_MOMENTUM_THRESHOLD)

    # ============================================================
    # VALIDATION LAYER (NEW)
    # ============================================================

    validate_config()


def validate_config():
    """
    Fail fast if configuration is dangerous or invalid.
    This prevents capital destruction due to bad YAML edits.
    """

    errors = []

    # -----------------------------
    # LOT VALIDATION
    # -----------------------------
    if Config.LOT_SIZE <= 0:
        errors.append("LOT_SIZE must be > 0")

    if Config.LOTS <= 0:
        errors.append("LOTS must be > 0")

    # -----------------------------
    # STOP LOSS VALIDATION
    # -----------------------------
    if not 0 < Config.HARD_SL_PCT < 0.5:
        errors.append("HARD_SL_PCT must be between 0 and 0.5 (0%–50%)")

    if not 0 < Config.EARLY_SL_PCT < 0.5:
        errors.append("EARLY_SL_PCT must be between 0 and 0.5 (0%–50%)")

    if Config.EARLY_SL_PCT >= Config.HARD_SL_PCT:
        errors.append("EARLY_SL_PCT must be smaller than HARD_SL_PCT")

    # -----------------------------
    # EXTREME MOVE VALIDATION
    # -----------------------------
    if Config.EXTREME_MOVE_EMA_THRESHOLD <= 0:
        errors.append("EXTREME_MOVE_EMA_THRESHOLD must be positive")

    if Config.EXTREME_MOVE_MOMENTUM_THRESHOLD <= 0:
        errors.append("EXTREME_MOVE_MOMENTUM_THRESHOLD must be positive")

    # -----------------------------
    # MAX DAILY LOSS VALIDATION
    # -----------------------------
    if Config.MAX_DAILY_LOSS >= 0:
        errors.append("MAX_DAILY_LOSS must be negative (e.g., -3000)")

    # -----------------------------
    # FINAL CHECK
    # -----------------------------
    if errors:
        print("\n" + "=" * 80)
        print("❌ CONFIG VALIDATION FAILED")
        print("=" * 80)
        for err in errors:
            print("  -", err)
        print("=" * 80)
        raise ValueError("Invalid configuration. Fix config.yaml before running.")
