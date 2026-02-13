def place_market_order(kite, symbol, qty, side):
    return kite.place_order(
        variety=kite.VARIETY_REGULAR,
        exchange="NFO",
        tradingsymbol=symbol,
        transaction_type=side,
        quantity=qty,
        order_type=kite.ORDER_TYPE_MARKET,
        product=kite.PRODUCT_MIS
    )
