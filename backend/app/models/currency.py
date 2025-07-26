from sqlalchemy import Column, Integer, String, DateTime, func
from app.core.database import Base

class Currency(Base):
    __tablename__ = "currencies"

    id         = Column(Integer, primary_key=True, index=True)
    code       = Column(String(3), unique=True, nullable=False)
    name       = Column(String, nullable=False)
    symbol     = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())