from bot.validators import validate_order_inputs

class OrderService:
    def __init__(self, client):
        self.client = client

    def create_order(self, symbol, side, order_type, quantity, price=None):
        symbol, side, order_type, quantity, price = validate_order_inputs(
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=quantity,
            price=price
        )

        return self.client.place_order(
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=quantity,
            price=price
        )