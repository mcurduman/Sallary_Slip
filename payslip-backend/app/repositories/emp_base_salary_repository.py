from typing import Optional, Iterable
from app.repositories.base_repository import BaseRepository
import uuid
from sqlalchemy import select, delete
from app.db.models.emp_base_salary import EmployeeBaseSalary
from app.utils.errors.DatabaseException import DatabaseException
from app.utils.errors.ResourceNotFoundException import ResourceNotFoundException

class EmployeeBaseSalaryRepository(BaseRepository[EmployeeBaseSalary, uuid.UUID]):
    _base_salary_not_found_msg = "Employee Base Salary not found"

    async def get(self, id: uuid.UUID) -> Optional[EmployeeBaseSalary]:
        try:
            base_salary = await self._session.execute(select(EmployeeBaseSalary).where(EmployeeBaseSalary.id == id))
            if not base_salary:
                raise ResourceNotFoundException(self._base_salary_not_found_msg)
            return base_salary.first()
        except Exception as e:
            raise DatabaseException(f"Failed to retrieve employee base salary: {str(e)}")
        
    async def get_by_employee_id(self, employee_id: uuid.UUID) -> Optional[EmployeeBaseSalary]:
        try:
            base_salary = await self._session.execute(select(EmployeeBaseSalary).where(EmployeeBaseSalary.employee_id == employee_id))
            if not base_salary:
                raise ResourceNotFoundException(self._base_salary_not_found_msg)
            return base_salary.first()
        except Exception as e:
            raise DatabaseException(f"Failed to retrieve employee base salary by employee ID: {str(e)}")

    async def create(self, entity: EmployeeBaseSalary) -> EmployeeBaseSalary:
        try:
            self._session.add(entity)
            await self._session.flush()
            return entity
        except Exception as e:
            raise  DatabaseException(f"Failed to create employee base salary: {str(e)}")
        
    async def get_all(self) -> Iterable[EmployeeBaseSalary]:
        try:
            result = await self._session.execute(select(EmployeeBaseSalary))
            base_salaries = result.scalars().all()
            return base_salaries
        except Exception as e:
            raise  DatabaseException(f"Failed to retrieve employee base salaries: {str(e)}")
        
    async def delete(self, id: uuid.UUID) -> None:
        try:
            base_salary = await self.get(id)
            if not base_salary:
                raise  ResourceNotFoundException(self._base_salary_not_found_msg)
            await self._session.execute(delete(EmployeeBaseSalary).where(EmployeeBaseSalary.id == id))
        except Exception as e:
            raise  DatabaseException(f"Failed to delete employee base salary: {str(e)}")
        
    async def update(self, entity: EmployeeBaseSalary) -> EmployeeBaseSalary:
        try:
            if not entity:
                raise  ResourceNotFoundException(self._base_salary_not_found_msg)
            await self._session.merge(entity)
            await self._session.flush()
            return entity
        except Exception as e:
            raise  DatabaseException(f"Failed to update employee base salary: {str(e)}")