import yaml
from types import SimpleNamespace

def _to_namespace(d):
    if isinstance(d, dict):
        return SimpleNamespace(**{k: _to_namespace(v) for k, v in d.items()})
    return d

def load_config():
    with open("config/config.yaml") as f:
        return _to_namespace(yaml.safe_load(f))

CONFIG = load_config()
