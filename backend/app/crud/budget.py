from sqlalchemy.ext.asyncio import AsyncSession
from app.models.budget import BudgetChoice
from app.schemas.budget import BudgetChoiceCreate
from sqlalchemy.future import select
from typing import List, Optional
from sqlalchemy import update
from sqlalchemy.exc import SQLAlchemyError


async def create_budget_choice(db: AsyncSession, data: BudgetChoiceCreate):
    try:
        # Check if a budget choice already exists for the user
        existing_result = await db.execute(
            select(BudgetChoice).where(BudgetChoice.user_id == data.user_id)
        )
        existing_choice = existing_result.scalar_one_or_none()

        if existing_choice:
            # Update existing record
            await db.execute(
                update(BudgetChoice)
                .where(BudgetChoice.user_id == data.user_id)
                .values(
                    needs_percentage=data.needs_percentage,
                    wants_percentage=data.wants_percentage,
                    savings_percentage=data.savings_percentage,
                )
            )
            await db.commit()
            return {"status": "updated", "message": "Budget choice updated"}
        else:
            # Insert new record
            new_choice = BudgetChoice(**data.dict())
            db.add(new_choice)
            await db.commit()
            await db.refresh(new_choice)
            return {"status": "created", "message": "Budget choice created"}

    except SQLAlchemyError as e:
        await db.rollback()
        return {"status": "error", "message": str(e)}



async def get_budget_choices_by_user(user_id: int, db: AsyncSession) -> List[BudgetChoice]:
    result = await db.execute(
        select(BudgetChoice).where(BudgetChoice.user_id == user_id)
    )
    return result.scalars().all()