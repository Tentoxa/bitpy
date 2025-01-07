import json
import time
import hmac
import base64
import hashlib
import asyncio
import websockets
from typing import Optional, List, Dict, Any, Callable

from ..models.login import BitgetCredentials
from ..utils.log_manager import LogManager


class BitgetWebsocketClient:
    def __init__(
            self,
            credentials: Optional[BitgetCredentials] = None,
            is_private: bool = False,
            debug: bool = False
    ):
        self.api_key = credentials.api_key if credentials else None
        self.secret_key = credentials.secret_key if credentials else None
        self.passphrase = credentials.api_passphrase if credentials else None
        self.debug = debug

        self.websocket = None
        self.connected = False
        self.subscriptions = set()
        self.callbacks = {}
        self._tasks = []
        self._should_reconnect = True

        self.is_private = is_private

        self.logger = LogManager(self, debug)
        self.logger.info("Initializing BitgetWebsocketClient")

        self.base_url = "wss://ws.bitget.com/v2/ws/"
        self.url = f"{self.base_url}{'private' if is_private else 'public'}"
        self.logger.debug(f"WebSocket URL set to: {self.url}")

    def _generate_signature(self, timestamp: int) -> str:
        """
        Generate HMAC SHA256 signature for authentication.

        Args:
            timestamp: Unix timestamp in seconds

        Returns:
            Base64 encoded signature
        """
        if not self.secret_key:
            raise ValueError("Secret key is required for signature generation")

        # Create the message string: timestamp + "GET" + "/user/verify"
        message = f"{timestamp}GET/user/verify"

        # Create the HMAC SHA256 signature
        hmac_obj = hmac.new(
            self.secret_key.encode('utf-8'),
            message.encode('utf-8'),
            hashlib.sha256
        )

        # Return base64 encoded signature
        return base64.b64encode(hmac_obj.digest()).decode('utf-8')

    async def _login(self) -> bool:
        """
        Perform login for private websocket connections.

        Returns:
            bool: True if login successful, False otherwise
        """
        if not all([self.api_key, self.secret_key, self.passphrase]):
            self.logger.error("Missing credentials for private connection")
            return False

        try:
            # Generate timestamp in seconds
            timestamp = int(time.time())

            # Generate signature
            signature = self._generate_signature(timestamp)

            # Construct login request
            login_request = {
                "op": "login",
                "args": [{
                    "apiKey": self.api_key,
                    "passphrase": self.passphrase,
                    "timestamp": str(timestamp),
                    "sign": signature
                }]
            }

            # Send login request
            self.logger.debug("Sending login request")
            await self.websocket.send(json.dumps(login_request))

            # Wait for login response
            response = await self.websocket.recv()
            response_data = json.loads(response)

            if response_data.get("event") == "login" and response_data.get("code") == "0":
                self.logger.info("Login successful")
                return True
            else:
                self.logger.error(f"Login failed: {response_data}")
                return False

        except Exception as e:
            self.logger.error(f"Login error: {str(e)}")
            return False

    async def _message_handler(self) -> None:
        self.logger.debug("Starting message handler")
        while self.connected:
            try:
                message = await self.websocket.recv()

                if message == "pong":
                    self.logger.debug("Pong received")
                    continue

                data = json.loads(message)
                self.logger.debug(f"Received message: {data}")

                if "event" in data:
                    if data["event"] == "login" and data.get("code") == "0":
                        self.logger.info("Successfully logged in")
                    continue

                channel = data.get("arg", {}).get("channel")
                if channel in self.callbacks:
                    self.logger.debug(f"Processing callback for channel: {channel}")
                    try:
                        await self.callbacks[channel](data)
                    except Exception as callback_error:
                        self.logger.error(f"Callback error for channel {channel}: {str(callback_error)}")
                        continue

            except websockets.ConnectionClosed:
                self.logger.warning("WebSocket connection closed")
                break
            except Exception as e:
                self.logger.error(f"Message handler error: {str(e)}")
                if not isinstance(e, asyncio.CancelledError):
                    continue

        self.logger.debug("Message handler ended")
        if self._should_reconnect:
            await self._reconnect()

    async def _reconnect(self) -> None:
        self.logger.info("Attempting to reconnect")
        self.connected = False

        while self._should_reconnect:
            try:
                await self.connect()
                # Resubscribe to previous subscriptions
                for sub in self.subscriptions:
                    sub_dict = json.loads(sub)
                    channel = sub_dict.get("channel")
                    if channel in self.callbacks:
                        await self.subscribe([sub_dict], self.callbacks[channel])
                break
            except Exception as e:
                self.logger.error(f"Reconnection failed: {str(e)}")
                await asyncio.sleep(5)

    async def _ping(self) -> None:
        self.logger.debug("Starting ping loop")
        while self.connected:
            try:
                await self.websocket.send("ping")
                self.logger.debug("Ping sent")
                await asyncio.sleep(30)
            except Exception as e:
                self.logger.error(f"Ping error: {str(e)}")
                break
        self.logger.debug("Ping loop ended")

    async def connect(self) -> None:
        if self.connected:
            return

        self.logger.info("Attempting to connect to WebSocket")
        try:
            self.websocket = await websockets.connect(self.url)
            self.connected = True
            self._should_reconnect = True
            self.logger.info("WebSocket connection established")

            if self.is_private:
                if not await self._login():
                    self.logger.error("Login failed, closing connection")
                    await self.close()
                    raise ConnectionError("Login failed")

            # Create background tasks
            ping_task = asyncio.create_task(self._ping())
            handler_task = asyncio.create_task(self._message_handler())

            # Store tasks for cleanup
            self._tasks.extend([ping_task, handler_task])

            self.logger.debug("Started background tasks")

        except Exception as e:
            self.logger.error(f"Connection error: {str(e)}")
            self.connected = False
            raise

    async def subscribe(self, subscriptions: List[Dict[str, str]], callback: Callable[[Dict], Any]) -> None:
        if not self.connected:
            self.logger.error("Cannot subscribe: WebSocket is not connected")
            raise ConnectionError("WebSocket is not connected")

        self.logger.info(f"Subscribing to channels: {subscriptions}")
        request = {
            "op": "subscribe",
            "args": subscriptions
        }

        for sub in subscriptions:
            channel = sub.get("channel")
            if channel:
                self.callbacks[channel] = callback
                self.subscriptions.add(json.dumps(sub))
                self.logger.debug(f"Added callback for channel: {channel}")

        await self.websocket.send(json.dumps(request))

    async def close(self) -> None:
        self.logger.info("Closing WebSocket connection")
        self._should_reconnect = False
        if self.connected:
            # Cancel all background tasks
            for task in self._tasks:
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    pass

            self._tasks.clear()
            await self.websocket.close()
            self.connected = False
            self.logger.debug("WebSocket connection closed")