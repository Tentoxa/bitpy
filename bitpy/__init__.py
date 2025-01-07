"""A Python client for the Bitget API with comprehensive position management

... moduleauthor: Tentoxa
"""

__version__ = '1.0.0'

from bitpy.rest_api import BitgetAPI
from bitpy.ws_api import BitgetWebsocketAPI
from bitpy.exceptions import (
    BitgetAPIError,
    InvalidProductTypeError,
    InvalidGranularityError,
    InvalidBusinessTypeError,
    RequestError
)

__all__ = [
    'BitgetWebsocketAPI',
    'BitgetAPI',
    'BitgetAPIError',
    'InvalidProductTypeError',
    'InvalidGranularityError',
    'InvalidBusinessTypeError',
    'RequestError'
]