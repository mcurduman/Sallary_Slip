from typing import Optional, Iterable
from app.db.models.position import Position
from app.repositories.base_repository import BaseRepository
import uuid
from sqlalchemy import select, delete
from app.utils.errors.DatabaseException import DatabaseException
from app.utils.errors.ResourceNotFoundException import ResourceNotFoundException

class PositionRepository(BaseRepository[Position,   uuid.UUID]):
    _pos_not_found_msg = "Position not found"

    async def get(self, id: uuid.UUID) -> Optional[Position]:
        try:
            position = await self._session.execute(select(Position).where(Position.id == id))
            if not position:
                raise ResourceNotFoundException(self._pos_not_found_msg)
            return position.first()
        except Exception as e:
            raise DatabaseException(f"Failed to retrieve position: {str(e)}")

    async def get_by_name(self, name: str) -> Optional[Position]:
        try:
            position = await self._session.execute(select(Position).where(Position.name == name))
            if not position:
                raise ResourceNotFoundException(self._pos_not_found_msg)
            return position
        except Exception as e:
            raise DatabaseException(f"Failed to retrieve position: {str(e)}")
    
    async def create(self, entity: Position) -> Position:
        try:
            self._session.add(entity)
            await self._session.flush()
            return entity
        except Exception as e:
            raise DatabaseException(f"Failed to create position: {str(e)}")

    async def get_all(self) -> Iterable[Position]:
        try:
            result = await self._session.execute(select(Position))
            positions = result.scalars().all()
            return positions
        except Exception as e:
            raise DatabaseException(f"Failed to retrieve positions: {str(e)}")

    async def delete(self, id: uuid.UUID) -> None:
        try:
            position = await self.get(id)
            if not position:
                raise ResourceNotFoundException(self._pos_not_found_msg)
            await self._session.execute(delete(Position).where(Position.id == id))
        except Exception as e:
            raise DatabaseException(f"Failed to delete position: {str(e)}")

    async def update(self, entity: Position) -> Position:
        try:
            if not entity:
                raise ResourceNotFoundException("Position not found")
            await self._session.merge(entity)
            await self._session.flush()
            return entity
        except Exception as e:
            raise DatabaseException(f"Failed to update position: {str(e)}")
