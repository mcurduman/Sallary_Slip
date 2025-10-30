from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import AsyncSessionLocal
from app.services.user_service import UserService
from app.repositories.user_repository import UserRepository

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session

async def get_user_service():
    async with AsyncSessionLocal() as session:
        repo = UserRepository(session)
        return UserService(repo)

        