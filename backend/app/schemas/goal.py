from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional

class GoalCreate(BaseModel):
    user_id: int
    title: str
    description: Optional[str]
    target_amount: float
    due_date: Optional[date]
    type: Optional[str] = None
    saved_amount: float = 0  

class GoalResponse(BaseModel):
    id: int
    user_id: int
    title: str
    type: Optional[str]
    saved_amount: float
    target_amount: float
    due_date: Optional[date]
    is_completed: bool
    created_at: datetime
    progress_percent: float

    class Config:
        orm_mode = True

class AddGoalAmount(BaseModel):
    goal_id: int
    amount: float
