from app.db.models.employee import Employee
from app.repositories.employee_repository import EmployeeRepository
from typing import Optional, Iterable
import uuid
from app.utils.errors import ResourceNotFoundException, DatabaseException, BaseAppException

class EmployeeService:
    def __init__(self, employee_repository: EmployeeRepository):
        self.employee_repository = employee_repository

    async def create_employee(self, employee: Employee) -> Employee:
        try:
            return await self.employee_repository.create(employee)
        except DatabaseException as e:
            raise e
        except Exception as e:
            raise BaseAppException(f"Failed to create employee: {str(e)}")
        
    async def get_employee_by_email(self, email: str
        ) -> Optional[Employee]:
        try:
            return await self.employee_repository.get_by_email(email)
        except ResourceNotFoundException as e:
            raise e
        except DatabaseException as e:
            raise e
        except Exception as e:
            raise BaseAppException(f"Failed to retrieve employee: {str(e)}")
        
    async def get_all_employees(self) -> Iterable[Employee]:
        try:
            return await self.employee_repository.get_all()
        except DatabaseException as e:
            raise e
        except Exception as e:
            raise BaseAppException(f"Failed to retrieve employees: {str(e)}")
        
    async def delete_employee(self, employee_id: uuid.UUID) -> None:
        try:
            await self.employee_repository.delete(employee_id)
        except ResourceNotFoundException as e:
            raise e
        except DatabaseException as e:
            raise e
        except Exception as e:
            raise BaseAppException(f"Failed to delete employee: {str(e)}")
        
    async def update_employee(self, employee: Employee
        ) -> Employee:
        try:
            return await self.employee_repository.update(employee)
        except ResourceNotFoundException as e:
            raise e
        except DatabaseException as e:
            raise e
        except Exception as e:
            raise BaseAppException(f"Failed to update employee: {str(e)}")

    async def get_employee_all_details(self, employee_id: uuid.UUID) -> Optional[Employee]:
        try:
            return await self.employee_repository.get_employee_all_details(employee_id)
        except ResourceNotFoundException as e:
            raise e
        except DatabaseException as e:
            raise e
        except Exception as e:
            raise BaseAppException(f"Failed to retrieve employee details: {str(e)}")
        
    async def is_manager(self, employee_id: uuid.UUID) -> bool:
        try:
            return await self.employee_repository.is_manager(employee_id)
        except DatabaseException as e:
            raise e
        except Exception as e:
            raise BaseAppException(f"Failed to check if employee is a manager: {str(e)}")
        
    async def get_managers(self) -> Iterable[Employee]:
        try:
            return await self.employee_repository.get_managers()
        except DatabaseException as e:
            raise e
        except Exception as e:
            raise BaseAppException(f"Failed to retrieve managers: {str(e)}")
    
    async def get_employees_by_manager_email(self, manager_email: str) -> Iterable[Employee]:
        try:
            return await self.employee_repository.get_by_manager_mail(manager_email)
        except DatabaseException as e:
            raise e
        except Exception as e:
            raise BaseAppException(f"Failed to retrieve employees by manager email: {str(e)}")
    