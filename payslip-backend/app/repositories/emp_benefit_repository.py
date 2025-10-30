from typing import Optional, Iterable
from app.repositories.base_repository import BaseRepository
import app.utils.errors as errors
import uuid
from sqlalchemy import select
from app.db.models.emp_benefit import EmployeeBenefit

class EmployeeBenefitRepository(BaseRepository[EmployeeBenefit, uuid.UUID]):
    _benefit_not_found_msg = "Employee Benefit not found"

    async def get(self, id: uuid.UUID) -> Optional[EmployeeBenefit]:
        try:
            benefit = await self._session.execute(select(EmployeeBenefit).where(EmployeeBenefit.id == id))
            if not benefit:
                raise errors.ResourceNotFoundException(self._benefit_not_found_msg)
            return benefit.first()
        except Exception as e:
            raise errors.DatabaseException(f"Failed to retrieve employee benefit: {str(e)}")
        
    async def create(self, entity: EmployeeBenefit) -> EmployeeBenefit:
        try:
            self._session.add(entity)
            await self._session.commit()
            await self._session.refresh(entity)
            return entity
        except Exception as e:
            await self._session.rollback()
            raise errors.DatabaseException(f"Failed to create employee benefit: {str(e)}")
        
    async def get_all(self) -> Iterable[EmployeeBenefit]:
        try:
            result = await self._session.execute(select(EmployeeBenefit))
            benefits = result.scalars().all()
            return benefits
        except Exception as e:
            raise errors.DatabaseException(f"Failed to retrieve employee benefits: {str(e)}")
        
    async def get_by_employee_id(self, employee_id: uuid.UUID) -> Iterable[EmployeeBenefit]:
        try:
            result = await self._session.execute(select(EmployeeBenefit).where(EmployeeBenefit.employee_id == employee_id))
            benefits = result.scalars().all()
            return benefits
        except Exception as e:
            raise errors.DatabaseException(f"Failed to retrieve employee benefits by employee ID: {str(e)}")
        
    async def delete(self, id: uuid.UUID) -> None:
        try:
            benefit = await self.get(id)
            if not benefit:
                raise errors.ResourceNotFoundException(self._benefit_not_found_msg)
            await self._session.delete(benefit)
            await self._session.commit()
        except Exception as e:
            await self._session.rollback()
            raise errors.DatabaseException(f"Failed to delete employee benefit: {str(e)}")
        
    async def update(self, entity: EmployeeBenefit) -> EmployeeBenefit:
        try:
            if not entity:
                raise errors.ResourceNotFoundException(self._benefit_not_found_msg)
            await self._session.merge(entity)
            await self._session.commit()
            await self._session.refresh(entity)
            return entity
        except Exception as e:
            await self._session.rollback()
            raise errors.DatabaseException(f"Failed to update employee benefit: {str(e)}")