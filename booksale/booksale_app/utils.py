
# Phương thức này sẽ được dùng để tính tông tiền hóa đơn
def sum_price_order(order_items_price):
    if not order_items_price:
        return 0
    return sum(order_items_price)