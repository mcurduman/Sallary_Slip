from pydantic import BaseModel, Field, EmailStr
from app.utils.enums.user_role_enum import UserRole
from typing import List

class UserBase(BaseModel):
    email: EmailStr = Field(..., alias="email")
    username: str = Field(..., alias="username")
    roles: List[UserRole] = Field([UserRole.EMPLOYEE], alias="roles")

    model_config = { "from_attributes": True,
                     "populate_by_name": True }
    
