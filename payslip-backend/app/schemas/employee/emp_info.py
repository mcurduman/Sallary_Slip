from pydantic import BaseModel, Field
from typing import Optional

class EmployeeInfo(BaseModel):
    full_name: str = Field(..., alias="fullName")
    email: str = Field(..., alias="email")
    gross_salary: float = Field(..., alias="grossSalary")
    net_salary: float = Field(..., alias="netSalary")
    working_days: int = Field(..., alias="workingDays")
    vacation_days_taken: int = Field(..., alias="vacationDaysTaken")
    bonuses: Optional[float] = Field(0.0, alias="bonuses")

    model_config = {"from_attributes": True, "populate_by_name": True}