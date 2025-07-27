from sqlalchemy import select
from datetime import datetime, date
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import AssetType, Currency, NetWorthAsset, NetWorthSnapshot
from static_data.networth_api_response import api_response
from datetime import date
from decimal import Decimal
import traceback

async def store_networth_data(db: AsyncSession, user_id: int = 1):
    try:
        # 1. Get or Create Currency
        currency_code = api_response['netWorthResponse']['totalNetWorthValue']['currencyCode']
        result = await db.execute(select(Currency).filter_by(code=currency_code))
        currency = result.scalar_one_or_none()

        if not currency:
            currency = Currency(code=currency_code)
            db.add(currency)
            await db.flush()  # To get currency.id

        currency_id = currency.id

        # 2. Prepare AssetType records
        asset_type_ids = {}
        for asset in api_response['netWorthResponse']['assetValues']:
            code = asset['netWorthAttribute']
            if code not in asset_type_ids:
                result = await db.execute(select(AssetType).filter_by(code=code))
                asset_type = result.scalar_one_or_none()

                if not asset_type:
                    label = code.replace("ASSET_TYPE_", "").replace("_", " ").title()
                    asset_type = AssetType(code=code, label=label)
                    db.add(asset_type)
                    await db.flush()  # To get asset_type.id

                asset_type_ids[code] = asset_type.id

        # 3. Create NetWorthSnapshot
        total_value = Decimal(api_response['netWorthResponse']['totalNetWorthValue']['units'])
        snapshot = NetWorthSnapshot(
            user_id=user_id,
            currency_id=currency_id,
            total_value=total_value,
            snapshot_date=date.today()
        )
        db.add(snapshot)
        await db.flush()  # To get snapshot.id

        # 4. Create NetWorthAsset entries
        for asset in api_response['netWorthResponse']['assetValues']:
            try:
                value = Decimal(asset['value']['units'])
                asset_type_id = asset_type_ids[asset['netWorthAttribute']]
                net_asset = NetWorthAsset(
                    snapshot_id=snapshot.id,
                    asset_type_id=asset_type_id,
                    currency_id=currency_id,
                    value=value
                )
                db.add(net_asset)
            except Exception as asset_err:
                print(f"[Asset Error] Skipping asset: {asset} — Error: {asset_err}")

        # 5. Final Commit
        await db.commit()

        return {"status": "success", "message": "Net worth data stored successfully."}

    except Exception as e:
        await db.rollback()
        print(f"[DB Error] {str(e)}")
        return {"status": "error", "message": str(e)}
    
