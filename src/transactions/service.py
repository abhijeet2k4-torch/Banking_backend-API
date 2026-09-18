from decimal import Decimal
from uuid import UUID
from fastapi import HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, desc, or_
from src.db.models import TransactionModel as TransactionTable
from src.db.models import AccountModel as AccountTable, TransactionType

class TransactionService:
    async def get_current_user_transactions(self, user_id: UUID, session: AsyncSession):
        account = await self.get_account_by_id(user_id=user_id, session=session)
        transactions = await session.exec(select(TransactionTable).where(or_(TransactionTable.sender_account_number == account.account_number, TransactionTable.receiver_account_number == account.account_number)).order_by(desc(TransactionTable.created_at)))
        return transactions.all()

    async def get_transaction_by_id(self, transaction_id: UUID, session: AsyncSession):
        transaction = await session.exec(select(TransactionTable).where(TransactionTable.transaction_id == transaction_id))
        transaction = transaction.first()
        if not transaction:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found.")
        return transaction

    async def get_transaction_by_user_id(self, user_id: UUID, session: AsyncSession):
        account = await self.get_account_by_id(user_id=user_id, session=session)
        transactions = await session.exec(select(TransactionTable).where(or_(TransactionTable.sender_account_number == account.account_number, TransactionTable.receiver_account_number == account.account_number)).order_by(desc(TransactionTable.created_at)))
        return transactions.all()

    async def create_withdrawal(self, user_id: UUID, transaction_amount: Decimal, session: AsyncSession):
        account = await self.get_account_by_id(user_id=user_id, session=session)
        if account.balance < transaction_amount:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Insufficient balance for withdrawal.")
        if account.status != "active":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Your account is not active.")
        create_transaction = await self.create_transaction(sender_account=account, receiver_account=None, transaction_type=TransactionType.WITHDRAWAL, transaction_amount=transaction_amount, session=session)
        return create_transaction

    async def create_deposit(self, user_id: UUID, transaction_amount: Decimal, session: AsyncSession):
            account = await self.get_account_by_id(user_id=user_id, session=session)
            if account.status != "active":
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Your account is not active.")
            create_transaction = await self.create_transaction(sender_account=None, receiver_account=account, transaction_type=TransactionType.DEPOSIT, transaction_amount=transaction_amount, session=session)
            return create_transaction

    async def create_transfer(self, user_id: UUID, transaction_amount: Decimal, receiver_account_number: str, session: AsyncSession):
                sender_account = await self.get_account_by_id(user_id=user_id, session=session)
                receiver_account = await self.get_account_by_account_number(account_number=receiver_account_number, session=session)
                if sender_account.balance < transaction_amount:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Insufficient balance for transfer.")
                if sender_account.status != "active":
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Your account is not active.")
                if receiver_account.status != "active":
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Receiver account is not active.")
                create_transaction = await self.create_transaction(sender_account=sender_account, receiver_account=receiver_account, transaction_type=TransactionType.TRANSFER, transaction_amount=transaction_amount, session=session)
                return create_transaction
    
    # auxiliary functions
    async def get_account_by_id(self, user_id: UUID, session: AsyncSession):
        account = await session.exec(select(AccountTable).where(AccountTable.user_id == user_id))
        account = account.first()
        if not account:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found for the user.")
        return account

    async def get_account_by_account_number(self, account_number: str, session: AsyncSession):
        account = await session.exec(select(AccountTable).where(AccountTable.account_number == account_number))
        account = account.first()
        if not account:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found for the account number.")
        return account

    async def create_transaction(self, sender_account: AccountTable | None, receiver_account: AccountTable | None, transaction_type: TransactionType, transaction_amount: Decimal, session: AsyncSession):
        transaction = TransactionTable(
            sender_account_number=sender_account.account_number if sender_account else None,
            receiver_account_number=receiver_account.account_number if receiver_account else None,
            transaction_type=transaction_type,
            transaction_amount=transaction_amount
        )
        session.add(transaction)
        if sender_account:
            sender_account.balance -= transaction_amount
        if receiver_account:
            receiver_account.balance += transaction_amount
        await session.commit()
        await session.refresh(transaction)
        return transaction