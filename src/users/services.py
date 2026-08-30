from uuid import UUID
from fastapi import HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas import PatchUserModel
from sqlmodel import select, desc
from src.db.models import UserModel as UserTable

class UserService:
    async def get_all_users(self, session: AsyncSession):
        query = select(UserTable).order_by(desc(UserTable.created_at))
        result = await session.exec(query)
        users = result.all()
        return users

    async def get_user_by_id(self, user_id: UUID, session: AsyncSession):
        query = select(UserTable).where(UserTable.user_id == user_id)
        result = await session.exec(query)
        user = result.first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user

    async def update_user(self, user_id: UUID, user_data: PatchUserModel, session: AsyncSession):
        user_to_update = await self.get_user_by_id(user_id, session)
        update_data_dict = user_data.model_dump(exclude_unset=True)
        for k, v in update_data_dict.items():
            setattr(user_to_update, k, v)
        await session.commit()
        return user_to_update

    async def delete_user(self, user_id: UUID, session: AsyncSession):
        user_to_delete = await self.get_user_by_id(user_id, session)
        await session.delete(user_to_delete)
        await session.commit()
        return user_to_delete