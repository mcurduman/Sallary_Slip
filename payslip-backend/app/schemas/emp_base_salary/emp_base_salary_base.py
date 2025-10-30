from pydantic import BaseModel, Field, model_validator
import uuid
from typing import Optional
from app.utils.validators.percentage_validator import validate_percentage
from app.utils.validators.date_validator import validate_date_range
from pydantic import field_validator
from datetime import date


class EmployeeBaseSalaryBase(BaseModel):
    employee_id: uuid.UUID = Field(default_factory=uuid.uuid4, alias="employeeId")
    base_salary: float = Field(..., alias="baseSalary")
    tax_percentage: Optional[float] = Field(None, alias="taxPercentage")
    effective_start_date: Optional[date] = Field(None, alias="effectiveStartDate")
    effective_end_date: Optional[date] = Field(None, alias="effectiveEndDate")

    model_config = { "from_attributes": True,
                     "populate_by_name": True }
    
    @field_validator("tax_percentage")
    @classmethod
    def validate_tax_percentage(cls, v):
        if not validate_percentage(v):
            raise ValueError("Tax percentage must be between 0 and 100")
        return v
    
    @model_validator(mode="after")
    def check_date_range(self):
        if not validate_date_range(self.effective_start_date, self.effective_end_date):
            raise ValueError("effective_end_date must be after effective_start_date")
        return self
        