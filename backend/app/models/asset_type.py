from sqlalchemy import Column, Integer, String, DateTime, func
from app.core.database import Base

class AssetType(Base):
    __tablename__ = "asset_types"

    id         = Column(Integer, primary_key=True, index=True)
    code       = Column(String, unique=True, nullable=False)
    label      = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())