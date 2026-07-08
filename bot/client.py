import time
import hmac
import hashlib
from urllib.parse import urlencode

import requests

from bot.logging_config import setup_logger

logger = setup_logger()

class BinanceFuturesClient:
    def __init__(self, api_key: str, api_secret: str, base_url: str):
        if not api_key or not api_secret:
            raise ValueError("API key and secret are required")

        self.api_key = api_key
        self.api_secret = api_secret.encode("utf-8")
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update({"X-MBX-APIKEY": self.api_key})
        self.time_offset = self._get_server_time_offset()

    def _get_server_time_offset(self):
        try:
            response = self.session.get(f"{self.base_url}/fapi/v1/time", timeout=10)
            response.raise_for_status()
            server_time = response.json()["serverTime"]
            local_time = int(time.time() * 1000)
            offset = server_time - local_time
            logger.info("Time sync completed | offset=%s ms", offset)
            return offset
        except Exception as error:
            logger.exception("Time sync failed")
            return 0

    def _sign_params(self, params: dict) -> dict:
        params["timestamp"] = int(time.time() * 1000) + self.time_offset
        params["recvWindow"] = 10000

        query_string = urlencode(params)
        signature = hmac.new(
            self.api_secret,
            query_string.encode("utf-8"),
            hashlib.sha256
        ).hexdigest()

        params["signature"] = signature
        return params

    def _request(self, method: str, endpoint: str, params=None, signed=False):
        params = params or {}

        if signed:
            params = self._sign_params(params)

        url = f"{self.base_url}{endpoint}"

        try:
            logger.info("API Request | %s %s | params=%s", method, endpoint, params)

            response = self.session.request(
                method=method,
                url=url,
                params=params,
                timeout=15
            )

            try:
                data = response.json()
            except ValueError:
                data = {"raw_response": response.text}

            logger.info("API Response | status=%s | data=%s", response.status_code, data)

            if response.status_code >= 400:
                raise Exception(f"Binance API Error: {data}")

            return data

        except requests.exceptions.RequestException as error:
            logger.exception("Network error: %s", error)
            raise Exception(f"Network error: {error}") from error

    def place_order(self, symbol, side, order_type, quantity, price=None):
        params = {
            "symbol": symbol,
            "side": side,
            "type": order_type,
            "quantity": quantity,
        }

        if order_type == "LIMIT":
            params["price"] = price
            params["timeInForce"] = "GTC"

        return self._request(
            method="POST",
            endpoint="/fapi/v1/order",
            params=params,
            signed=True
        )