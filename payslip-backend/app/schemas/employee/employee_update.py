from pydantic import BaseModel, Field, method_validator
from app.utils.enums.employment_status_enum import EmploymentStatus
from typing import Optional
from datetime import date
import uuid

class EmployeeUpdate(BaseModel):
    termination_date: Optional[date] = Field(None, alias="terminationDate")

    @method_validator(mode="after")
    def validate_termination_fields(self):
        if self.employment_status == EmploymentStatus.terminated and self.termination_date is None:
            raise ValueError("Termination date must be provided when employment status is 'terminated'")
        elif self.employment_status != EmploymentStatus.terminated and self.termination_date is not None:
            raise ValueError("Termination date must be null when employment status is not 'terminated'")
        return self
    last_name: str = Field(..., alias="lastName")
    first_name: str = Field(..., alias="firstName")
    middle_name: Optional[str] = Field(None, alias="middleName")
    discipline_id: str = Field(..., alias="disciplineId")
    manager_id: Optional[uuid.UUID] = Field(None, alias="managerId")
    employment_status: Optional[EmploymentStatus] = Field(None, alias="employmentStatus")
    position_id: str = Field(..., alias="positionId")


