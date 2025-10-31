from app.repositories.user_repository import UserRepository
from app.db.models.user import User
from app.utils.errors import ResourceNotFoundException, DatabaseException, BaseAppException
from typing import Optional, Iterable
from pydantic import EmailStr
class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def create_user(self, user: User) -> User:
        try:
            existing_car = await self.user_repository.get_by_email(user.email)
            if existing_car:
                raise ValueError("User with this email already exists")
            return await self.user_repository.create(user)
        except DatabaseException as e:
            raise e
        except Exception as e:
            raise BaseAppException(f"Failed to create user: {str(e)}")

    async def get_user_by_email(self, email: EmailStr) -> Optional[User]:
        try:
            return await self.user_repository.get_by_email(email)
        except ResourceNotFoundException as e:
            raise e
        except DatabaseException as e:
            raise e
        except Exception as e:
            raise BaseAppException(f"Failed to retrieve user: {str(e)}")
            
    async def get_all_users(self) -> Iterable[User]:
        try:
            return await self.user_repository.get_all()
        except DatabaseException as e:
            raise e
        except Exception as e:
            raise BaseAppException(f"Failed to retrieve users: {str(e)}")

    async def delete_user(self, user_id: str) -> None:
        try:
            await self.user_repository.delete(user_id)
        except ResourceNotFoundException as e:
            raise e
        except DatabaseException as e:
            raise e
        except Exception as e:
            raise BaseAppException(f"Failed to delete user: {str(e)}")

    