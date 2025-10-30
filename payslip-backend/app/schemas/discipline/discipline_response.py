from app.schemas.discipline.disciplin_base import DisciplineBase
import uuid
from pydantic import Field

class DisciplineResponse(DisciplineBase):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)