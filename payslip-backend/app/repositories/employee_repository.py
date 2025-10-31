from typing import Optional, Iterable
from app.db.models.employee import Employee
from app.repositories.base_repository import BaseRepository
import app.utils.errors as errors
import uuid
from sqlalchemy import select
from sqlalchemy.orm import joinedload

class EmployeeRepository(BaseRepository[Employee, uuid.UUID]):
    _emp_not_found_msg = "Employee not found"

    async def get(self, id: uuid.UUID) -> Optional[Employee]:
        try:
            employee = await self._session.execute(select(Employee).where(Employee  .id == id))
            if not employee:
                raise errors.ResourceNotFoundException(self._emp_not_found_msg)
            return employee.first()
        except Exception as e:
            raise errors.DatabaseException(f"Failed to retrieve employee: {str(e)}")

    async def get_by_email(self, email: str) -> Optional[Employee]:
        try:
            employee = await self._session.execute(select(Employee).where(Employee.email == email))
            if not employee:
                raise errors.ResourceNotFoundException(self._emp_not_found_msg)
            return employee.first()
        except Exception as e:
            raise errors.DatabaseException(f"Failed to retrieve employee: {str(e)}")

    async def get_by_manager_id(self, manager_id: uuid.UUID) -> Iterable[Employee]:
        try:
            employees = await self._session.execute(select(Employee).where(Employee.manager_id == manager_id))
            return employees.scalars().all()
        except Exception as e:
            raise errors.DatabaseException(f"Failed to retrieve employees by manager ID: {str(e)}")

    async def get_managers(self) -> Iterable[Employee]:
        try:
            result = await self._session.execute(
                select(Employee).where(Employee.id.in_(
                    select(Employee.manager_id).distinct().where(Employee.manager_id.isnot(None))
                ))
            )
            managers = result.scalars().all()
            return managers
        except Exception as e:
            raise errors.DatabaseException(f"Failed to retrieve managers: {str(e)}")
        
    async def get_employee_all_details(self, employee_id: uuid.UUID) -> Optional[Employee]:
        try:
            result = await self._session.execute(
            select(Employee)
            .where(Employee.id == employee_id)
            .options(
                joinedload(Employee.position),
                joinedload(Employee.discipline)
            )
            )
            employee = result.scalars().first()
            if not employee:
                raise errors.ResourceNotFoundException(self._emp_not_found_msg)
            return employee
        except Exception as e:
            raise errors.DatabaseException(f"Failed to retrieve employee details: {str(e)}")
    
    async def is_manager(self, employee_id: uuid.UUID) -> bool:
        try:
            result = await self._session.execute(
                select(Employee).where(Employee.manager_id == employee_id)
            )
            employees = result.scalars().all()
            return len(employees) > 0
        except Exception as e:
            raise errors.DatabaseException(f"Failed to check if employee is a manager: {str(e)}")

    async def create(self, entity: Employee) -> Employee:
        try:
            self._session.add(entity)
            await self._session.commit()
            await self._session.refresh(entity)
            return entity
        except Exception as e:
            await self._session.rollback()
            raise errors.DatabaseException(f"Failed to create employee: {str(e)}")

    async def get_all(self) -> Iterable[Employee]:
        try:
            result = await self._session.execute(select(Employee))
            employees = result.scalars().all()
            return employees
        except Exception as e:
            raise errors.DatabaseException(f"Failed to retrieve employees: {str(e)}")

    async def delete(self, id: uuid.UUID) -> None:
        try:
            employee = await self.get(id)
            if not employee:
                raise errors.ResourceNotFoundException(self._emp_not_found_msg)
            await self._session.delete(employee)
            await self._session.commit()
        except Exception as e:
            await self._session.rollback()
            raise errors.DatabaseException(f"Failed to delete employee: {str(e)}")

    async def update(self, entity: Employee) -> Employee:
        try:
            await self._session.merge(entity)
            await self._session.commit()
            await self._session.refresh(entity)
            return entity
        except Exception as e:
            await self._session.rollback()
            raise errors.DatabaseException(f"Failed to update position: {str(e)}")