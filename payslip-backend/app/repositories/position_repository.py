from typing import Optional, Iterable
from app.db.models.position import Position
from app.repositories.base_repository import BaseRepository
import app.utils.errors as errors
import uuid
from sqlalchemy import select, delete

class PositionRepository(BaseRepository[Position,   uuid.UUID]):
    _pos_not_found_msg = "Position not found"

    async def get(self, id: uuid.UUID) -> Optional[Position]:
        try:
            position = await self._session.execute(select(Position).where(Position.id == id))
            if not position:
                raise errors.ResourceNotFoundException(self._pos_not_found_msg)
            return position.first()
        except Exception as e:
            raise errors.DatabaseException(f"Failed to retrieve position: {str(e)}")

    async def get_by_name(self, name: str) -> Optional[Position]:
        try:
            position = await self._session.execute(select(Position).where(Position.name == name))
            if not position:
                raise errors.ResourceNotFoundException(self._pos_not_found_msg)
            return position
        except Exception as e:
            raise errors.DatabaseException(f"Failed to retrieve position: {str(e)}")
    
    async def create(self, entity: Position) -> Position:
        try:
            self._session.add(entity)
            await self._session.commit()
            await self._session.refresh(entity)
            return entity
        except Exception as e:
            await self._session.rollback()
            raise errors.DatabaseException(f"Failed to create position: {str(e)}")

    async def get_all(self) -> Iterable[Position]:
        try:
            result = await self._session.execute(select(Position))
            positions = result.scalars().all()
            return positions
        except Exception as e:
            raise errors.DatabaseException(f"Failed to retrieve positions: {str(e)}")

    async def delete(self, id: uuid.UUID) -> None:
        try:
            position = await self.get(id)
            if not position:
                raise errors.ResourceNotFoundException(self._pos_not_found_msg)
            await self._session.execute(delete(Position).where(Position.id == id))
            await self._session.commit()
        except Exception as e:
            await self._session.rollback()
            raise errors.DatabaseException(f"Failed to delete position: {str(e)}")

    async def update(self, entity: Position) -> Position:
        try:
            if not entity:
                raise errors.ResourceNotFoundException("Position not found")
            await self._session.merge(entity)
            await self._session.commit()
            await self._session.refresh(entity)
            return entity
        except Exception as e:
            await self._session.rollback()
            raise errors.DatabaseException(f"Failed to update position: {str(e)}")
