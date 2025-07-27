from sqlalchemy import select
from datetime import datetime, date
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import BankTransaction
from static_data.bank_transaction_response import api_response
from datetime import date
from decimal import Decimal
import traceback

async def insert_transactions(db: AsyncSession, user_id: int = 1):
    try:
        # 1. Get or Create Currency
        txns = api_response['bankTransactions'][0]['txns']
        bank = api_response["bankTransactions"][0]["bank"]

        async with AsyncSessionLocal() as session:
        for txn in txns:
            transaction = BankTransaction(
                bank_name=bank,
                transaction_amount=float(txn[0]),
                transaction_narration=txn[1],
                transaction_date=datetime.datetime.strptime(txn[2], "%Y-%m-%d").date(),
                transaction_type=int(txn[3]),
                transaction_mode=txn[4],
                current_balance=float(txn[5])
            )
            session.add(transaction)
        try:
            await session.commit()
            print("✅ Transactions inserted successfully")
        except IntegrityError as e:
            print("❌ Insert failed:", e)

        return {"status": "success", "message": "Net worth data stored successfully."}

    except Exception as e:
        await db.rollback()
        print(f"[DB Error] {str(e)}")
        return {"status": "error", "message": str(e)}
    
