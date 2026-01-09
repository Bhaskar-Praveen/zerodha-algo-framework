import os
import importlib
from broker.zerodha import ZerodhaBroker
from core.executor import TradeExecutor

STRATEGY_CLASS = os.getenv("STRATEGY_CLASS")

if not STRATEGY_CLASS:
    raise Exception("STRATEGY_CLASS env variable not set")

module_path, class_name = STRATEGY_CLASS.rsplit(".", 1)
strategy_module = importlib.import_module(module_path)
strategy = getattr(strategy_module, class_name)()

broker = ZerodhaBroker(
    api_key=os.getenv("ZERODHA_API_KEY"),
    access_token=os.getenv("ZERODHA_ACCESS_TOKEN")
)

engine = TradeExecutor(broker, strategy)
engine.run(market_data={})
