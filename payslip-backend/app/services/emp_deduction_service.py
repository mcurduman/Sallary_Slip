from app.db.models.emp_deduction import EmployeeDeduction
from app.repositories.emp_deduction_repository import EmployeeDeductionRepository
from typing import Optional, Iterable
import uuid
from app.utils.errors import ResourceNotFoundException, DatabaseException, BaseAppException

class EmpDeductionService:
    def __init__(self, emp_deduction_repository: EmployeeDeductionRepository):
        self.emp_deduction_repository = emp_deduction_repository

    async def create_emp_deduction(self, emp_deduction: EmployeeDeduction) -> EmployeeDeduction:
        try:
            return await self.emp_deduction_repository.create(emp_deduction)
        except DatabaseException as e:
            raise e
        except Exception as e:
            raise BaseAppException(f"Failed to create employee deduction: {str(e)}")
        
    async def get_emp_deduction_by_id(self, emp_deduction_id: uuid.UUID
        ) -> Optional[EmployeeDeduction]:
        try:
            return await self.emp_deduction_repository.get(emp_deduction_id)
        except ResourceNotFoundException as e:
            raise e
        except DatabaseException as e:
            raise e
        except Exception as e:
            raise BaseAppException(f"Failed to retrieve employee deduction: {str(e)}")
        
    async def get_all_emp_deductions(self) -> Iterable[EmployeeDeduction]:
        try:
            return await self.emp_deduction_repository.get_all()
        except DatabaseException as e:
            raise e
        except Exception as e:
            raise BaseAppException(f"Failed to retrieve employee deductions: {str(e)}")
        
    async def delete_emp_deduction(self, emp_deduction_id: uuid.UUID) -> None:
        try:
            await self.emp_deduction_repository.delete(emp_deduction_id)
        except ResourceNotFoundException as e:
            raise e
        except DatabaseException as e:
            raise e
        except Exception as e:
            raise BaseAppException(f"Failed to delete employee deduction: {str(e)}")
    
    async def update_emp_deduction(self, emp_deduction: EmployeeDeduction
        ) -> EmployeeDeduction:
        try:
            return await self.emp_deduction_repository.update(emp_deduction)
        except ResourceNotFoundException as e:
            raise e
        except DatabaseException as e:
            raise e
        except Exception as e:
            raise BaseAppException(f"Failed to update employee deduction: {str(e)}")
