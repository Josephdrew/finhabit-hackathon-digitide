from pydantic import BaseModel, Field
from datetime import datetime

class BudgetChoiceCreate(BaseModel):
    user_id: int
    needs_percentage: float = Field(..., ge=0, le=100)
    wants_percentage: float = Field(..., ge=0, le=100)
    savings_percentage: float = Field(..., ge=0, le=100)

class BudgetChoiceResponse(BaseModel):
    id: int
    user_id: int
    needs_percentage: float
    wants_percentage: float
    savings_percentage: float
    created_at: datetime

    class Config:
        orm_mode = True
