from app.repositories.position_repository import PositionRepository
from app.db.models.position import Position
from typing import Iterable
import uuid
from app.utils.errors.DatabaseException import DatabaseException
from app.utils.errors.ResourceNotFoundException import ResourceNotFoundException
from app.utils.errors.BaseAppException import BaseAppException

class PositionService:
    def __init__(self, position_repository: PositionRepository):
        self.position_repository = position_repository

    async def create_position(self, position: Position) -> Position:
        try:
            return await self.position_repository.create(position)
        except DatabaseException as e:
            raise e
        except Exception as e:
            raise BaseAppException(f"Failed to create position: {str(e)}")

    async def get_position_by_id(self, position_id: uuid.UUID) -> Position:
        try:
            return await self.position_repository.get(position_id)
        except ResourceNotFoundException as e:
            raise e
        except DatabaseException as e:
            raise e
        except Exception as e:
            raise BaseAppException(f"Failed to retrieve position: {str(e)}")

    async def get_all_positions(self) -> Iterable[Position]:
        try:
            return await self.position_repository.get_all()
        except DatabaseException as e:
            raise e
        except Exception as e:
            raise BaseAppException(f"Failed to retrieve positions: {str(e)}")
