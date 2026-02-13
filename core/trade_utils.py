from config.config_loader import CONFIG

def get_quantity():
    return CONFIG.trade.lot_size * CONFIG.trade.lots

def get_stop_loss_pct():
    return CONFIG.risk.stop_loss_pct
