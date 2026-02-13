import logging
import os
from datetime import datetime
from core.version import BOT_VERSION

def setup_logger():

    os.makedirs("logs/trading", exist_ok=True)

    date_str = datetime.now().strftime("%Y-%m-%d")
    log_file = f"logs/trading/{date_str}.log"

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    handler = logging.FileHandler(log_file)
    formatter = logging.Formatter(
        f'%(asctime)s | {BOT_VERSION} | %(levelname)s | %(message)s'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger
