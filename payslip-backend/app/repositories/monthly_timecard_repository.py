from typing import Optional, Iterable
from app.repositories.base_repository import BaseRepository
import uuid
from sqlalchemy import select
from app.db.models.monthly_timecard import MonthlyTimecard
from app.utils.errors.DatabaseException import DatabaseException
from app.utils.errors.ResourceNotFoundException import ResourceNotFoundException

class MonthlyTimecardRepository(BaseRepository[MonthlyTimecard, uuid.UUID]):
    _timecard_not_found_msg = "Monthly Timecard not found"

    async def get(self, id: uuid.UUID) -> Optional[MonthlyTimecard]:
        try:
            timecard = await self._session.execute(select(MonthlyTimecard).where(MonthlyTimecard.id == id))
            if not timecard:
                raise ResourceNotFoundException(self._timecard_not_found_msg)
            return timecard.first()
        except Exception as e:
            raise DatabaseException(f"Failed to retrieve monthly timecard: {str(e)}")
        
    async def get_by_employee_id(self, employee_id: uuid.UUID) -> Iterable[MonthlyTimecard]:
        try:
            result = await self._session.execute(select(MonthlyTimecard).where(MonthlyTimecard.employee_id == employee_id))
            timecards = result.scalars().all()
            return timecards
        except Exception as e:
            raise DatabaseException(f"Failed to retrieve monthly timecards by employee ID: {str(e)}")
    
    async def create(self, entity: MonthlyTimecard) -> MonthlyTimecard:
        try:
            self._session.add(entity)
            await self._session.flush()
            return entity
        except Exception as e:
            raise DatabaseException(f"Failed to create monthly timecard: {str(e)}")
        
    async def get_all(self) -> Iterable[MonthlyTimecard]:
        try:
            result = await self._session.execute(select(MonthlyTimecard))
            timecards = result.scalars().all()
            return timecards
        except Exception as e:
            raise DatabaseException(f"Failed to retrieve monthly timecards: {str(e)}")
        
    async def delete(self, id: uuid.UUID) -> None:
        try:
            timecard = await self.get(id)
            if not timecard:
                raise ResourceNotFoundException(self._timecard_not_found_msg)
            await self._session.delete(timecard)
        except Exception as e:
            raise DatabaseException(f"Failed to delete monthly timecard: {str(e)}")
        
    async def update(self, entity: MonthlyTimecard) -> MonthlyTimecard:
        try:
            if not entity:
                raise ResourceNotFoundException(self._timecard_not_found_msg)
            await self._session.merge(entity)
            await self._session.flush()
            return entity
        except Exception as e:
            raise DatabaseException(f"Failed to update monthly timecard: {str(e)}")