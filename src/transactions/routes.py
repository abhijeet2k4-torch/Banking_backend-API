from uuid import UUID
from fastapi import status, APIRouter, Depends
from typing import List
from src.db.main import get_session
from .schemas import TransactionModel, WithdrawalCreate, DepositCreate, TransferCreate
from sqlalchemy.ext.asyncio import AsyncSession
from .service import TransactionService

router = APIRouter()
transaction_service = TransactionService()

@router.get("/",response_model=List[TransactionModel], responses={status.HTTP_200_OK: {"description": "Books returned"}, status.HTTP_401_UNAUTHORIZED: {"description": "Unauthorized"}, status.HTTP_403_FORBIDDEN: {"description": "Invalid or expired token"}})
async def get_current_user_transactions(user_id: UUID, session: AsyncSession = Depends(get_session)):
    return await transaction_service.get_current_user_transactions(user_id=user_id, session=session)

@router.get("/by_id/{transaction_id}",response_model=TransactionModel, responses={status.HTTP_200_OK: {"description": "Books returned"}, status.HTTP_401_UNAUTHORIZED: {"description": "Unauthorized"}, status.HTTP_403_FORBIDDEN: {"description": "Invalid or expired token"}})
async def get_transaction_by_id(transaction_id: UUID, session: AsyncSession = Depends(get_session)):
    return await transaction_service.get_transaction_by_id(transaction_id=transaction_id, session=session)

@router.get("/by_user/{user_id}",response_model=List[TransactionModel], responses={status.HTTP_200_OK: {"description": "Books returned"}, status.HTTP_401_UNAUTHORIZED: {"description": "Unauthorized"}, status.HTTP_403_FORBIDDEN: {"description": "Invalid or expired token"}})
async def get_transaction_by_user_id(user_id: UUID, session: AsyncSession = Depends(get_session)):
    return await transaction_service.get_transaction_by_user_id(user_id=user_id, session=session)

@router.post("/withdrawals",response_model=TransactionModel, responses={status.HTTP_201_CREATED: {"description": "Withdrawal created"}, status.HTTP_400_BAD_REQUEST: {"description": "Invalid request body"}, status.HTTP_401_UNAUTHORIZED: {"description": "Unauthorized"}, status.HTTP_403_FORBIDDEN: {"description": "Invalid or expired token"}})
async def create_withdrawal(user_id: UUID, transaction_amount: WithdrawalCreate, session: AsyncSession = Depends(get_session)):
    return await transaction_service.create_withdrawal(user_id=user_id, transaction_amount=transaction_amount.transaction_amount, session=session)

@router.post("/deposits",response_model=TransactionModel, responses={status.HTTP_201_CREATED: {"description": "Deposit created"}, status.HTTP_400_BAD_REQUEST: {"description": "Invalid request body"}, status.HTTP_401_UNAUTHORIZED: {"description": "Unauthorized"}, status.HTTP_403_FORBIDDEN: {"description": "Invalid or expired token"}})
async def create_deposit(user_id: UUID, transaction_amount: DepositCreate, session: AsyncSession = Depends(get_session)):
    return await transaction_service.create_deposit(user_id=user_id, transaction_amount=transaction_amount.transaction_amount, session=session)

@router.post("/transfers",response_model=TransactionModel, responses={status.HTTP_201_CREATED: {"description": "Transfer created"}, status.HTTP_400_BAD_REQUEST: {"description": "Invalid request body"}, status.HTTP_401_UNAUTHORIZED: {"description": "Unauthorized"}, status.HTTP_403_FORBIDDEN: {"description": "Invalid or expired token"}})
async def create_transfer(user_id: UUID, transaction_amount: TransferCreate, session: AsyncSession = Depends(get_session)):
    return await transaction_service.create_transfer(user_id=user_id, transaction_amount=transaction_amount.transaction_amount, receiver_account_number=transaction_amount.receiver_account_number, session=session)

