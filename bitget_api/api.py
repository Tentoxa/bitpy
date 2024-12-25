from .clients.position import BitgetPositionClient
from .utils.request_handler import RequestHandler


class BitgetAPI:
    def __init__(self, api_key: str, secret_key: str, api_passphrase: str, base_url: str = "https://api.bitget.com",
                 debug: bool = False):
        request_handler = RequestHandler(api_key, secret_key, api_passphrase, base_url, debug)

        self.position = BitgetPositionClient(request_handler, debug)