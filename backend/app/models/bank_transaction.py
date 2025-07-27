from sqlalchemy import Column, Integer, String, Text, Date, Numeric, SmallInteger, ForeignKey
from sqlalchemy.ext.asyncio import AsyncAttrs
from app.core.database import Base

class BankTransaction(Base):
    __tablename__ = 'bank_transactions'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    bank_name = Column(String(100), nullable=False)
    transaction_amount = Column(Numeric(10, 2), nullable=False)
    transaction_narration = Column(Text, nullable=False)
    transaction_date = Column(Date, nullable=False)
    transaction_type = Column(String(100), nullable=False)
    transaction_mode = Column(String(50), nullable=False)
    category_type = Column(String(20), nullable=True)
    current_balance = Column(Numeric(10, 2), nullable=False)
