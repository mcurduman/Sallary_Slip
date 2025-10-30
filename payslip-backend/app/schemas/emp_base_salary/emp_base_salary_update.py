from app.schemas.emp_base_salary.emp_base_salary_base import EmpBaseSalaryBase
from pydantic import Field
import uuid

class EmpBaseSalaryUpdate(EmpBaseSalaryBase):
    id: uuid.UUID = Field(..., alias="id")