from app.schemas.emp_deduction.emp_deduction_base import EmployeeDeductionBase
import uuid
from pydantic import Field

class EmployeeDeductionResponse(EmployeeDeductionBase):
    id: uuid.UUID = Field(..., alias="id")
