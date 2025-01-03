"""A Python client for the Bitget API with comprehensive position management

... moduleauthor: Tentoxa
"""

__version__ = '1.0.0'

from bitget_api.api import BitgetAPI
from bitget_api.exceptions import (
    BitgetAPIError,
    InvalidProductTypeError,
    InvalidGranularityError,
    InvalidBusinessTypeError,
    RequestError
)

__all__ = [
    'BitgetAPI',
    'BitgetAPIError',
    'InvalidProductTypeError',
    'InvalidGranularityError',
    'InvalidBusinessTypeError',
    'RequestError'
]