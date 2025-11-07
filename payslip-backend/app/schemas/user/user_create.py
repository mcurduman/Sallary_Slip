from app.schemas.user.user_base import UserBase
from pydantic import Field
class UserCreate(UserBase):
    password: str = Field(..., alias="password")

    model_config = { "from_attributes": True,"populate_by_name": True }