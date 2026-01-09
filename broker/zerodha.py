from kiteconnect import KiteConnect

class ZerodhaBroker:
    def __init__(self, api_key, access_token):
        self.kite = KiteConnect(api_key=api_key)
        self.kite.set_access_token(access_token)

    def place_order(self, symbol, side, quantity):
        print(f"[ORDER] {side} {symbol} x {quantity}")
