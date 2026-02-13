import time

def wait_for_completion(kite, order_id, timeout=10):

    start = time.time()

    while time.time() - start < timeout:

        orders = kite.orders()

        for order in orders:
            if order["order_id"] == order_id:

                status = order["status"]

                if status == "COMPLETE":
                    return order

                if status in ["REJECTED", "CANCELLED"]:
                    raise Exception(order.get("status_message"))

        time.sleep(1)

    raise Exception("Order Timeout")
