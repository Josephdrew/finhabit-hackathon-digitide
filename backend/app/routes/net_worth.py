from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.net_worth import NetWorthResponse
from app.crud.net_worth import get_latest_snapshot_for_user
from scripts.store_networth_snapshot import store_networth_data

router = APIRouter()

@router.get("/home/{user_id}", response_model=NetWorthResponse)
async def fetch_net_worth(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await get_latest_snapshot_for_user(db, user_id)
    if not result:
        raise HTTPException(status_code=404, detail="No net worth snapshot found.")
    return result


@router.post("/networth/init")
async def load_networth_data(db: AsyncSession = Depends(get_db)):
    result = await store_networth_data(db=db, user_id=1)
    return result
