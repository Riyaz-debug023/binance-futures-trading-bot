from decimal import Decimal, InvalidOperation

VALID_SIDES = {"BUY", "SELL"}
VALID_ORDER_TYPES = {"MARKET", "LIMIT"}

def validate_symbol(symbol: str) -> str:
    symbol = symbol.upper().strip()
    if not symbol or not symbol.endswith("USDT"):
        raise ValueError("Symbol must be a USDT-M Futures pair, example: BTCUSDT")
    return symbol

def validate_side(side: str) -> str:
    side = side.upper().strip()
    if side not in VALID_SIDES:
        raise ValueError("Side must be BUY or SELL")
    return side

def validate_order_type(order_type: str) -> str:
    order_type = order_type.upper().strip()
    if order_type not in VALID_ORDER_TYPES:
        raise ValueError("Order type must be MARKET or LIMIT")
    return order_type

def validate_positive_decimal(value: str, field_name: str) -> str:
    try:
        number = Decimal(str(value))
    except InvalidOperation:
        raise ValueError(f"{field_name} must be a valid number")

    if number <= 0:
        raise ValueError(f"{field_name} must be greater than 0")

    return str(number)

def validate_order_inputs(symbol, side, order_type, quantity, price=None):
    symbol = validate_symbol(symbol)
    side = validate_side(side)
    order_type = validate_order_type(order_type)
    quantity = validate_positive_decimal(quantity, "Quantity")

    if order_type == "LIMIT":
        if price is None:
            raise ValueError("Price is required for LIMIT orders")
        price = validate_positive_decimal(price, "Price")

    return symbol, side, order_type, quantity, price