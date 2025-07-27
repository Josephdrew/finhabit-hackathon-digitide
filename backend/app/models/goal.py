# models/goal.py

from sqlalchemy import Column, Integer, String, Text, Numeric, Date, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class Goal(Base):
    __tablename__ = "goals"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text)
    type = Column(String, nullable=True)  # needs/wants/savings
    target_amount = Column(Numeric, nullable=False)
    saved_amount = Column(Numeric, default=0)
    due_date = Column(Date, nullable=True)
    is_completed = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    transactions = relationship("GoalTransaction", back_populates="goal")


class GoalTransaction(Base):
    __tablename__ = "goal_transactions"

    id = Column(Integer, primary_key=True)
    goal_id = Column(Integer, ForeignKey("goals.id"), nullable=False)
    amount = Column(Numeric, nullable=False)
    added_at = Column(DateTime(timezone=True), server_default=func.now())

    goal = relationship("Goal", back_populates="transactions")
