
from typing import Optional, Iterable
import uuid
from app.db.models.user import User
from app.repositories.base_repository import BaseRepository
from sqlalchemy import select
from app.utils.errors.DatabaseException import DatabaseException
from app.utils.errors.ResourceNotFoundException import ResourceNotFoundException


class UserRepository(BaseRepository[User, str]):
    _user_not_found_msg = "User not found"

    async def get_by_email(self, email: str) -> Optional[User]:
        try:
            result = await self._session.execute(select(User).where(User.email == email))
            user = result.scalars().first()
            if not user:
                raise ResourceNotFoundException(self._user_not_found_msg)
            return user
        except Exception as e:
            raise DatabaseException(f"Failed to retrieve user: {str(e)}")
    
    async def get_by_username(self, username: str) -> Optional[User]:
        try:
            result = await self._session.execute(select(User).where(User.username == username))
            user = result.scalars().first()
            if not user:
                raise ResourceNotFoundException(self._user_not_found_msg)
            return user
        except Exception as e:
            raise DatabaseException(f"Failed to retrieve user: {str(e)}")

    async def user_exists(self, email: str) -> bool:
        try:
            result = await self._session.execute(select(User).where(User.email == email))
            user = result.scalars().first()
            return user is not None
        except Exception as e:
            raise DatabaseException(f"Failed to check user existence: {str(e)}")
        
    async def create(self, entity: User) -> User:
        try:
            self._session.add(entity)
            await self._session.flush()
            return entity
        except Exception as e:
            raise DatabaseException(f"Failed to create user: {str(e)}")

    async def get_all(self) -> Iterable[User]:
        try:
            result = await self._session.execute(select(User))
            users = result.scalars().all()
            return users
        except Exception as e:
            raise DatabaseException(f"Failed to retrieve users: {str(e)}")

    async def delete(self, id: uuid.UUID) -> None:
        try:
            user = await self.get(id)
            if not user:
                raise ResourceNotFoundException(self._user_not_found_msg)
            await self._session.delete(user)
        except Exception as e:
            raise DatabaseException(f"Failed to delete user: {str(e)}")

    async def update(self, entity: User) -> User:
        try:
            if not entity:
                raise ResourceNotFoundException(self._user_not_found_msg)
            await self._session.merge(entity)
            await self._session.flush()
            return entity
        except Exception as e:
            raise DatabaseException(f"Failed to update user: {str(e)}")

