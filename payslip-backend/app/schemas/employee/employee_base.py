from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from app.utils.validators.date_validator import validate_date_range
from pydantic import model_validator
from datetime import date
from app.utils.enums.employment_status_enum import EmploymentStatus

class EmployeeBase(BaseModel):
	national_id: str = Field(..., alias="nationalId")
	country_of_id: Optional[str] = Field(None, alias="countryOfId")
	first_name: str = Field(..., alias="firstName")
	middle_name: Optional[str] = Field(None, alias="middleName")
	last_name: str = Field(..., alias="lastName")
	email: EmailStr = Field(..., alias="email")
	position_id: str = Field(..., alias="positionId")
	manager_id: Optional[str] = Field(None, alias="managerId")
	discipline_id: Optional[str] = Field(None, alias="disciplineId")
	employment_status: Optional[str] = Field("active", alias="employmentStatus")
	hire_date: Optional[date] = Field(None, alias="hireDate")
	termination_date: Optional[date] = Field(None, alias="terminationDate")


	model_config = {"from_attributes": True, "populate_by_name": True}

	@model_validator(mode="after")
	def check_date_range(self):
		if not validate_date_range(self.hire_date, self.termination_date):
			raise ValueError("Termination date must be null or after hire_date")
		return self

	@model_validator(mode="after")
	def validate_employment_status_termination_date(self):
		if self.employment_status == EmploymentStatus.terminated and self.termination_date is None:
			raise ValueError("Termination date must be provided when employment status is 'terminated'")
		elif self.employment_status != EmploymentStatus.terminated and self.termination_date is not None:
			raise ValueError("Termination date must be null when employment status is not 'terminated'")    
		return self