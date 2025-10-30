from pydantic import BaseModel, Field, EmailStr
from app.utils.enums.user_role_enum import UserRole

class UserBase(BaseModel):
    email: EmailStr = Field(..., alias="email")
    username: str = Field(..., alias="username")
    role: UserRole = Field(UserRole.employee, alias="role")
    hashed_password: str = Field(..., alias="hashedPassword")

    model_config = { "from_attributes": True,
                     "populate_by_name": True }
    
