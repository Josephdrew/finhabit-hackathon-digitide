from pydantic import BaseModel
from typing import Optional

class CurrencyBase(BaseModel):
    code: str
    name: str
    symbol: Optional[str] = None
