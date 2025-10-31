from app.repositories.discipline_repository import DisciplineRepository
from app.db.models.discipline import Discipline
from app.utils.errors import ResourceNotFoundException, DatabaseException, BaseAppException

class DisciplineService:
    def __init__(self, discipline_repository: DisciplineRepository):
        self.discipline_repository = discipline_repository

    async def create_discipline(self, discipline: Discipline) -> Discipline:
        try:
            return await self.discipline_repository.create(discipline)
        except DatabaseException as e:
            raise e
        except Exception as e:
            raise BaseAppException(f"Failed to create discipline: {str(e)}")
        
    async def get_discipline_by_id(self, discipline_id: str) -> Discipline:
        try:
            return await self.discipline_repository.get(discipline_id)
        except ResourceNotFoundException as e:
            raise e
        except DatabaseException as e:
            raise e
        except Exception as e:
            raise BaseAppException(f"Failed to retrieve discipline: {str(e)}")
            
    async def get_all_disciplines(self) -> list[Discipline]:
        try:
            return await self.discipline_repository.get_all()
        except DatabaseException as e:
            raise e
        except Exception as e:
            raise BaseAppException(f"Failed to retrieve disciplines: {str(e)}")

    async def delete_discipline(self, discipline_id: str) -> None:
        try:
            await self.discipline_repository.delete(discipline_id)
        except ResourceNotFoundException as e:
            raise e
        except DatabaseException as e:
            raise e
        except Exception as e:
            raise BaseAppException(f"Failed to delete discipline: {str(e)}")