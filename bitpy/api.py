from .clients.position import BitgetPositionClient
from .clients.market import BitgetMarketClient
from .clients.account import BitgetAccountClient
from .utils.log_manager import LogManager

from .utils.request_handler import RequestHandler
from typing import Optional


class BitgetAPI:
    def __init__(self, api_key: Optional[str] = None, secret_key: Optional[str] = None,
                 api_passphrase: Optional[str] = None, base_url: str = "https://api.bitget.com",
                 debug: bool = False):
        request_handler = RequestHandler(base_url, api_key, secret_key, api_passphrase, debug)
        logger = LogManager(self, debug)

        self.position = BitgetPositionClient(request_handler, debug)
        self.market = BitgetMarketClient(request_handler, debug)
        self.account = BitgetAccountClient(request_handler, debug)

        if not all([api_key, secret_key, api_passphrase]):
            if debug:
                logger.debug("Warning: API initialized without full authentication. Only public endpoints will be "
                             "available.")