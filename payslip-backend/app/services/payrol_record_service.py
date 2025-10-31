from app.db.models.payroll_record import PayrollRecord
from app.repositories.payroll_record_repository import PayrollRecordRepository
from typing import Optional, Iterable
import uuid
from app.utils.errors import ResourceNotFoundException, DatabaseException, BaseAppException

class PayrolRecordService:
    def __init__(self, payroll_record_repository: PayrollRecordRepository):
        self.payroll_record_repository = payroll_record_repository

    async def create_payroll_record(self, payroll_record: PayrollRecord) -> PayrollRecord:
        try:
            return await self.payroll_record_repository.create(payroll_record)
        except DatabaseException as e:
            raise e
        except Exception as e:
            raise BaseAppException(f"Failed to create payroll record: {str(e)}")
        
    async def get_payroll_record_by_id(self, payroll_record_id: uuid.UUID
        ) -> Optional[PayrollRecord]:
        try:
            return await self.payroll_record_repository.get(payroll_record_id)
        except ResourceNotFoundException as e:
            raise e
        except DatabaseException as e:
            raise e
        except Exception as e:
            raise BaseAppException(f"Failed to retrieve payroll record: {str(e)}")
        
    async def get_all_payroll_records(self) -> Iterable[PayrollRecord]:
        try:
            return await self.payroll_record_repository.get_all()
        except DatabaseException as e:
            raise e
        except Exception as e:
            raise BaseAppException(f"Failed to retrieve payroll records: {str(e)}")
        
    async def delete_payroll_record(self, payroll_record_id: uuid.UUID) -> None:
        try:
            await self.payroll_record_repository.delete(payroll_record_id)
        except ResourceNotFoundException as e:
            raise e
        except DatabaseException as e:
            raise e
        except Exception as e:
            raise BaseAppException(f"Failed to delete payroll record: {str(e)}")
        
    async def update_payroll_record(self, payroll_record: PayrollRecord
        ) -> PayrollRecord:
        try:
            return await self.payroll_record_repository.update(payroll_record)
        except ResourceNotFoundException as e:
            raise e
        except DatabaseException as e:
            raise e
        except Exception as e:
            raise BaseAppException(f"Failed to update payroll record: {str(e)}")