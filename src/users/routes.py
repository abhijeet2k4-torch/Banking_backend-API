from uuid import UUID
from fastapi import status, APIRouter, Depends
from src.db.main import get_session
from .schemas import UserModel, PatchUserModel
from sqlalchemy.ext.asyncio import AsyncSession
from .services import UserService

router = APIRouter()
user_service = UserService()

@router.get('/',response_model=list[UserModel], responses={status.HTTP_200_OK: {"description": "Users returned"}, status.HTTP_401_UNAUTHORIZED: {"description": "Unauthorized"}, status.HTTP_403_FORBIDDEN: {"description": "Invalid or expired token"}})
async def get_users(session: AsyncSession=Depends(get_session)):
    return await user_service.get_all_users(session)

@router.get('/{user_id}',response_model=UserModel, responses={status.HTTP_200_OK: {"description": "User returned"}, status.HTTP_401_UNAUTHORIZED: {"description": "Unauthorized"}, status.HTTP_403_FORBIDDEN: {"description": "Invalid or expired token"}})
async def get_user(user_id: UUID, session: AsyncSession=Depends(get_session)):
    return await user_service.get_user_by_id(str(user_id), session)

@router.patch('/{user_id}',response_model=UserModel, responses={status.HTTP_200_OK: {"description": "User updated"}, status.HTTP_401_UNAUTHORIZED: {"description": "Unauthorized"}, status.HTTP_403_FORBIDDEN: {"description": "Invalid or expired token"}})
async def update_user(user_id: UUID, user_data: PatchUserModel, session: AsyncSession=Depends(get_session)):
    return await user_service.update_user(str(user_id), user_data, session)

@router.delete('/{user_id}',response_model=UserModel, responses={status.HTTP_200_OK: {"description": "User deleted"}, status.HTTP_401_UNAUTHORIZED: {"description": "Unauthorized"}, status.HTTP_403_FORBIDDEN: {"description": "Invalid or expired token"}})
async def delete_user(user_id: UUID, session: AsyncSession=Depends(get_session)):
    return await user_service.delete_user(str(user_id), session)
