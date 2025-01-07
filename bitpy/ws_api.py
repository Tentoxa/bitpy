from typing import Optional
from .clients.ws import BitgetWebsocketClient

from .models.login import BitgetCredentials

from .utils.log_manager import LogManager


class BitgetWebsocketAPI:
    def __init__(self, api_key: Optional[str] = None, secret_key: Optional[str] = None,
                 api_passphrase: Optional[str] = None, is_private: bool = False, debug: bool = False):
        credentials = BitgetCredentials(api_key, secret_key, api_passphrase)
        if is_private:
            print("Private API is not supported yet")
            return

        self.websocket = BitgetWebsocketClient(credentials, is_private, debug)

        logger = LogManager(self, debug)

        if not all([api_key, secret_key, api_passphrase]):
            if debug:
                logger.debug("Warning: Websocket API initialized without full authentication. Only public endpoints will be "
                             "available.")