from pydantic import BaseModel

class AssetTypeBase(BaseModel):
    code: str
    label: str