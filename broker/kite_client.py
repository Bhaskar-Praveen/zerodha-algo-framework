from kiteconnect import KiteConnect

def get_kite(api_key, access_token):

    kite = KiteConnect(api_key=api_key)
    kite.set_access_token(access_token)

    return kite
