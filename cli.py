import argparse
import os
from dotenv import load_dotenv

from bot.client import BinanceFuturesClient
from bot.orders import OrderService
from bot.logging_config import setup_logger

logger = setup_logger()
load_dotenv()

def build_parser():
    parser = argparse.ArgumentParser(
        description="Binance Futures Testnet Trading Bot"
    )

    parser.add_argument("--symbol", required=True, help="Example: BTCUSDT")
    parser.add_argument("--side", required=True, help="BUY or SELL")
    parser.add_argument("--type", required=True, help="MARKET or LIMIT")
    parser.add_argument("--quantity", required=True, help="Order quantity")
    parser.add_argument("--price", required=False, help="Required for LIMIT order")

    return parser

def print_order_summary(args):
    print("\n========== ORDER REQUEST SUMMARY ==========")
    print(f"Symbol     : {args.symbol.upper()}")
    print(f"Side       : {args.side.upper()}")
    print(f"Type       : {args.type.upper()}")
    print(f"Quantity   : {args.quantity}")
    if args.price:
        print(f"Price      : {args.price}")
    print("==========================================\n")

def print_order_response(response):
    print("========== ORDER RESPONSE ==========")
    print(f"Order ID       : {response.get('orderId')}")
    print(f"Status         : {response.get('status')}")
    print(f"Executed Qty   : {response.get('executedQty')}")
    print(f"Average Price  : {response.get('avgPrice', 'N/A')}")
    print(f"Client Order ID: {response.get('clientOrderId')}")
    print("====================================")
    print("\n✅ Order placed successfully\n")

def main():
    parser = build_parser()
    args = parser.parse_args()

    try:
        print_order_summary(args)

        client = BinanceFuturesClient(
            api_key=os.getenv("BINANCE_API_KEY"),
            api_secret=os.getenv("BINANCE_API_SECRET"),
            base_url=os.getenv("BINANCE_BASE_URL", "https://testnet.binancefuture.com")
        )

        order_service = OrderService(client)

        response = order_service.create_order(
            symbol=args.symbol,
            side=args.side,
            order_type=args.type,
            quantity=args.quantity,
            price=args.price
        )

        print_order_response(response)

    except ValueError as error:
        logger.exception("Validation error")
        print(f"\n❌ Validation failed: {error}\n")

    except Exception as error:
        logger.exception("Order failed")
        print(f"\n❌ Order failed: {error}\n")

if __name__ == "__main__":
    main()