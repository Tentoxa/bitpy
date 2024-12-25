from dataclasses import dataclass, fields
from typing import List
from enum import Enum


class ProductType(Enum):
    USDT_FUTURES = 'USDT-FUTURES'
    COIN_FUTURES = 'COIN-FUTURES'
    USDC_FUTURES = 'USDC-FUTURES'
    SUSDT_FUTURES = 'SUSDT-FUTURES'
    SCOIN_FUTURES = 'SCOIN-FUTURES'
    SUSDC_FUTURES = 'SUSDC-FUTURES'


@dataclass
class PositionData:
    marginCoin: str
    symbol: str
    holdSide: str
    openDelegateSize: str
    marginSize: str
    available: str
    locked: str
    total: str
    leverage: str
    achievedProfits: str
    openPriceAvg: str
    marginMode: str
    posMode: str
    unrealizedPL: str
    liquidationPrice: str
    keepMarginRate: str
    markPrice: str
    breakEvenPrice: str
    totalFee: str
    deductedFee: str
    marginRatio: str
    assetMode: str
    autoMargin: str
    grant: str
    takeProfit: str
    stopLoss: str
    takeProfitId: str
    stopLossId: str
    cTime: str
    uTime: str

    def __init__(self, **kwargs):
        names = set([f.name for f in fields(self)])
        for k, v in kwargs.items():
            if k in names:
                # Convert None to empty string to match API behavior
                setattr(self, k, v if v is not None else '')


@dataclass
class HistoricalPositionData:
    positionId: str
    marginCoin: str
    symbol: str
    holdSide: str
    openAvgPrice: str
    closeAvgPrice: str
    marginMode: str
    openTotalPos: str
    closeTotalPos: str
    pnl: str
    netProfit: str
    totalFunding: str
    openFee: str
    closeFee: str
    cTime: str
    uTime: str

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v if v is not None else '')


@dataclass
class PositionTierData:
    symbol: str
    level: str
    startUnit: str
    endUnit: str
    leverage: str
    keepMarginRate: str

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v if v is not None else '')


@dataclass
class PositionTierResponse:
    code: str
    msg: str
    requestTime: int
    data: List[PositionTierData]


@dataclass
class HistoricalPositionsResponse:
    code: str
    msg: str
    requestTime: int
    data: List[HistoricalPositionData]


@dataclass
class AllPositionsResponse:
    code: str
    msg: str
    requestTime: int
    data: List[PositionData]


@dataclass
class SinglePositionResponse:
    code: str
    msg: str
    requestTime: int
    data: List[PositionData]
