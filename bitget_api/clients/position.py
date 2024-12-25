from ..utils.request_handler import RequestHandler
from ..models.position import (AllPositionsResponse,
                               SinglePositionResponse,
                               PositionData,
                               HistoricalPositionData,
                               HistoricalPositionsResponse,
                               PositionTierData,
                               PositionTierResponse,
                               ProductType)
from datetime import datetime, timedelta
from typing import Optional, Union
from ..exceptions import InvalidProductTypeError

class BitgetPositionClient:
    MAX_TIME_RANGE_DAYS = 90
    DEFAULT_LIMIT = 20
    MAX_LIMIT = 100

    def __init__(self, request_handler: RequestHandler, debug: bool = False):
        self.request_handler = request_handler
        self.debug = debug

    @staticmethod
    def _clean_symbol(symbol: str) -> str:
        cleaned = ''.join(c for c in symbol.lower().strip() if c.isalnum())
        return f"{cleaned[:-4]}usdt" if "usdt" in cleaned else cleaned

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

    def _validate_product_type(self, product_type: str) -> str:
        valid_types = [pt.value for pt in ProductType]
        if product_type not in valid_types:
            raise InvalidProductTypeError(f"Invalid product type. Must be one of: {', '.join(valid_types)}")
        return product_type

    def _build_params(self, **kwargs) -> dict:
        return {k: str(v) for k, v in kwargs.items() if v is not None}

    def get_all_positions(self, product_type: str, margin_coin: Optional[str] = None) -> AllPositionsResponse:
        product_type = self._validate_product_type(product_type)
        params = self._build_params(
            productType=product_type,
            marginCoin=margin_coin.upper() if margin_coin else None
        )
        response = self.request_handler.request("GET", "/api/v2/mix/position/all-position", params)
        return AllPositionsResponse(
            code=response["code"],
            msg=response["msg"],
            requestTime=response["requestTime"],
            data=[PositionData(**item) for item in response["data"]]
        )

    def get_single_position(self, symbol: str, product_type: str, margin_coin: str) -> SinglePositionResponse:
        product_type = self._validate_product_type(product_type)
        params = self._build_params(
            symbol=self._clean_symbol(symbol),
            productType=product_type,
            marginCoin=margin_coin.upper()
        )
        response = self.request_handler.request("GET", "/api/v2/mix/position/single-position", params)
        return SinglePositionResponse(
            code=response["code"],
            msg=response["msg"],
            requestTime=response["requestTime"],
            data=[PositionData(**item) for item in response["data"]]
        )

    def get_historical_position(
        self,
        product_type: str = "USDT-FUTURES",
        symbol: Optional[str] = None,
        id_less_than: Optional[str] = None,
        start_time: Optional[Union[datetime, int]] = None,
        end_time: Optional[Union[datetime, int]] = None,
        limit: Optional[int] = None
    ) -> HistoricalPositionsResponse:
        product_type = self._validate_product_type(product_type)

        start_time, end_time = self._validate_time_range(start_time, end_time)
        limit = min(limit or self.DEFAULT_LIMIT, self.MAX_LIMIT)

        params = self._build_params(
            productType=product_type,
            symbol=self._clean_symbol(symbol) if symbol else None,
            idLessThan=id_less_than,
            startTime=start_time,
            endTime=end_time,
            limit=limit
        )
        response = self.request_handler.request("GET", "/api/v2/mix/position/history-position", params)
        return HistoricalPositionsResponse(
            code=response["code"],
            msg=response["msg"],
            requestTime=response["requestTime"],
            data=[HistoricalPositionData(**item) for item in response["data"]["list"]]
        )

    def get_position_tier(self, symbol: str, product_type: str) -> PositionTierResponse:
        product_type = self._validate_product_type(product_type)
        params = self._build_params(
            symbol=self._clean_symbol(symbol),
            productType=product_type
        )
        response = self.request_handler.request("GET", "/api/v2/mix/market/query-position-lever", params)
        return PositionTierResponse(
            code=response["code"],
            msg=response["msg"],
            requestTime=response["requestTime"],
            data=[PositionTierData(**item) for item in response["data"]]
        )