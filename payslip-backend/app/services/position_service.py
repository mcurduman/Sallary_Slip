from app.repositories.position_repository import PositionRepository
from app.db.models.position import Position
from app.utils.errors import ResourceNotFoundException, DatabaseException, BaseAppException

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
        
    async def get_position_by_id(self, position_id: str) -> Position:
        try:
            return await self.position_repository.get(position_id)
        except ResourceNotFoundException as e:
            raise e
        except DatabaseException as e:
            raise e
        except Exception as e:
            raise BaseAppException(f"Failed to retrieve position: {str(e)}")
            
    async def get_all_positions(self) -> list[Position]:
        try:
            return await self.position_repository.get_all()
        except DatabaseException as e:
            raise e
        except Exception as e:
            raise BaseAppException(f"Failed to retrieve positions: {str(e)}")

    async def delete_position(self, position_id: str) -> None:
        try:
            await self.position_repository.delete(position_id)
        except ResourceNotFoundException as e:
            raise e
        except DatabaseException as e:
            raise e
        except Exception as e:
            raise BaseAppException(f"Failed to delete position: {str(e)}")
        
    async def update_position(self, position: Position) -> Position:
        try:
            return await self.position_repository.update(position)
        except ResourceNotFoundException as e:
            raise e
        except DatabaseException as e:
            raise e
        except Exception as e:
            raise BaseAppException(f"Failed to update position: {str(e)}")