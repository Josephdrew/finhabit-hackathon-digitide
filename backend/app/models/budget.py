from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.core.database import Base

class BudgetChoice(Base):
    __tablename__ = 'budget_choice'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    needs_percentage = Column(Float, nullable=False)
    wants_percentage = Column(Float, nullable=False)
    savings_percentage = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Optional: define relationship if user model exists
    user = relationship("User", back_populates="budget_choices")
