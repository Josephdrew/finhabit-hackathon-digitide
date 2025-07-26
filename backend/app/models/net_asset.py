from sqlalchemy import Column, Integer, Numeric, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from app.core.database import Base

class NetWorthAsset(Base):
    __tablename__ = "net_worth_assets"

    id            = Column(Integer, primary_key=True, index=True)
    snapshot_id   = Column(Integer, ForeignKey("net_worth_snapshots.id"))
    asset_type_id = Column(Integer, ForeignKey("asset_types.id"))
    currency_id   = Column(Integer, ForeignKey("currencies.id"))
    value         = Column(Numeric(15, 2), nullable=False)
    created_at    = Column(DateTime(timezone=True), server_default=func.now())

    snapshot   = relationship("NetWorthSnapshot", back_populates="assets")
    asset_type = relationship("AssetType")
    currency   = relationship("Currency")