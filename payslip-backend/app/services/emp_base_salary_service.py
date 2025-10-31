from app.db.models.emp_base_salary import EmployeeBaseSalary
from app.repositories.emp_base_salary_repository import EmployeeBaseSalaryRepository
from typing import Optional, Iterable
import uuid
import app.utils.errors as errors
from app.utils.errors import ResourceNotFoundException, DatabaseException, BaseAppException
class EmpBaseSalaryService:
    def __init__(self, emp_base_salary_repository: EmployeeBaseSalaryRepository):
        self.emp_base_salary_repository = emp_base_salary_repository

    async def create_emp_base_salary(self, emp_base_salary: EmployeeBaseSalary) -> EmployeeBaseSalary:
        try:
            return await self.emp_base_salary_repository.create(emp_base_salary)
        except DatabaseException as e:
            raise e
        except Exception as e:
            raise BaseAppException(f"Failed to create employee base salary: {str(e)}")
        
    async def get_emp_base_salary_by_id(self, emp_base_salary_id: uuid.UUID
        ) -> EmployeeBaseSalary:
        try:
            return await self.emp_base_salary_repository.get(emp_base_salary_id)
        except ResourceNotFoundException as e:
            raise e
        except DatabaseException as e:
            raise e
        except Exception as e:
            raise BaseAppException(f"Failed to retrieve employee base salary: {str(e)}")
        
    async def get_all_emp_base_salaries(self) -> Iterable[EmployeeBaseSalary]:
        try:
            return await self.emp_base_salary_repository.get_all()
        except DatabaseException as e:
            raise e
        except Exception as e:
            raise BaseAppException(f"Failed to retrieve employee base salaries: {str(e)}")
        
    async def delete_emp_base_salary(self, emp_base_salary_id: uuid.UUID) -> None:
        try:
            await self.emp_base_salary_repository.delete(emp_base_salary_id)
        except ResourceNotFoundException as e:
            raise e
        except DatabaseException as e:
            raise e
        except Exception as e:
            raise BaseAppException(f"Failed to delete employee base salary: {str(e)}")
        
    async def update_emp_base_salary(self, emp_base_salary: EmployeeBaseSalary
        ) -> EmployeeBaseSalary:
        try:
            return await self.emp_base_salary_repository.update(emp_base_salary)
        except ResourceNotFoundException as e:
            raise e
        except DatabaseException as e:
            raise e
        except Exception as e:
            raise BaseAppException(f"Failed to update employee base salary: {str(e)}")