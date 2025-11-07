from typing import Optional, Iterable, List
from app.repositories.base_repository import BaseRepository
from app.db.models.payroll_record import PayrollRecord
import uuid
from app.utils.errors.DatabaseException import DatabaseException
from app.utils.errors.ResourceNotFoundException import ResourceNotFoundException
from app.core.logging import get_logger
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

class PayrollRecordRepository(BaseRepository[PayrollRecord, uuid.UUID]):

    def __init__(self, session: AsyncSession):

        assert isinstance(session, AsyncSession), f"Session is not AsyncSession, got {type(session)}"
        get_logger().info(f"Session type: {type(session)}")
        self._session = session

    async def get_by_id(self, id: uuid.UUID) -> Optional[PayrollRecord]:
        try:
            payroll_record = await self._session.execute(select(PayrollRecord).where(PayrollRecord.id == id))
            if not payroll_record:
                raise ResourceNotFoundException("Payroll record not found")
            return payroll_record.first()
        except Exception as e:
            raise DatabaseException(f"Failed to retrieve payroll record: {str(e)}")

    async def get_payroll_data(self, employee_id: uuid.UUID, month: int, year: int) -> Iterable[PayrollRecord]:
        try:
            get_logger().info(f"Retrieving payroll data for employee {employee_id}, month {month}, year {year}")
            result = await self._session.execute(select(PayrollRecord).where(
                PayrollRecord.employee_id == employee_id,
                PayrollRecord.payroll_month == month,
                PayrollRecord.payroll_year == year
            ))
            records = result.scalars().first()
            get_logger().info(f"Retrieved payroll records: {records}")
            return records
        except Exception as e:
            raise DatabaseException(f"Failed to retrieve payroll record: {str(e)}")

    async def _check_exists(self, employee_id: uuid.UUID, month: int, year: int) -> bool:
        try:
            get_logger().info(f"Checking existence of payroll record for employee {employee_id}, month {month}, year {year}")
            result = await self._session.execute(select(PayrollRecord).where(
                PayrollRecord.employee_id == employee_id,
                PayrollRecord.payroll_month == month,
                PayrollRecord.payroll_year == year
            ))
            record = result.scalars().first()
            get_logger().info(f"Payroll record existence check complete: {record is not None}")
            return record is not None
        except Exception as e:
            raise DatabaseException(f"Failed to check payroll record existence: {str(e)}")

    async def create(self, entity: PayrollRecord) -> PayrollRecord:
        try:
            get_logger().info("Creating payroll record in repository")
            if await self._check_exists(entity.employee_id, entity.payroll_month, entity.payroll_year):
                raise DatabaseException("Payroll record for this employee and period already exists")
            self._session.add(entity)
            get_logger().info(f"Payroll record created successfully: {entity}")
            return entity
        except Exception as e:
            raise DatabaseException(f"Failed to create payroll record: {str(e)}")
         
    async def get_all(self) -> Iterable[PayrollRecord]:
        try:
            get_logger().info("Retrieving all payroll records from repository")
            result = await self._session.execute(select(PayrollRecord))
            records = result.scalars().all()
            return records
        except Exception as e:
            raise DatabaseException(f"Failed to retrieve payroll records: {str(e)}")

    async def get_all_by_ids(self, ids_list: List[uuid.UUID], month: int, year: int) -> Iterable[PayrollRecord]:
        try:
            result = await self._session.execute(
                select(PayrollRecord).where(
                    PayrollRecord.employee_id.in_(ids_list),
                    PayrollRecord.payroll_month == month,
                    PayrollRecord.payroll_year == year
                )
            )
            records = result.scalars().all()
            return records
        except Exception as e:
            raise DatabaseException(f"Failed to retrieve payroll records for manager: {str(e)}")
        
    async def get_by_employee_email(self, employee_email: str) -> Iterable[PayrollRecord]:
        try:
            get_logger().info(f"Retrieving payroll records for employee email: {employee_email}")
            
            result = await self._session.execute(
                select(PayrollRecord).options(joinedload(PayrollRecord.employee)).where(
                    PayrollRecord.employee.has(email=employee_email)
                )
            )
            records = result.scalars().all()
            get_logger().info(f"Retrieved payroll records: {records}")
            return records
        except Exception as e:
            raise DatabaseException(f"Failed to retrieve payroll records for employee: {str(e)}")
