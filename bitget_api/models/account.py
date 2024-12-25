from dataclasses import dataclass
from enum import Enum
from .base import BaseResponse, BaseData


class BusinessType(Enum):
    UNKNOWN = 'unknown'
    TRANS_FROM_EXCHANGE = 'trans_from_exchange'
    TRANS_TO_EXCHANGE = 'trans_to_exchange'
    OPEN_LONG = 'open_long'
    OPEN_SHORT = 'open_short'
    CLOSE_LONG = 'close_long'
    CLOSE_SHORT = 'close_short'
    FORCE_CLOSE_LONG = 'force_close_long'
    FORCE_CLOSE_SHORT = 'force_close_short'
    CONTRACT_SETTLE_FEE = 'contract_settle_fee'
    APPEND_MARGIN = 'append_margin'
    ADJUST_DOWN_LEVER_APPEND_MARGIN = 'adjust_down_lever_append_margin'
    REDUCE_MARGIN = 'reduce_margin'
    AUTO_APPEND_MARGIN = 'auto_append_margin'
    CASH_GIFT_ISSUE = 'cash_gift_issue'
    CASH_GIFT_RECYCLE = 'cash_gift_recycle'
    TRACKING_FOLLOW_PAY = 'tracking_follow_pay'
    TRACKING_FOLLOW_BACK = 'tracking_follow_back'
    TRACKING_TRADER_INCOME = 'tracking_trader_income'
    BURST_LONG_LOSS_QUERY = 'burst_long_loss_query'
    BURST_SHORT_LOSS_QUERY = 'burst_short_loss_query'
    TRANS_FROM_CONTRACT = 'trans_from_contract'
    TRANS_TO_CONTRACT = 'trans_to_contract'
    TRANS_FROM_OTC = 'trans_from_otc'
    TRANS_TO_OTC = 'trans_to_otc'
    BUY = 'buy'
    SELL = 'sell'
    FORCE_BUY = 'force_buy'
    FORCE_SELL = 'force_sell'
    BURST_BUY = 'burst_buy'
    BURST_SELL = 'burst_sell'
    BONUS_ISSUE = 'bonus_issue'
    BONUS_RECYCLE = 'bonus_recycle'
    BONUS_EXPIRED = 'bonus_expired'
    DELIVERY_LONG = 'delivery_long'
    DELIVERY_SHORT = 'delivery_short'
    TRANS_FROM_CROSS = 'trans_from_cross'
    TRANS_TO_CROSS = 'trans_to_cross'
    TRANS_FROM_ISOLATED = 'trans_from_isolated'
    TRANS_TO_ISOLATED = 'trans_to_isolated'


@dataclass
class AccountData(BaseData):
    marginCoin: str
    locked: str
    available: str
    crossedMaxAvailable: str
    isolatedMaxAvailable: str
    maxTransferOut: str
    accountEquity: str
    usdtEquity: str
    btcEquity: str
    crossedRiskRate: str
    crossedMarginLeverage: str
    isolatedLongLever: str
    isolatedShortLever: str
    marginMode: str
    posMode: str
    unrealizedPL: str
    coupon: str
    crossedUnrealizedPL: str
    isolatedUnrealizedPL: str
    assetMode: str


@dataclass
class AccountResponse(BaseResponse):
    data: AccountData


@dataclass
class AccountListData(BaseData):
    marginCoin: str
    locked: str
    available: str
    crossedMaxAvailable: str
    isolatedMaxAvailable: str
    maxTransferOut: str
    accountEquity: str
    usdtEquity: str
    btcEquity: str
    crossedRiskRate: str
    unrealizedPL: str
    coupon: str
    unionTotalMagin: str
    unionAvailable: str
    unionMm: str
    assetList: list[dict]
    isolatedMargin: str
    crossedMargin: str
    crossedUnrealizedPL: str
    isolatedUnrealizedPL: str
    assetMode: str


@dataclass
class AccountListResponse(BaseResponse):
    data: list[AccountListData]


@dataclass
class SubAccountAssetData(BaseData):
    marginCoin: str
    locked: str
    available: str
    crossedMaxAvailable: str
    isolatedMaxAvailable: str
    maxTransferOut: str
    accountEquity: str
    usdtEquity: str
    btcEquity: str
    unrealizedPL: str
    coupon: str


@dataclass
class SubAccountData(BaseData):
    userId: int
    assetList: list[SubAccountAssetData]


@dataclass
class SubAccountAssetsResponse(BaseResponse):
    data: list[SubAccountData]


@dataclass
class InterestData(BaseData):
    coin: str
    liability: str
    interestFreeLimit: str
    interestLimit: str
    hourInterestRate: str
    interest: str
    cTime: str


@dataclass
class InterestHistoryData(BaseData):
    nextSettleTime: str
    borrowAmount: str
    borrowLimit: str
    interestList: list[InterestData]
    endId: str


@dataclass
class InterestHistoryResponse(BaseResponse):
    data: InterestHistoryData


@dataclass
class OpenCountData(BaseData):
    size: str


@dataclass
class OpenCountResponse(BaseResponse):
    data: OpenCountData


@dataclass
class SetAutoMarginResponse(BaseResponse):
    data: str


@dataclass
class SetLeverageData(BaseData):
    symbol: str
    marginCoin: str
    longLeverage: str
    shortLeverage: str
    crossMarginLeverage: str
    marginMode: str


@dataclass
class SetLeverageResponse(BaseResponse):
    data: SetLeverageData


@dataclass
class PositionModeData(BaseData):
    posMode: str


@dataclass
class PositionModeResponse(BaseResponse):
    data: PositionModeData


@dataclass
class BillData(BaseData):
    billId: str
    symbol: str
    amount: str
    fee: str
    feeByCoupon: str
    businessType: str
    coin: str
    balance: str
    cTime: str


@dataclass
class BillsResponseData(BaseData):
    bills: list[BillData]
    endId: str


@dataclass
class BillsResponse(BaseResponse):
    data: BillsResponseData


@dataclass
class MarginModeData(BaseData):
    symbol: str
    marginCoin: str
    longLeverage: str
    shortLeverage: str
    marginMode: str


@dataclass
class MarginModeResponse(BaseResponse):
    data: MarginModeData
