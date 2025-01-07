from .base_client import BitgetBaseClient
from ..exceptions import InvalidBusinessTypeError
from ..models.account import *
from datetime import datetime
from typing import Optional, Union


class BitgetAccountClient(BitgetBaseClient):
    def get_account(self, symbol: str, product_type: str, margin_coin: str) -> AccountResponse:
        self._validate_product_type(product_type)

        params = self._build_params(
            symbol=self._clean_symbol(symbol),
            productType=product_type,
            marginCoin=margin_coin
        )

        response = self.request_handler.request(
            method="GET",
            endpoint="/api/v2/mix/account/account",
            params=params,
            authenticate=True
        )

        return AccountResponse(**response)

    @staticmethod
    def _validate_businesstype(business_type: str) -> None:

        if type(business_type) != str:
            raise InvalidBusinessTypeError(f"Invalid business type. Must be a string")

        valid_types = [pt.value.lower() for pt in BusinessType]
        if business_type.lower() not in valid_types:
            raise InvalidBusinessTypeError(f"Invalid business type. Must be one of: {', '.join(valid_types)}")

    def get_accounts(self, product_type: str) -> AccountListResponse:
        self._validate_product_type(product_type)

        params = self._build_params(productType=product_type)

        response = self.request_handler.request(
            method="GET",
            endpoint="/api/v2/mix/account/accounts",
            params=params,
            authenticate=True
        )

        return AccountListResponse(**response)

    def get_sub_account_assets(self, product_type: str) -> SubAccountAssetsResponse:
        self._validate_product_type(product_type)

        params = self._build_params(productType=product_type)

        response = self.request_handler.request(
            method="GET",
            endpoint="/api/v2/mix/account/sub-account-assets",
            params=params,
            authenticate=True
        )

        return SubAccountAssetsResponse(**response)

    def get_interest_history(
            self,
            product_type: str,
            coin: Optional[str] = None,
            id_less_than: Optional[str] = None,
            start_time: Optional[Union[datetime, int]] = None,
            end_time: Optional[Union[datetime, int]] = None,
            limit: Optional[int] = None
    ) -> InterestHistoryResponse:
        self._validate_product_type(product_type)

        start_time, end_time = self._validate_time_range(start_time, end_time)
        limit = min(limit or 20, 100)

        params = self._build_params(
            productType=product_type,
            coin=coin,
            idLessThan=id_less_than,
            startTime=start_time,
            endTime=end_time,
            limit=limit
        )

        response = self.request_handler.request(
            method="GET",
            endpoint="/api/v2/mix/account/interest-history",
            params=params,
            authenticate=True
        )
        return InterestHistoryResponse(**response)

    def get_open_count(self, symbol: str, product_type: str, margin_coin: str,
                       open_price: str, open_amount: str, leverage: Optional[str] = None) -> OpenCountResponse:
        self._validate_product_type(product_type)

        params = self._build_params(
            symbol=self._clean_symbol(symbol),
            productType=product_type,
            marginCoin=margin_coin,
            openPrice=open_price,
            openAmount=open_amount,
            leverage=leverage
        )

        response = self.request_handler.request(
            method="GET",
            endpoint="/api/v2/mix/account/open-count",
            params=params,
            authenticate=True
        )

        return OpenCountResponse(**response)

    def set_auto_margin(self, symbol: str, auto_margin: str, margin_coin: str, hold_side: str) -> SetAutoMarginResponse:
        params = self._build_params(
            symbol=self._clean_symbol(symbol),
            autoMargin=auto_margin,
            marginCoin=margin_coin,
            holdSide=hold_side
        )

        response = self.request_handler.request(
            method="POST",
            endpoint="/api/v2/mix/account/set-auto-margin",
            params=params,
            authenticate=True
        )

        return SetAutoMarginResponse(**response)

    def set_leverage(self, symbol: str, product_type: str, margin_coin: str,
                     leverage: str, hold_side: Optional[str] = None) -> SetLeverageResponse:
        self._validate_product_type(product_type)

        params = self._build_params(
            symbol=self._clean_symbol(symbol),
            productType=product_type,
            marginCoin=margin_coin,
            leverage=leverage,
            holdSide=hold_side
        )

        response = self.request_handler.request(
            method="POST",
            endpoint="/api/v2/mix/account/set-leverage",
            params=params,
            authenticate=True
        )

        return SetLeverageResponse(**response)


    def set_margin(self, symbol: str, product_type: str, margin_coin: str, amount: str, hold_side: str) -> BaseResponse:
        self._validate_product_type(product_type)

        params = self._build_params(
            symbol=self._clean_symbol(symbol),
            productType=product_type,
            marginCoin=margin_coin,
            amount=amount,
            holdSide=hold_side
        )

        response = self.request_handler.request(
            method="POST",
            endpoint="/api/v2/mix/account/set-margin",
            params=params,
            authenticate=True
        )

        return BaseResponse(**response)


    def set_asset_mode(self, product_type: str, asset_mode: str) -> BaseResponse:
        self._validate_product_type(product_type)

        params = self._build_params(
            productType=product_type,
            assetMode=asset_mode
        )

        response = self.request_handler.request(
            method="POST",
            endpoint="/api/v2/mix/account/set-asset-mode",
            params=params,
            authenticate=True
        )

        return BaseResponse(**response)


    def set_position_mode(self, product_type: str, pos_mode: str) -> PositionModeResponse:
        self._validate_product_type(product_type)

        params = self._build_params(
            productType=product_type,
            posMode=pos_mode
        )

        response = self.request_handler.request(
            method="POST",
            endpoint="/api/v2/mix/account/set-position-mode",
            params=params,
            authenticate=True
        )

        return PositionModeResponse(**response)

    def get_bills(
            self,
            product_type: str,
            coin: Optional[str] = None,
            business_type: Optional[str] = None,
            id_less_than: Optional[str] = None,
            start_time: Optional[Union[datetime, int]] = None,
            end_time: Optional[Union[datetime, int]] = None,
            limit: Optional[int] = None
    ) -> BillsResponse:
        self._validate_product_type(product_type)
        if business_type:
            self._validate_businesstype(business_type)

        # Validate coin parameter
        if coin and business_type not in ('trans_from_exchange', 'trans_to_exchange'):
            raise ValueError(
                "coin parameter is only valid when businessType is 'trans_from_exchange' or 'trans_to_exchange'")

        start_time, end_time = self._validate_time_range(start_time, end_time)
        limit = min(limit or 20, 100)

        params = self._build_params(
            productType=product_type,
            coin=coin,
            businessType=business_type,
            idLessThan=id_less_than,
            startTime=start_time,
            endTime=end_time,
            limit=limit
        )

        response = self.request_handler.request(
            method="GET",
            endpoint="/api/v2/mix/account/bill",
            params=params,
            authenticate=True
        )

        return BillsResponse(**response)

    def set_margin_mode(self, symbol: str, product_type: str, margin_coin: str, margin_mode: str) -> MarginModeResponse:
        self._validate_product_type(product_type)

        params = self._build_params(
            symbol=self._clean_symbol(symbol),
            productType=product_type,
            marginCoin=margin_coin,
            marginMode=margin_mode
        )

        response = self.request_handler.request(
            method="POST",
            endpoint="/api/v2/mix/account/set-margin-mode",
            params=params,
            authenticate=True
        )

        return MarginModeResponse(**response)
