"""A Python client for the Bitget API with comprehensive position management

... moduleauthor: Tentoxa
"""

__version__ = '1.0.0'

from bitget_api.api import BitgetAPI
from bitget_api.exceptions import (
    BitgetAPIError,
    InvalidProductTypeError,
    RequestError
)

# Optional: Export key classes/functions for easier imports
__all__ = [
    'BitgetAPI',
    'BitgetAPIError',
    'InvalidProductTypeError',
    'RequestError'
]