from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.crud.budget import create_budget_choice
from app.schemas.budget import BudgetChoiceCreate, BudgetChoiceResponse
from typing import List
from asyncpg.pool import Pool
from app.models.budget import BudgetChoice
from sqlalchemy import text


router = APIRouter()

@router.post("/budget-choice")
async def create_budget_choice_route(
    data: BudgetChoiceCreate,
    db: AsyncSession = Depends(get_db)
):
    return await create_budget_choice(db, data)


@router.get("/budget-choice/{user_id}", response_model=List[BudgetChoiceResponse])
async def get_budget_choices(user_id: int, db: AsyncSession = Depends(get_db)):
    query = text("""
        SELECT id, user_id, needs_percentage, wants_percentage, savings_percentage, created_at
        FROM budget_choice
        WHERE user_id = :user_id
        ORDER BY created_at DESC
    """)
    result = await db.execute(query, {"user_id": user_id})
    rows = result.fetchall()
    return [BudgetChoiceResponse(**dict(row._mapping)) for row in rows]
