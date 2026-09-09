from fastapi import status, APIRouter, Depends
from src.db.main import get_session
from .schemas import AccountModel, AccountStatusUpdateModel
from sqlalchemy.ext.asyncio import AsyncSession
from .services import AccountService

router = APIRouter()
account_service = AccountService()

@router.get('/', response_model=list[AccountModel],responses={status.HTTP_200_OK: {"description": "Accounts returned"}, status.HTTP_401_UNAUTHORIZED: {"description": "Unauthorized"}, status.HTTP_403_FORBIDDEN: {"description": "Invalid or expired token"}})
async def get_all_accounts(session: AsyncSession = Depends(get_session)):
    return await account_service.get_all_accounts(session)

@router.get('/{account_number}', response_model=AccountModel, responses={status.HTTP_200_OK: {"description": "Account returned"}, status.HTTP_401_UNAUTHORIZED: {"description": "Unauthorized"}, status.HTTP_403_FORBIDDEN: {"description": "Invalid or expired token"}})
async def get_account(account_number: str, session: AsyncSession = Depends(get_session)):
    return await account_service.get_account(account_number, session)

@router.patch('/{account_number}', response_model=AccountModel, responses={status.HTTP_200_OK: {"description": "Account status updated"}, status.HTTP_401_UNAUTHORIZED: {"description": "Unauthorized"}, status.HTTP_403_FORBIDDEN: {"description": "Invalid or expired token"}})
async def set_status(account_number: str, account_data: AccountStatusUpdateModel, session: AsyncSession = Depends(get_session)):
    return await account_service.set_status(account_number, account_data.status, session)