from pydantic import BaseModel, Field, method_validator
import uuid
from datetime import date
from typing import Optional

class PayrolRecordBase(BaseModel):
    employee_id: uuid.UUID = Field(default_factory=uuid.uuid4, alias="employeeId")
    year: int = Field(..., alias="year")
    month: int = Field(..., alias="month")
    gross_pay: float = Field(..., alias="grossPay")
    net_pay: float = Field(..., alias="netPay")
    total_deductions: float = Field(..., alias="totalDeductions")
    run_date: Optional[date] = Field(None, alias="runDate")
    
    model_config = {"from_attributes": True, "populate_by_name": True}

    @method_validator(mode="after")
    def validate_dates(self):
        if self.run_date and (self.run_date.year != self.year or self.run_date.month != self.month):
            raise ValueError("run_date must correspond to the specified year and month")
        return self 