class Config:
    LOT_SIZE = 65  # Add this line
    # ... other existing variables

EXIT_REASONS = {
    "HARD_SL": "Hard Stop Loss",
    "EOD": "End Of Day Exit",
    "DRAWDOWN": "Daily Drawdown",
    "MANUAL": "Manual Exit"
}
