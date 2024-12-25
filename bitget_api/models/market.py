from .base import BaseResponse, BaseData
from enum import Enum
from dataclasses import dataclass
from typing import List, Optional


class CandleGranularity(Enum):
    MINUTE_1 = '1m'
    MINUTE_3 = '3m'
    MINUTE_5 = '5m'
    MINUTE_15 = '15m'
    MINUTE_30 = '30m'
    HOUR_1 = '1H'
    HOUR_4 = '4H'
    HOUR_6 = '6H'
    HOUR_12 = '12H'
    DAY_1 = '1D'
    WEEK_1 = '1W'
    MONTH_1 = '1M'
    HOUR_6_UTC = '6Hutc'
    HOUR_12_UTC = '12Hutc'
    DAY_1_UTC = '1Dutc'
    DAY_3_UTC = '3Dutc'
    WEEK_1_UTC = '1Wutc'
    MONTH_1_UTC = '1Mutc'


@dataclass
class VIPFeeRateData(BaseData):
    level: str
    dealAmount: str
    assetAmount: str
    takerFeeRate: str
    makerFeeRate: str
    btcWithdrawAmount: str
    usdtWithdrawAmount: str


@dataclass
class VIPFeeRateResponse(BaseResponse):
    data: List[VIPFeeRateData]


@dataclass
class InterestRateHistory(BaseData):
    ts: str
    annualInterestRate: str
    dailyInterestRate: str


@dataclass
class InterestRateHistoryData(BaseData):
    coin: str
    historyInterestRateList: List[InterestRateHistory]


@dataclass
class InterestRateHistoryResponse(BaseResponse):
    data: InterestRateHistoryData


@dataclass
class ExchangeRateTier(BaseData):
    tier: str
    minAmount: str
    maxAmount: str
    exchangeRate: str


@dataclass
class ExchangeRateData(BaseData):
    coin: str
    exchangeRateList: List[ExchangeRateTier]


@dataclass
class ExchangeRateResponse(BaseResponse):
    data: List[ExchangeRateData]


@dataclass
class DiscountRateTier(BaseData):
    tier: str
    minAmount: str
    maxAmount: str
    discountRate: str


@dataclass
class DiscountRateData(BaseData):
    coin: str
    userLimit: str
    totalLimit: str
    discountRateList: List[DiscountRateTier]


@dataclass
class DiscountRateResponse(BaseResponse):
    data: List[DiscountRateData]


@dataclass
class MarketDepthData(BaseData):
    asks: List[List[float]]
    bids: List[List[float]]
    ts: str
    scale: str
    precision: str
    isMaxPrecision: str


@dataclass
class MarketDepthResponse(BaseResponse):
    data: MarketDepthData


@dataclass
class TickerData(BaseData):
    symbol: str
    lastPr: str
    askPr: str
    bidPr: str
    bidSz: str
    askSz: str
    high24h: str
    low24h: str
    ts: str
    change24h: str
    baseVolume: str
    quoteVolume: str
    usdtVolume: str
    openUtc: str
    changeUtc24h: str
    indexPrice: str
    fundingRate: str
    holdingAmount: str
    deliveryStartTime: Optional[str]
    deliveryTime: Optional[str]
    deliveryStatus: str
    open24h: str
    markPrice: str


@dataclass
class TickerResponse(BaseResponse):
    data: List[TickerData]


@dataclass
class RecentTransaction(BaseData):
    tradeId: str
    price: str
    size: str
    side: str
    ts: str
    symbol: str


@dataclass
class RecentTransactionsResponse(BaseResponse):
    data: List[RecentTransaction]


@dataclass
class HistoricalTransaction(BaseData):
    tradeId: str
    price: str
    size: str
    side: str
    ts: str
    symbol: str


@dataclass
class HistoricalTransactionsResponse(BaseResponse):
    data: List[HistoricalTransaction]


@dataclass
class CandlestickData(BaseData):
    timestamp: str
    openPrice: str
    highPrice: str
    lowPrice: str
    closePrice: str
    baseVolume: str
    quoteVolume: str


@dataclass
class CandlestickResponse(BaseResponse):
    data: List[CandlestickData]


@dataclass
class OpenInterestItem(BaseData):
    symbol: str
    size: str


@dataclass
class OpenInterestData(BaseData):
    openInterestList: List[OpenInterestItem]
    ts: str


@dataclass
class OpenInterestResponse(BaseResponse):
    data: OpenInterestData


@dataclass
class FundingTimeItem(BaseData):
    symbol: str
    nextFundingTime: str
    ratePeriod: str


@dataclass
class FundingTimeResponse(BaseResponse):
    data: List[FundingTimeItem]


@dataclass
class SymbolPrice(BaseData):
    symbol: str
    price: str
    indexPrice: str
    markPrice: str
    ts: str


@dataclass
class SymbolPriceResponse(BaseResponse):
    data: List[SymbolPrice]


@dataclass
class HistoricalFundingRate(BaseData):
    symbol: str
    fundingRate: str
    fundingTime: str


@dataclass
class HistoricalFundingRateResponse(BaseResponse):
    data: List[HistoricalFundingRate]


@dataclass
class CurrentFundingRate(BaseData):
    symbol: str
    fundingRate: str


@dataclass
class CurrentFundingRateResponse(BaseResponse):
    data: List[CurrentFundingRate]


@dataclass
class ContractConfig(BaseData):
    symbol: str
    baseCoin: str
    quoteCoin: str
    buyLimitPriceRatio: str
    sellLimitPriceRatio: str
    feeRateUpRatio: str
    makerFeeRate: str
    takerFeeRate: str
    openCostUpRatio: str
    supportMarginCoins: List[str]
    minTradeNum: str
    priceEndStep: str
    volumePlace: str
    pricePlace: str
    sizeMultiplier: str
    symbolType: str
    minTradeUSDT: str
    maxSymbolOrderNum: str
    maxProductOrderNum: str
    maxPositionNum: str
    symbolStatus: str
    offTime: str
    limitOpenTime: str
    deliveryTime: str
    deliveryStartTime: str
    launchTime: str
    fundInterval: str
    minLever: str
    maxLever: str
    posLimit: str
    maintainTime: str


@dataclass
class ContractConfigResponse(BaseResponse):
    data: List[ContractConfig]
