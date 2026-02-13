import json
import os
from datetime import datetime

STATE_FILE = "state.json"

def today():
    return datetime.now().strftime("%Y-%m-%d")

def default_state():
    return {
        "date": today(),
        "position": {
            "active": False
        },
        "daily_pnl": 0
    }

def load_state():
    if not os.path.exists(STATE_FILE):
        return default_state()

    with open(STATE_FILE) as f:
        state = json.load(f)

    if state.get("date") != today():
        return default_state()

    return state

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)
