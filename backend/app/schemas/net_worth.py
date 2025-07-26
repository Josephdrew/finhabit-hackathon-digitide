from pydantic import BaseModel
from typing import List
from decimal import Decimal

class AssetValueSchema(BaseModel):
    asset_type: str
    value: Decimal
    currency_code: str

class NetWorthResponse(BaseModel):
    net_worth: Decimal
    currency_code: str
    asset_values: List[AssetValueSchema]
