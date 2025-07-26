from sqlalchemy import Column, Integer, Date, Numeric, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from app.core.database import Base

class NetWorthSnapshot(Base):
    __tablename__ = "net_worth_snapshots"

    id             = Column(Integer, primary_key=True, index=True)
    user_id        = Column(Integer, nullable=True)
    currency_id    = Column(Integer, ForeignKey("currencies.id"))
    total_value    = Column(Numeric(15, 2), nullable=False)
    snapshot_date  = Column(Date, nullable=False)
    created_at     = Column(DateTime(timezone=True), server_default=func.now())

    currency = relationship("Currency")
    assets = relationship("NetWorthAsset", back_populates="snapshot")