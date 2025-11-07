from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class EmployeeDetails(BaseModel):
    email: EmailStr = Field(..., alias="email")
    full_name: str = Field(..., alias="fullName")
    discipline: Optional[str] = Field(None, alias="discipline")
    position: Optional[str] = Field(None, alias="position")

    model_config = { "from_attributes": True,
                     "populate_by_name": True }