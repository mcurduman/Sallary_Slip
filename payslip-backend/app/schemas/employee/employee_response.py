from app.schemas.position.position_response import PositionResponse
from app.schemas.discipline.discipline_response import DisciplineResponse
from pydantic import BaseModel, Field
from typing import Optional

class EmployeeResponse(BaseModel):
    national_id: str = Field(..., alias="nationalId")
    country_of_id: Optional[str] = Field(None, alias="countryOfId")
    position: PositionResponse = Field(..., alias="position")
    discipline: DisciplineResponse = Field(..., alias="discipline")
    first_name: str = Field(..., alias="firstName")
    middle_name: Optional[str] = Field(None, alias="middleName")
    last_name: str = Field(..., alias="lastName")
    email: str = Field(..., alias="email")

    model_config = {"from_attributes": True, "populate_by_name": True}