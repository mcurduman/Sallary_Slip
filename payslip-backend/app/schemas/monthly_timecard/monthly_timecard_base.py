from pydantic import BaseModel, field_validator, Field, method_validator
from typing import Optional
import uuid
from datetime import date
from app.utils.enums import TimecardStatus

class MonthlyTimecardBase(BaseModel):
    employee_id: uuid.UUID = Field(default_factory=uuid.uuid4, alias="employeeId")
    year: int = Field(..., alias="year")
    month: int = Field(..., alias="month")
    approved_by: Optional[uuid.UUID] = Field(None, alias="approvedBy")
    worked_days: Optional[int] = Field(None, alias="workedDays")
    paid_leave_days: Optional[int] = Field(None, alias="paidLeaveDays")
    unpaid_leave_days: Optional[int] = Field(None, alias="unpaidLeaveDays")
    worked_hours: Optional[int] = Field(None, alias="workedHours")
    overtime_hours: Optional[int] = Field(None, alias="overtimeHours")
    status: Optional[TimecardStatus] = Field(TimecardStatus.DRAFT, alias="status")

    model_config = {"from_attributes": True, "populate_by_name": True}
    
    @field_validator("month")
    @classmethod
    def validate_month(cls, v):
        if v < 1 or v > 12:
            raise ValueError("Month must be between 1 and 12")
        return v
    
    @field_validator("year")
    @classmethod
    def validate_year(cls, v):
        current_year = date.today().year
        if v < 1900 or v > current_year:
            raise ValueError(f"Year must be between 1900 and {current_year}")
        return v
    
    @method_validator(mode="after")
    def validate_status_and_approver(self):
        if self.status == TimecardStatus.APPROVED and self.approved_by is None:
            raise ValueError("approved_by must be set when status is APPROVED")
        elif self.status != TimecardStatus.APPROVED and self.approved_by is not None:
            raise ValueError("approved_by must be None unless status is APPROVED")
        return self


