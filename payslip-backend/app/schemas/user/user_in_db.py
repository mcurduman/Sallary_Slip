from app.schemas.user.user_base import UserBase
from pydantic import Field

class UserInDB(UserBase):
    hashed_password: str = Field(..., alias="hashedPassword")

    model_config = { "from_attributes": True,
                     "populate_by_name": True }