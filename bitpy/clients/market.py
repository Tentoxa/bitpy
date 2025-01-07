from ..models.market import *
from bitpy.exceptions import InvalidGranularityError
from typing import Optional, Union
from datetime import datetime
from .base_client import BitgetBaseClient


class BitgetMarketClient(BitgetBaseClient):
    def get_vip_fee_rate(self) -> VIPFeeRateResponse:
        response = self.request_handler.request(
            method="GET",
            endpoint="/api/v2/mix/market/vip-fee-rate",
            authenticate=False
        )

        return VIPFeeRateResponse(
            code=response["code"],
            msg=response["msg"],
            requestTime=response["requestTime"],
            data=[VIPFeeRateData(**item) for item in response["data"]]
        )

    @staticmethod
    def _validate_granularity(granularity: str) -> None:
        if type(granularity) != str:
            raise InvalidGranularityError(f"Invalid granularity. Must be a string")

        valid_types = [pt.value.lower() for pt in CandleGranularity]
        if granularity.lower() not in valid_types:
            raise InvalidGranularityError(f"Invalid granularity type. Must be one of: {', '.join(valid_types)}")

    def get_interest_rate_history(self, coin: str) -> InterestRateHistoryResponse:
        response = self.request_handler.request(
            method="GET",
            endpoint="/api/v2/mix/market/union-interest-rate-history",
            params={"coin": coin},
            authenticate=False
        )

        return InterestRateHistoryResponse(**response)

    def get_exchange_rate(self) -> ExchangeRateResponse:
        response = self.request_handler.request(
            method="GET",
            endpoint="/api/v2/mix/market/exchange-rate",
            authenticate=False
        )

        return ExchangeRateResponse(**response)

    def get_discount_rate(self) -> DiscountRateResponse:
        response = self.request_handler.request(
            method="GET",
            endpoint="/api/v2/mix/market/discount-rate",
            authenticate=False
        )
        return DiscountRateResponse(**response)

    def get_merge_depth(self, symbol: str, product_type: str, precision: str = None,
                        limit: str = None) -> MarketDepthResponse:
        self._validate_product_type(product_type)
        params = self._build_params(
            symbol=self._clean_symbol(symbol),
            productType=product_type,
            precision=precision,
            limit=limit
        )

        response = self.request_handler.request(
            method="GET",
            endpoint="/api/v2/mix/market/merge-depth",
            params=params,
            authenticate=False
        )
        return MarketDepthResponse(**response)

    def get_ticker(self, symbol: str, product_type: str) -> TickerResponse:
        self._validate_product_type(product_type)
        params = self._build_params(
            symbol=self._clean_symbol(symbol),
            productType=product_type
        )
        response = self.request_handler.request(
            method="GET",
            endpoint="/api/v2/mix/market/ticker",
            params=params,
            authenticate=False
        )
        return TickerResponse(**response)

    def get_all_tickers(self, product_type: str) -> TickerResponse:
        self._validate_product_type(product_type)
        params = self._build_params(productType=product_type)
        response = self.request_handler.request(
            method="GET",
            endpoint="/api/v2/mix/market/tickers",
            params=params,
            authenticate=False
        )
        return TickerResponse(**response)

    def get_recent_transactions(self, symbol: str, product_type: str,
                                limit: str = None) -> RecentTransactionsResponse:
        self._validate_product_type(product_type)
        params = self._build_params(
            symbol=self._clean_symbol(symbol),
            productType=product_type,
            limit=limit
        )

        response = self.request_handler.request(
            method="GET",
            endpoint="/api/v2/mix/market/fills",
            params=params,
            authenticate=False
        )
        return RecentTransactionsResponse(**response)

    def get_historical_transactions(
            self,
            symbol: str,
            product_type: str,
            limit: Optional[int] = 500,
            id_less_than: Optional[str] = None,
            start_time: Optional[Union[datetime, int]] = None,
            end_time: Optional[Union[datetime, int]] = None
    ) -> HistoricalTransactionsResponse:
        self._validate_product_type(product_type)

        start_time, end_time = self._validate_time_range(start_time, end_time)
        limit = min(limit or 500, 1000)

        params = self._build_params(
            symbol=self._clean_symbol(symbol),
            productType=product_type,
            limit=limit,
            idLessThan=id_less_than,
            startTime=start_time,
            endTime=end_time
        )

        response = self.request_handler.request(
            method="GET",
            endpoint="/api/v2/mix/market/fills-history",
            params=params,
            authenticate=False
        )
        return HistoricalTransactionsResponse(**response)

    def get_candlestick(self, symbol: str, product_type: str, granularity: str,
                        start_time: Optional[Union[datetime, int]] = None,
                        end_time: Optional[Union[datetime, int]] = None,
                        k_line_type: str = None, limit: Optional[int] = 100) -> CandlestickResponse:
        self._validate_product_type(product_type)
        self._validate_granularity(granularity)

        start_time, end_time = self._validate_time_range(start_time, end_time)
        limit = min(limit or 100, 1000)

        params = self._build_params(
            symbol=self._clean_symbol(symbol),
            productType=product_type,
            granularity=granularity,
            startTime=start_time,
            endTime=end_time,
            kLineType=k_line_type,
            limit=limit
        )

        response = self.request_handler.request(
            method="GET",
            endpoint="/api/v2/mix/market/candles",
            params=params,
            authenticate=False
        )
        return CandlestickResponse(**response)

    def get_history_candlestick(self, symbol: str, product_type: str, granularity: str,
                                start_time: Optional[Union[datetime, int]] = None,
                                end_time: Optional[Union[datetime, int]] = None,
                                limit: Optional[int] = 100) -> CandlestickResponse:
        self._validate_product_type(product_type)
        self._validate_granularity(granularity)
        start_time, end_time = self._validate_time_range(start_time, end_time)
        limit = min(limit or 100, 200)

        params = self._build_params(
            symbol=self._clean_symbol(symbol),
            productType=product_type,
            granularity=granularity,
            startTime=start_time,
            endTime=end_time,
            limit=limit
        )
        response = self.request_handler.request(
            method="GET",
            endpoint="/api/v2/mix/market/history-candles",
            params=params,
            authenticate=False
        )
        return CandlestickResponse(**response)

    def get_history_index_candlestick(self, symbol: str, product_type: str, granularity: str,
                                      start_time: Optional[Union[datetime, int]] = None,
                                      end_time: Optional[Union[datetime, int]] = None,
                                      limit: Optional[int] = 100) -> CandlestickResponse:
        self._validate_product_type(product_type)
        self._validate_granularity(granularity)
        start_time, end_time = self._validate_time_range(start_time, end_time)
        limit = min(limit or 100, 200)

        params = self._build_params(
            symbol=self._clean_symbol(symbol),
            productType=product_type,
            granularity=granularity,
            startTime=start_time,
            endTime=end_time,
            limit=limit
        )
        response = self.request_handler.request(
            method="GET",
            endpoint="/api/v2/mix/market/history-index-candles",
            params=params,
            authenticate=False
        )
        return CandlestickResponse(**response)

    def get_history_mark_candlestick(self, symbol: str, product_type: str, granularity: str,
                                     start_time: Optional[Union[datetime, int]] = None,
                                     end_time: Optional[Union[datetime, int]] = None,
                                     limit: Optional[int] = 100) -> CandlestickResponse:
        self._validate_product_type(product_type)
        self._validate_granularity(granularity)
        start_time, end_time = self._validate_time_range(start_time, end_time)
        limit = min(limit or 100, 200)

        params = self._build_params(
            symbol=self._clean_symbol(symbol),
            productType=product_type,
            granularity=granularity,
            startTime=start_time,
            endTime=end_time,
            limit=limit
        )
        response = self.request_handler.request(
            method="GET",
            endpoint="/api/v2/mix/market/history-mark-candles",
            params=params,
            authenticate=False
        )
        return CandlestickResponse(**response)

    def get_open_interest(self, symbol: str, product_type: str) -> OpenInterestResponse:
        self._validate_product_type(product_type)
        params = self._build_params(
            symbol=self._clean_symbol(symbol),
            productType=product_type
        )
        response = self.request_handler.request(
            method="GET",
            endpoint="/api/v2/mix/market/open-interest",
            params=params,
            authenticate=False
        )
        return OpenInterestResponse(**response)

    def get_funding_time(self, symbol: str, product_type: str) -> FundingTimeResponse:
        self._validate_product_type(product_type)
        params = self._build_params(
            symbol=self._clean_symbol(symbol),
            productType=product_type
        )
        response = self.request_handler.request(
            method="GET",
            endpoint="/api/v2/mix/market/funding-time",
            params=params,
            authenticate=False
        )
        return FundingTimeResponse(**response)

    def get_symbol_price(self, symbol: str, product_type: str) -> SymbolPriceResponse:
        self._validate_product_type(product_type)
        params = self._build_params(
            symbol=self._clean_symbol(symbol),
            productType=product_type
        )
        response = self.request_handler.request(
            method="GET",
            endpoint="/api/v2/mix/market/symbol-price",
            params=params,
            authenticate=False
        )
        return SymbolPriceResponse(**response)

    def get_historical_funding_rates(self, symbol: str, product_type: str,
                                     page_size: str = None, page_no: str = None) -> HistoricalFundingRateResponse:
        self._validate_product_type(product_type)
        if page_size:
            page_size = min(int(page_size), 100)
        params = self._build_params(
            symbol=self._clean_symbol(symbol),
            productType=product_type,
            pageSize=page_size,
            pageNo=page_no
        )
        response = self.request_handler.request(
            method="GET",
            endpoint="/api/v2/mix/market/history-fund-rate",
            params=params,
            authenticate=False
        )
        return HistoricalFundingRateResponse(**response)

    def get_current_funding_rate(self, symbol: str, product_type: str) -> CurrentFundingRateResponse:
        self._validate_product_type(product_type)
        params = self._build_params(
            symbol=self._clean_symbol(symbol),
            productType=product_type
        )
        response = self.request_handler.request(
            method="GET",
            endpoint="/api/v2/mix/market/current-fund-rate",
            params=params,
            authenticate=False
        )
        return CurrentFundingRateResponse(**response)

    def get_contract_config(self, symbol: str = None, product_type: str = None) -> ContractConfigResponse:
        self._validate_product_type(product_type)
        params = self._build_params(
            symbol=self._clean_symbol(symbol) if symbol else None,
            productType=product_type
        )
        response = self.request_handler.request(
            method="GET",
            endpoint="/api/v2/mix/market/contracts",
            params=params,
            authenticate=False
        )
        return ContractConfigResponse(**response)
