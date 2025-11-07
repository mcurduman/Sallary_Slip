from app.schemas.payroll_record.payroll_record_base import PayrollRecordBase
import uuid
from pydantic import Field

class PayrollRecordUpdate(PayrollRecordBase):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, alias="id")
