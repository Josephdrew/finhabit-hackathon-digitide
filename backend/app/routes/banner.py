from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from sqlalchemy.future import select
from app.models.banner import Banner
from datetime import date

router = APIRouter()

@router.get("/banners")
async def get_active_banners(db: AsyncSession = Depends(get_db)):
    today = date.today()
    query = select(Banner).where(
        Banner.is_active == True,
        Banner.start_date <= today,
        Banner.end_date >= today
    )
    result = await db.execute(query)
    banners = result.scalars().all()
    return banners
