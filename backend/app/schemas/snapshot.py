from pydantic import BaseModel
from datetime import date
from typing import Optional

class SnapshotBase(BaseModel):
    user_id: Optional[int]
    currency_id: int
    total_value: float
    snapshot_date: date