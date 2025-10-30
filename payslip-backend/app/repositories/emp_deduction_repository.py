from typing import Optional, Iterable
from app.db.models.emp_deduction import EmployeeDeduction
from app.repositories.base_repository import BaseRepository
import app.utils.errors as errors
import uuid
from sqlalchemy import select

class EmployeeDeductionRepository(BaseRepository[EmployeeDeduction, uuid.UUID]):
    _deduction_not_found_msg = "Employee Deduction not found"

    async def get(self, id: uuid.UUID) -> Optional[EmployeeDeduction]:
        try:
            deduction = await self._session.execute(select(EmployeeDeduction).where(EmployeeDeduction.id == id))
            if not deduction:
                raise errors.ResourceNotFoundException(self._deduction_not_found_msg)
            return deduction.first()
        except Exception as e:
            raise errors.DatabaseException(f"Failed to retrieve employee deduction: {str(e)}")
        
    async def create(self, entity: EmployeeDeduction) -> EmployeeDeduction:
        try:
            self._session.add(entity)
            await self._session.commit()
            await self._session.refresh(entity)
            return entity
        except Exception as e:
            await self._session.rollback()
            raise errors.DatabaseException(f"Failed to create employee deduction: {str(e)}")
        
    async def get_all(self) -> Iterable[EmployeeDeduction]:
        try:
            result = await self._session.execute(select(EmployeeDeduction))
            deductions = result.scalars().all()
            return deductions
        except Exception as e:
            raise errors.DatabaseException(f"Failed to retrieve employee deductions: {str(e)}")
        
    async def get_by_employee_id(self, employee_id: uuid.UUID) -> Iterable[EmployeeDeduction]:
        try:
            result = await self._session.execute(select(EmployeeDeduction).where(EmployeeDeduction.employee_id == employee_id))
            deductions = result.scalars().all()
            return deductions
        except Exception as e:
            raise errors.DatabaseException(f"Failed to retrieve employee deductions by employee ID: {str(e)}")
        
    async def delete(self, id: uuid.UUID) -> None:
        try:
            deduction = await self.get(id)
            if not deduction:
                raise errors.ResourceNotFoundException(self._deduction_not_found_msg)
            await self._session.delete(deduction)
            await self._session.commit()
        except Exception as e:
            await self._session.rollback()
            raise errors.DatabaseException(f"Failed to delete employee deduction: {str(e)}")
        
    async def update(self, entity: EmployeeDeduction) -> EmployeeDeduction:
        try:
            if not entity:
                raise errors.ResourceNotFoundException(self._deduction_not_found_msg)
            await self._session.merge(entity)
            await self._session.commit()
            await self._session.refresh(entity)
        except Exception as e:
            raise errors.DatabaseException(f"Failed to update employee deduction: {str(e)}")
        return entity