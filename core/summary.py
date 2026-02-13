import csv
import os
from datetime import datetime

os.makedirs("data", exist_ok=True)

FILE = "data/trade_history.csv"

def append_trade(row):

    file_exists = os.path.exists(FILE)

    with open(FILE, "a", newline="") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow([
                "date","version","expiry","strike","type",
                "entry_time","exit_time",
                "entry_price","exit_price",
                "qty","pnl","reason"
            ])

        writer.writerow(row)

def generate_eod_summary():

    today = datetime.now().strftime("%Y-%m-%d")
    total = 0
    trades = []

    if not os.path.exists(FILE):
        return "No trades today."

    with open(FILE) as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["date"] == today:
                trades.append(row)
                total += float(row["pnl"])

    summary = f"EOD Summary - {today}\n\n"

    for t in trades:
        summary += (
            f"{t['strike']} {t['type']} | Exp: {t['expiry']}\n"
            f"Entry: {t['entry_time']} Exit: {t['exit_time']}\n"
            f"Reason: {t['reason']} PnL: {t['pnl']}\n\n"
        )

    summary += f"Total PnL: {total}"

    return summary
