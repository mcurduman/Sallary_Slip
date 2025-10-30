from typing import Optional, Iterable
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from app.db.models.discipline import Discipline
import app.utils.errors as errors

class DisciplineRepository:
	_discipline_not_found_msg = "Discipline not found"
	
	def __init__(self, session: AsyncSession):
		self._session = session

	async def get(self, id) -> Optional[Discipline]:
		try:
			result = await self._session.execute(select(Discipline).where(Discipline.id == id))
			if not result:
				raise errors.ResourceNotFoundException(errors._discipline_not_found_msg)
			return result.first()
		except Exception as e:
			raise errors.DatabaseException(f"Failed to retrieve discipline: {str(e)}")      

	async def get_all(self) -> Iterable[Discipline]:
		try:
			result = await self._session.execute(select(Discipline))
			disciplines = result.scalars().all()
			return disciplines
		except Exception as e:
			raise errors.DatabaseException(f"Failed to retrieve disciplines: {str(e)}") 

	async def create(self, entity: Discipline) -> Discipline:
		try:
			self._session.add(entity)
			await self._session.commit()
			await self._session.refresh(entity)
			return entity
		except Exception as e:
			raise errors.DatabaseException(f"Failed to create discipline: {str(e)}")

	async def delete(self, id) -> None:
		try:
			discipline = await self.get(id)
			if not discipline:
				raise errors.ResourceNotFoundException(self._discipline_not_found_msg)
			await self._session.execute(delete(Discipline).where(Discipline.id == id))
			await self._session.commit()
		except Exception as e:
			raise errors.DatabaseException(f"Failed to delete discipline: {str(e)}")

	async def update(self, entity: Discipline) -> Discipline:
		try:
			await self._session.merge(entity)
			await self._session.commit()
			await self._session.refresh(entity)
		except Exception as e:
			raise errors.DatabaseException(f"Failed to update discipline: {str(e)}")
		return entity
