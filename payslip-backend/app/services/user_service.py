from app.repositories.user_repository import UserRepository
from app.schemas.user.user_create import UserCreate
from app.db.models.user import User
from app.schemas.user.user_response import UserResponse
from app.utils.errors.DatabaseException import DatabaseException
from app.utils.errors.ResourceNotFoundException import ResourceNotFoundException
from app.utils.errors.BaseAppException import BaseAppException
from app.utils.errors.UnauthorizedException import UnauthorizedException
from app.core.auth.jwt import verify_password, get_password_hash
from typing import Optional, Iterable
from pydantic import EmailStr


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def create_user(self, user: UserCreate) -> UserResponse:
        from app.db.models.user_role import UserRoleModel
        try:
            if await self.user_repository.user_exists(user.email):
                raise ValueError("User with this email already exists")
            db_user = User(
                email=user.email,
                username=user.username,
                hashed_password=get_password_hash(user.password),
                roles=[UserRoleModel(role=role) for role in user.roles]

            )
            created_user = await self.user_repository.create(db_user)
            user_dict = created_user.__dict__.copy()
            user_dict['roles'] = [role.role for role in created_user.roles]
            return UserResponse.model_validate(user_dict)
        except DatabaseException as e:
            raise e
        except Exception as e:
            raise BaseAppException(f"Failed to create user: {str(e)}")

    async def get_user_by_email(self, email: EmailStr) -> Optional[UserResponse]:
        try:
            user = await self.user_repository.get_by_email(email)
            if user:
                user_dict = user.__dict__.copy()
                user_dict['roles'] = [role.role for role in user.roles]
                return UserResponse.model_validate(user_dict)
            return None
        except ResourceNotFoundException as e:
            raise e
        except DatabaseException as e:
            raise e
        except Exception as e:
            raise BaseAppException(f"Failed to retrieve user: {str(e)}")
        
    async def get_user_by_username(self, username: str) -> Optional[UserResponse]:
        try:
            user = await self.user_repository.get_by_username(username)
            if user:
                user_dict = user.__dict__.copy()
                user_dict['roles'] = [role.role for role in user.roles]
                return UserResponse.model_validate(user_dict)
            return None
        except ResourceNotFoundException as e:
            raise e
        except DatabaseException as e:
            raise e
        except Exception as e:
            raise BaseAppException(f"Failed to retrieve user: {str(e)}")

    async def get_all_users(self) -> Iterable[UserResponse]:
        try:
            users = await self.user_repository.get_all()
            user_responses = []
            for user in users:
                user_dict = user.__dict__.copy()
                user_dict['roles'] = [role.role for role in user.roles]
                user_responses.append(UserResponse.model_validate(user_dict))
            return user_responses
        except DatabaseException as e:
            raise e
        except Exception as e:
            raise BaseAppException(f"Failed to retrieve users: {str(e)}")

    async def authenticate_user(self, username: str, password: str) -> Optional[UserResponse]:
        try:
            user = await self.user_repository.get_by_username(username)
            if user and verify_password(password, user.hashed_password):
                user_dict = user.__dict__.copy()
                user_dict['roles'] = [role.role for role in user.roles]
                return UserResponse.model_validate(user_dict)
            return None
        except ResourceNotFoundException:
            return None
        except DatabaseException as e:
            raise e
        except UnauthorizedException as e:
            raise e
        except Exception as e:
            raise BaseAppException(f"Failed to authenticate user: {str(e)}")