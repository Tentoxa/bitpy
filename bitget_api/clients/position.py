from .base_client import BitgetBaseClient
from ..models.position import *
from datetime import datetime
from typing import Optional, Union


class BitgetPositionClient(BitgetBaseClient):
    def get_all_positions(self, product_type: str, margin_coin: Optional[str] = None) -> AllPositionsResponse:
        self._validate_product_type(product_type)
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
        self._validate_product_type(product_type)
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
        self._validate_product_type(product_type)

        start_time, end_time = self._validate_time_range(start_time, end_time)
        limit = min(limit or 20, 100)

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
        self._validate_product_type(product_type)
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
