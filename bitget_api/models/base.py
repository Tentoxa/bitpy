from dataclasses import dataclass
from enum import Enum


class ProductType(Enum):
    USDT_FUTURES = 'USDT-FUTURES'
    COIN_FUTURES = 'COIN-FUTURES'
    USDC_FUTURES = 'USDC-FUTURES'
    SUSDT_FUTURES = 'SUSDT-FUTURES'
    SCOIN_FUTURES = 'SCOIN-FUTURES'
    SUSDC_FUTURES = 'SUSDC-FUTURES'


@dataclass
class BaseResponse:
    code: str
    msg: str
    requestTime: int


@dataclass
class BaseData:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v if v is not None else '')
