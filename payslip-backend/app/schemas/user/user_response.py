from app.schemas.user.user_base import UserBase
from pydantic import Field
import uuid
class UserResponse(UserBase):
    id: uuid.UUID = Field(..., alias="id")