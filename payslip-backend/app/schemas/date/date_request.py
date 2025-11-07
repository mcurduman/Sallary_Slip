from pydantic import BaseModel, Field, field_validator
from datetime import date

class DateRequest(BaseModel):
    year: int = Field(..., alias="year")
    month: int = Field(..., alias="month")

    model_config = {"populate_by_name": True}

    @field_validator("month")
    @classmethod
    def validate_month(cls, v):
        if v < 1 or v > 12:
            raise ValueError("month must be between 1 and 12")
        return v
    
    @field_validator("year")
    @classmethod
    def validate_year(cls, v):
        current_year = date.today().year
        if v < 1900 or v > current_year:
            raise ValueError(f"year must be between 1900 and {current_year}")
        return v