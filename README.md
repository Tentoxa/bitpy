# 🚀 Bitget API V2 Python Client

A comprehensive Python client for the Bitget API V2, providing extensive functionality for futures trading, account management, and market data access.

## ✨ Features

- 📊 Complete futures market trading capabilities
- 💼 Account management and settings
- 📈 Real-time and historical market data
- 🔄 Automatic rate limiting and request handling
- 🛡️ Comprehensive error handling and validation
- 📝 Detailed debug logging capabilities
- 🎯 Type hints and dataclass models for better code completion

## 🛠️ Installation

```bash
# Install using PYPI
pip install bitget-python
```

## 🔧 Quick Start

```python
from bitpy import BitgetAPI

# For market data only - no API keys needed
client = BitgetAPI(
    api_key=None,
    secret_key=None,
    api_passphrase=None
)

# Get market data without authentication
ticker = client.market.get_ticker(
    symbol="BTCUSDT",
    product_type="USDT-FUTURES"
)

# Get candlestick data
candles = client.market.get_candlestick(
    symbol="BTCUSDT",
    product_type="USDT-FUTURES",
    granularity="1m",
    limit=100
)
```

For account and position operations, API keys are required:

```python
# For trading operations - API keys required
client = BitgetAPI(
    api_key="your_api_key",
    secret_key="your_secret_key",
    api_passphrase="your_passphrase",
    debug=True
)

# Get account information (requires authentication)
account = client.account.get_account(
    symbol="BTCUSDT",
    product_type="USDT-FUTURES",
    margin_coin="USDT"
)
```

## 🌐 WebSocket Support (Only Public)

```python
from bitpy import BitgetWebsocketAPI
import asyncio

async def handle_ticker(data: dict):
    if "data" in data and len(data["data"]) > 0:
        ticker = data["data"][0]
        print(f"Symbol: {ticker['instId']}")
        print(f"Last Price: {ticker['lastPr']}")
        print(f"24h High: {ticker['high24h']}")
        print(f"24h Low: {ticker['low24h']}")
        print(f"24h Change %: {ticker['change24h']}")
        print("-" * 50)
        
async def main():
    # Initialize WebSocket client
    api = BitgetWebsocketAPI(is_private=False, debug=False)
    ws_client = api.websocket
    # Subscribe to channels
    subscriptions = [
        {
            "instType": "SPOT",
            "channel": "ticker",
            "instId": "BTCUSDT"
        }
    ]
    try:
        await ws_client.connect()
        print("Connected to WebSocket")
        await ws_client.subscribe(subscriptions, handle_ticker)
        # Keep connection alive
        while ws_client.connected:
            await asyncio.sleep(1)
            
    except KeyboardInterrupt:
        await ws_client.close()
        
if __name__ == "__main__":
    asyncio.run(main())
```

## 🔑 Core Components

**Account Management**
- Account information and settings
- Leverage and margin configuration
- Position mode management
- Asset mode settings
- Interest and bill history

**Position Management**
- Position tracking and history
- Position tier information
- Multiple position modes support

**Market Data**
- Real-time tickers and depth
- Candlestick data with multiple timeframes
- Funding rates and open interest
- Historical transaction data
- Contract specifications

## 💹 Supported Markets

| Market Type | Description |
|------------|-------------|
| USDT-FUTURES | USDT margined futures |
| COIN-FUTURES | Coin margined futures |
| USDC-FUTURES | USDC margined futures |
| SUSDT-FUTURES| Simulated USDT futures |
| SCOIN-FUTURES| Simulated coin futures |
| SUSDC-FUTURES| Simulated USDC futures |

## ⚠️ Error Handling

```python
from bitpy.exceptions import InvalidProductTypeError, BitgetAPIError

try:
    positions = client.position.get_all_positions("INVALID-TYPE")
except InvalidProductTypeError as e:
    print(f"Invalid product type: {e}")
except BitgetAPIError as e:
    print(f"API Error {e.code}: {e.message}")
```

## 🔄 Rate Limiting

The client implements a smart token bucket algorithm for rate limiting, automatically tracking and managing request limits per endpoint to ensure optimal API usage.

## 📊 Advanced Market Data

```python
# Get candlestick data
candles = client.market.get_candlestick(
    symbol="BTCUSDT",
    product_type="USDT-FUTURES",
    granularity="1m",
    limit=100
)

# Get market depth
depth = client.market.get_merge_depth(
    symbol="BTCUSDT",
    product_type="USDT-FUTURES",
    precision="0.1"
)
```

## 🤝 Contributing

Contributions are welcome! Feel free to submit a Pull Request. For feature requests or bug reports, please open an issue.

## 📄 License

This project is licensed under the MIT License. 