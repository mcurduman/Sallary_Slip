from typing import Optional, Iterable
from app.repositories.base_repository import BaseRepository
from app.utils.errors.DatabaseException import DatabaseException
from app.utils.errors.ResourceNotFoundException import ResourceNotFoundException
import uuid
from sqlalchemy import select
from app.db.models.emp_benefit import EmployeeBenefit

class EmployeeBenefitRepository(BaseRepository[EmployeeBenefit, uuid.UUID]):
    _benefit_not_found_msg = "Employee Benefit not found"

    async def get(self, id: uuid.UUID) -> Optional[EmployeeBenefit]:
        try:
            benefit = await self._session.execute(select(EmployeeBenefit).where(EmployeeBenefit.id == id))
            if not benefit:
                raise  ResourceNotFoundException(self._benefit_not_found_msg)
            return benefit.first()
        except Exception as e:
            raise  DatabaseException(f"Failed to retrieve employee benefit: {str(e)}")
        
    async def create(self, entity: EmployeeBenefit) -> EmployeeBenefit:
        try:
            self._session.add(entity)
            await self._session.flush()
            return entity
        except Exception as e:
            raise  DatabaseException(f"Failed to create employee benefit: {str(e)}")
        
    async def get_all(self) -> Iterable[EmployeeBenefit]:
        try:
            result = await self._session.execute(select(EmployeeBenefit))
            benefits = result.scalars().all()
            return benefits
        except Exception as e:
            raise  DatabaseException(f"Failed to retrieve employee benefits: {str(e)}")
        
    async def get_by_employee_id(self, employee_id: uuid.UUID) -> Iterable[EmployeeBenefit]:
        try:
            result = await self._session.execute(select(EmployeeBenefit).where(EmployeeBenefit.employee_id == employee_id))
            benefits = result.scalars().all()
            return benefits
        except Exception as e:
            raise  DatabaseException(f"Failed to retrieve employee benefits by employee ID: {str(e)}")
        
    async def delete(self, id: uuid.UUID) -> None:
        try:
            benefit = await self.get(id)
            if not benefit:
                raise  ResourceNotFoundException(self._benefit_not_found_msg)
            await self._session.delete(benefit)
        except Exception as e:
            raise  DatabaseException(f"Failed to delete employee benefit: {str(e)}")
        
    async def update(self, entity: EmployeeBenefit) -> EmployeeBenefit:
        try:
            if not entity:
                raise  ResourceNotFoundException(self._benefit_not_found_msg)
            await self._session.merge(entity)
            await self._session.flush()
            return entity
        except Exception as e:
            raise  DatabaseException(f"Failed to update employee benefit: {str(e)}")