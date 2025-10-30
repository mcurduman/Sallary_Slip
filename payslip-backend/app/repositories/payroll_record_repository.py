from typing import Optional, Iterable
from app.repositories.base_repository import BaseRepository
import app.utils.errors as errors
from app.db.models.payroll_record import PayrollRecord
import uuid

class PayrollRecordRepository(BaseRepository[PayrollRecord, uuid.UUID]):
    def get_by_id(self, id: uuid.UUID) -> Optional[PayrollRecord]:
        try:
            record = self._db.query(PayrollRecord).filter(PayrollRecord.id == id).first()
            if not record:
                raise errors.ResourceNotFoundException("Payroll record not found")
            return record
        except Exception as e:
            raise errors.DatabaseException(f"Failed to retrieve payroll record: {str(e)}")

    def create(self, entity: PayrollRecord) -> PayrollRecord:
        try:
            self._db.add(entity)
            self._db.commit()
            self._db.refresh(entity)
            return entity
        except Exception as e:
            self._db.rollback()
            raise errors.DatabaseException(f"Failed to create payroll record: {str(e)}")

    def get_all(self) -> Iterable[PayrollRecord]:
        try:
            records = self._db.query(PayrollRecord).all()
            return records
        except Exception as e:
            raise errors.DatabaseException(f"Failed to retrieve payroll records: {str(e)}")
        
    def delete(self, id: uuid.UUID) -> None:
        try:
            record = self.get_by_id(id)
            if not record:
                raise errors.ResourceNotFoundException("Payroll record not found")
            self._db.delete(record)
            self._db.commit()
        except Exception as e:
            self._db.rollback()
            raise errors.DatabaseException(f"Failed to delete payroll record: {str(e)}")
        
    def update(self, entity: PayrollRecord) -> PayrollRecord:
        try:
            self._db.merge(entity)
            self._db.commit()
            self._db.refresh(entity)
            return entity
        except Exception as e:
            self._db.rollback()
            raise errors.DatabaseException(f"Failed to update payroll record: {str(e)}")