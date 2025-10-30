from app.schemas.position.position_base import PositionBase
import uuid
from pydantic import Field

class PositionUpdate(PositionBase):
    id: uuid.UUID = Field(..., alias="id")
