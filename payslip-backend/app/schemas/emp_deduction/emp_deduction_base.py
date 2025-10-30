from pydantic import BaseModel, Field, field_validator, model_validator
import uuid
from typing import Optional
from datetime import date
from app.utils.enums.calculation_method_enum import CalculationMethod
from app.utils.enums.periodicity_enum import Periodicity
from app.utils.enums.deduction_type_enum import DeductionType
from app.utils.validators.percentage_validator import validate_percentage


class EmployeeDeductionBase(BaseModel):
    employee_id: uuid.UUID = Field(default_factory=uuid.uuid4, alias="employeeId")
    type: DeductionType = Field(..., alias="type")
    amount: Optional[float] = Field(None, alias="amount")
    percentage: Optional[float] = Field(None, alias="percentage")
    calculation_method: CalculationMethod = Field(
        CalculationMethod.fixed,
        alias="calculationMethod"
    )
    taxable: bool = Field(True, alias="taxable")
    periodicity: Periodicity = Field(
        Periodicity.monthly,
        alias="periodicity"
    )
    effective_start_date: Optional[date] = Field(None, alias="effectiveStartDate")
    effective_end_date: Optional[date] = Field(None, alias="effectiveEndDate")
    
    model_config = { "from_attributes": True,
                     "populate_by_name": True }
    
    @field_validator("percentage")
    @classmethod
    def validate_percentage(cls, v):
        if not validate_percentage(v):
            raise ValueError("Percentage must be between 0 and 100")
        return v
    
    @model_validator(mode="after")
    def validate_calculation_method(self):
        if self.calculation_method == CalculationMethod.percentage and self.percentage is None:
            raise ValueError("Percentage must be provided when calculation method is 'percentage'")
        if self.calculation_method == CalculationMethod.fixed and self.amount is None:
            raise ValueError("Amount must be provided when calculation method is 'fixed'")
        return self
    
    @model_validator(mode="after")
    def check_date_range(self):
        if self.effective_start_date and self.effective_end_date:
            if self.effective_end_date <= self.effective_start_date:
                raise ValueError("effective_end_date must be after effective_start_date")
        return self