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

## 🔧 Quick Start

```python
from bitget_api import BitgetAPI

# Initialize the client
client = BitgetAPI(
    api_key="your_api_key",
    secret_key="your_secret_key",
    api_passphrase="your_passphrase",
    debug=True
)

# Get market data
ticker = client.market.get_ticker(
    symbol="BTCUSDT",
    product_type="USDT-FUTURES"
)

# Get account information
account = client.account.get_account(
    symbol="BTCUSDT",
    product_type="USDT-FUTURES",
    margin_coin="USDT"
)
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
from bitget_api.exceptions import InvalidProductTypeError, BitgetAPIError

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

Citations:
[1] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/45765156/c6616fd7-7ff6-4ed8-adec-990982d907e4/account.py
[2] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/45765156/a397637a-9470-4e70-88f9-620274df873a/position.py
[3] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/45765156/1fba71bc-7a09-4b25-82be-021a9273ec80/market.py