from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from app.core.database import get_db
from app.models.notification import Notification
from app.schemas.notification import NotificationResponse

router = APIRouter()

@router.get("/notifications/{user_id}", response_model=List[NotificationResponse])
async def get_notifications(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Notification).where(Notification.user_id == user_id).order_by(Notification.created_at.desc()))
    notifications = result.scalars().all()

    if not notifications:
        raise HTTPException(status_code=404, detail="No notifications found for this user.")

    return notifications
