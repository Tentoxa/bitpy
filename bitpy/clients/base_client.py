from ..utils.request_handler import RequestHandler
from ..models.base import ProductType
from bitpy.exceptions import InvalidProductTypeError
from datetime import datetime, timedelta
from typing import Optional, Union


class BitgetBaseClient:
    MAX_TIME_RANGE_DAYS = 90

    def __init__(self, request_handler: RequestHandler, debug: bool = False):
        self.request_handler = request_handler
        self.debug = debug

    @staticmethod
    def _build_params(**kwargs) -> dict:
        return {k: str(v) for k, v in kwargs.items() if v is not None}

    @staticmethod
    def _clean_symbol(symbol: str) -> str:
        cleaned = ''.join(c for c in symbol.lower().strip() if c.isalnum())
        return f"{cleaned[:-4]}usdt" if "usdt" in cleaned else cleaned

    @staticmethod
    def _validate_product_type(product_type: str) -> None:
        if type(product_type) != str:
            raise InvalidProductTypeError(f"Invalid Product Type. Must be a string")

        valid_types = [pt.value for pt in ProductType]
        if product_type not in valid_types:
            raise InvalidProductTypeError(f"Invalid product type. Must be one of: {', '.join(valid_types)}")

    def _validate_time_range(self, start_time: Optional[Union[datetime, int]],
                             end_time: Optional[Union[datetime, int]]) -> tuple:
        if not (start_time and end_time):
            return start_time, end_time

        if isinstance(end_time, datetime) and isinstance(start_time, datetime):
            time_diff = end_time - start_time
            if time_diff.days > self.MAX_TIME_RANGE_DAYS:
                start_time = end_time - timedelta(days=self.MAX_TIME_RANGE_DAYS)

        return (
            int(start_time.timestamp() * 1000) if isinstance(start_time, datetime) else start_time,
            int(end_time.timestamp() * 1000) if isinstance(end_time, datetime) else end_time
        )
