import requests
import base64
import hmac
from datetime import datetime
from typing import Optional, Dict, Any
from .log_manager import LogManager
from time import time
from collections import defaultdict
from ..exceptions import RequestError


class RateLimiter:
    def __init__(self, logger: LogManager):
        self.endpoint_limits = defaultdict(lambda: {
            "tokens": None,
            "last_update": time(),
            "max_tokens": None
        })
        self.logger = logger

    def update_limit(self, endpoint: str, remaining_limit: int):
        current = time()
        limit_info = self.endpoint_limits[endpoint]
        old_tokens = limit_info["tokens"]
        limit_info["tokens"] = remaining_limit
        limit_info["last_update"] = current

        current_max = limit_info.get("max_tokens")
        limit_info["max_tokens"] = max(remaining_limit, current_max if current_max is not None else 0)

        self.logger.debug(f"Rate limit updated for {endpoint}: {old_tokens} -> {remaining_limit} tokens")

    def acquire(self, endpoint: str) -> bool:
        limit_info = self.endpoint_limits[endpoint]
        current = time()

        # If we have a rate limit and it's been more than 1 second since last update
        if limit_info["tokens"] is not None:
            time_passed = current - limit_info["last_update"]
            if time_passed >= 1.0:  # Rate limit resets every second
                limit_info["tokens"] = limit_info["max_tokens"]
                limit_info["last_update"] = current
                self.logger.debug(f"Rate limit reset for {endpoint}. New tokens: {limit_info['tokens']}")
                return True

            if limit_info["tokens"] <= 0:
                self.logger.debug(f"No tokens available for {endpoint}. Time until reset: {1.0 - time_passed:.2f}s")
                return False

        return True


class RequestHandler:
    def __init__(self, api_key: str, secret_key: str, api_passphrase: str, base_url: str, debug: bool = False):
        self.api_key = api_key
        self.secret_key = secret_key
        self.api_passphrase = api_passphrase
        self.base_url = base_url.rstrip('/')
        self.debug = debug
        self.session = requests.Session()
        self.logger = LogManager(self, debug)
        self.rate_limiter = RateLimiter(self.logger)

    def _get_headers(self, method: str, request_path: str, query_string: str = "", body: str = "") -> dict:
        timestamp = str(int(datetime.now().timestamp() * 1000))
        signature = self._generate_signature(timestamp, method, request_path, query_string, body)

        headers = {
            "ACCESS-KEY": self.api_key,
            "ACCESS-SIGN": signature,
            "ACCESS-TIMESTAMP": timestamp,
            "ACCESS-PASSPHRASE": self.api_passphrase,
            "Content-Type": "application/json",
            "locale": "en-US"
        }
        return headers

    def _generate_signature(self, timestamp: str, method: str, request_path: str, query_string: str = "",
                            body: str = "") -> str:
        message = timestamp + method.upper() + request_path
        if query_string:
            message += "?" + query_string
        if body:
            message += body

        signature = base64.b64encode(
            hmac.new(
                self.secret_key.encode('utf-8'),
                message.encode('utf-8'),
                digestmod='sha256'
            ).digest()
        ).decode('utf-8')
        return signature

    def request(self, method: str, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict:
        query_string = "&".join(f"{k}={v}" for k, v in sorted(params.items())) if params else ""
        headers = self._get_headers(method, endpoint, query_string)

        url = f"{self.base_url}{endpoint}"
        if query_string:
            url += f"?{query_string}"

        while True:
            self.logger.debug(f"Checking rate limit for endpoint: {endpoint}")
            if self.rate_limiter.acquire(endpoint):
                try:
                    self.logger.debug("Rate limit check passed, sending request")
                    response = self.session.request(method, url, headers=headers)
                    self.logger.debug(f"Response status code: {response.status_code}")
                    self.logger.debug(f"Response headers: {response.headers}")

                    remaining_limit = int(response.headers.get('x-mbx-used-remain-limit', 0))
                    self.logger.debug(f"Remaining rate limit: {remaining_limit}")
                    self.rate_limiter.update_limit(endpoint, remaining_limit)

                    if response.status_code == 429:
                        self.logger.debug("Rate limit (429) response received, retrying")
                        self.rate_limiter.update_limit(endpoint, 0)
                        continue

                    self.logger.debug(f"Response content: {response.content}")
                    response_data = response.json()
                    self.logger.debug(f"Response data: {response_data}")

                    if response_data.get("code") != "00000":
                        raise RequestError(response_data.get("msg", "Unknown error"))

                    return response_data

                except requests.exceptions.RequestException as e:
                    self.logger.error(f"Request failed: {str(e)}")
                    self.logger.error(f"Full error details: {e.__class__.__name__}: {str(e)}")
                    raise
