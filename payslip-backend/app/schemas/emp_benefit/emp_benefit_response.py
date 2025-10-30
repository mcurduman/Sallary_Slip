from app.schemas.emp_benefit import EmployeeBenefitBase
from pydantic import Field
import uuid

class EmployeeBenefitResponse(EmployeeBenefitBase):
    id: uuid.UUID = Field(..., alias="id")