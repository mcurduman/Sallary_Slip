from app.db.models.emp_benefit import EmployeeBenefit
from app.repositories.emp_benefit_repository import EmployeeBenefitRepository
from typing import Optional, Iterable
import uuid
from app.utils.errors import ResourceNotFoundException, DatabaseException, BaseAppException

class EmpBenefitService:
    def __init__(self, emp_benefit_repository: EmployeeBenefitRepository):
        self.emp_benefit_repository = emp_benefit_repository

    async def create_emp_benefit(self, emp_benefit: EmployeeBenefit) -> EmployeeBenefit:
        try:
            return await self.emp_benefit_repository.create(emp_benefit)
        except DatabaseException as e:
            raise e
        except Exception as e:
            raise BaseAppException(f"Failed to create employee benefit: {str(e)}")
        
    async def get_emp_benefit_by_id(self, emp_benefit_id: uuid.UUID
        ) -> Optional[EmployeeBenefit]:
        try:
            return await self.emp_benefit_repository.get(emp_benefit_id)
        except ResourceNotFoundException as e:
            raise e
        except DatabaseException as e:
            raise e
        except Exception as e:
            raise BaseAppException(f"Failed to retrieve employee benefit: {str(e)}")
        
    async def get_all_emp_benefits(self) -> Iterable[EmployeeBenefit]:
        try:
            return await self.emp_benefit_repository.get_all()
        except DatabaseException as e:
            raise e
        except Exception as e:
            raise BaseAppException(f"Failed to retrieve employee benefits: {str(e)}")
        
    async def delete_emp_benefit(self, emp_benefit_id: uuid.UUID) -> None:
        try:
            await self.emp_benefit_repository.delete(emp_benefit_id)
        except ResourceNotFoundException as e:
            raise e
        except DatabaseException as e:
            raise e
        except Exception as e:
            raise BaseAppException(f"Failed to delete employee benefit: {str(e)}")
        
    async def update_emp_benefit(self, emp_benefit: EmployeeBenefit
        ) -> EmployeeBenefit:
        try:
            return await self.emp_benefit_repository.update(emp_benefit)
        except ResourceNotFoundException as e:
            raise e
        except DatabaseException as e:
            raise e
        except Exception as e:
            raise BaseAppException(f"Failed to update employee benefit: {str(e)}")
