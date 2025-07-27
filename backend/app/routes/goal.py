from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.models.goal import Goal, GoalTransaction
from app.schemas.goal import GoalCreate, GoalResponse, AddGoalAmount
from sqlalchemy.future import select
from decimal import Decimal

router = APIRouter()

@router.post("/goals", response_model=GoalResponse)
async def create_goal(goal: GoalCreate, db: AsyncSession = Depends(get_db)):
    new_goal = Goal(**goal.dict())
    db.add(new_goal)
    await db.commit()
    await db.refresh(new_goal)
    return GoalResponse(
        id=new_goal.id,
        user_id=new_goal.user_id,
        title=new_goal.title,
        description=new_goal.description,
        type=new_goal.type,
        saved_amount=float(new_goal.saved_amount),
        target_amount=float(new_goal.target_amount),
        due_date=new_goal.due_date,
        is_completed=new_goal.is_completed,
        created_at=new_goal.created_at,
        progress_percent=round((float(new_goal.saved_amount) / float(new_goal.target_amount)) * 100, 2)
        if new_goal.target_amount else 0.0
    )


@router.get("/goals", response_model=list[GoalResponse])
async def list_goals(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Goal).where(Goal.user_id == user_id))
    goals = result.scalars().all()

    return [
        GoalResponse(
            id=goal.id,
            user_id=goal.user_id,
            title=goal.title,
            description=goal.description,
            type=goal.type,
            saved_amount=float(goal.saved_amount),
            target_amount=float(goal.target_amount),
            due_date=goal.due_date,
            is_completed=goal.is_completed,
            created_at=goal.created_at,
            progress_percent=round((float(goal.saved_amount) / float(goal.target_amount)) * 100, 2)
            if goal.target_amount else 0.0
        )
        for goal in goals
    ]

@router.delete("/goals/{goal_id}")
async def delete_goal(goal_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Goal).where(Goal.id == goal_id))
    goal = result.scalar_one_or_none()
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    await db.delete(goal)
    await db.commit()
    return {"detail": "Goal deleted successfully"}

@router.get("/goals/stats/{user_id}")
async def goal_stats(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Goal).where(Goal.user_id == user_id))
    goals = result.scalars().all()

    total_goals = len(goals)
    completed = sum(1 for g in goals if g.is_completed)
    progress = [
        {
            "goal_id": g.id,
            "title": g.title,
            "progress_percent": float(g.saved_amount / g.target_amount) * 100 if g.target_amount else 0
        }
        for g in goals
    ]
    return {
        "total_goals": total_goals,
        "completed_goals": completed,
        "progress": progress
    }


