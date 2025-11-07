from app.schemas.user.user_base import UserBase
from pydantic import Field
class UserUpdate(UserBase):
    password: str | None = Field(None, alias="password")
    model_config = { "from_attributes": True,"populate_by_name": True }