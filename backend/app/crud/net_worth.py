from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.snapshot import NetWorthSnapshot
from app.models.net_asset import NetWorthAsset  # Import if needed for attribute references
from app.schemas.net_worth import NetWorthResponse, AssetValueSchema

async def get_latest_snapshot_for_user(db: AsyncSession, user_id: int) -> NetWorthResponse | None:
    result = await db.execute(
        select(NetWorthSnapshot)
        .options(
            selectinload(NetWorthSnapshot.assets)
                .selectinload(NetWorthAsset.asset_type),   
            selectinload(NetWorthSnapshot.assets)
                .selectinload(NetWorthAsset.currency),
            selectinload(NetWorthSnapshot.currency),
        )
        .where(NetWorthSnapshot.user_id == user_id)
        .order_by(NetWorthSnapshot.snapshot_date.desc())
        .limit(1)
    )
    snapshot = result.scalar_one_or_none()

    if not snapshot:
        return None

    asset_values = [
        AssetValueSchema(
            asset_type=asset.asset_type.label,
            value=asset.value,
            currency_code=asset.currency.code,
        )
        for asset in snapshot.assets
    ]

    return NetWorthResponse(
        net_worth=snapshot.total_value,
        currency_code=snapshot.currency.code,
        asset_values=asset_values
    )
