
from .models import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

async def create_user(db: AsyncSession, user_in):
    user = User(**user_in.model_dump())
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

async def get_user_by_phone(db: AsyncSession, phone: str):
    result = await db.execute(select(User).where(User.phone == phone))
    return result.scalar_one_or_none()

