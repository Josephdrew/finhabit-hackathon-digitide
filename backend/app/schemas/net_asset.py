from pydantic import BaseModel

class AssetBase(BaseModel):
    snapshot_id: int
    asset_type_id: int
    currency_id: int
    value: float