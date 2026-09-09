from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, desc
from fastapi import HTTPException
from src.db.models import AccountModel as AccountTable, StatusType
from .schemas import AccountModel

class AccountService:
    async def get_all_accounts(self, session: AsyncSession) -> list[AccountModel]:
        statement = select(AccountTable).order_by(desc(AccountTable.created_at))
        result = await session.exec(statement)
        return result.all()

    async def get_account(self,account_number: str, session: AsyncSession) -> AccountModel:
        statement = select(AccountTable).where(AccountTable.account_number == account_number)
        result = await session.exec(statement)
        account = result.first()
        if not account:
            raise HTTPException(status_code=404, detail="Account not found")
        return account

    async def set_status(self, account_number: str, status: StatusType, session: AsyncSession) -> AccountModel | None:
        account_to_update = await self.get_account(account_number,session)
        account_to_update.status = status
        await session.commit()
        await session.refresh(account_to_update)
        return account_to_update
