from app.schemas.payrol_record.payrol_record_base import PayrolRecordBase
from app.schemas.employee.employee_response_manager import EmployeeResponseManager
from pydantic import Field

class PayrolRecordResponse(PayrolRecordBase):
    employee: EmployeeResponseManager = Field(alias="employee")
