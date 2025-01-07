from dataclasses import dataclass
from typing import List
from .base import BaseResponse, BaseData


@dataclass
class PositionData(BaseData):
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
    ctime: str
    utime: str


@dataclass
class HistoricalPositionData(BaseData):
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
    ctime: str
    utime: str


@dataclass
class PositionTierData(BaseData):
    symbol: str
    level: str
    startUnit: str
    endUnit: str
    leverage: str
    keepMarginRate: str


@dataclass
class PositionTierResponse(BaseResponse):
    data: List[PositionTierData]


@dataclass
class HistoricalPositionsResponse(BaseResponse):
    data: List[HistoricalPositionData]


@dataclass
class AllPositionsResponse(BaseResponse):
    data: List[PositionData]


@dataclass
class SinglePositionResponse(BaseResponse):
    data: List[PositionData]
