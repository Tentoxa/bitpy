# 🚀 Bitget API V2 Python Client

A powerful and intuitive Python client for the Bitget API V2, focusing on position management and trading operations. More API endpoints will be added based on user demand.

## ✨ Features

- 📊 Position management for all futures markets
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

# Get all positions
positions = client.position.get_all_positions(
    product_type="USDT-FUTURES",
    margin_coin="USDT"
)

# Get single position
position = client.position.get_single_position(
    symbol="BTCUSDT",
    product_type="USDT-FUTURES",
    margin_coin="USDT"
)
```

## 💹 Supported Markets

| Market Type | Description |
|------------|-------------|
| USDT-FUTURES | USDT margined futures |
| COIN-FUTURES | Coin margined futures |
| USDC-FUTURES | USDC margined futures |
| SUSDT-FUTURES| Simulated USDT futures |
| SCOIN-FUTURES| Simulated coin futures |
| SUSDC-FUTURES| Simulated USDC futures |

## 🛠️ Core Features

**Position Management**
- 📈 Get all positions
- 🎯 Get single position details
- 📜 Query historical positions
- 🔝 Get position tier information

**Advanced Capabilities**
- ⚡ Smart rate limiting
- 🔐 Secure request signing
- ⚠️ Comprehensive error handling
- 🔍 Debug logging support

## ⚠️ Error Handling

```python
from bitget_api.exceptions import RequestError, InvalidProductTypeError, BitgetAPIError

try:
    positions = client.position.get_all_positions("INVALID-TYPE")
except InvalidProductTypeError as e:
    print(f"Invalid product type: {e}")
except BitgetAPIError as e:
    print(f"API Error {e.code}: {e.message}")
```

## 🔄 Rate Limiting

The client implements a smart token bucket algorithm for rate limiting, automatically tracking and managing request limits per endpoint to ensure optimal API usage.

## 🤝 Contributing

Contributions are welcome! Feel free to submit a Pull Request. If you need additional API endpoints implemented, please open an issue and I will prioritize adding them.

## 📄 License

This project is licensed under the MIT License.