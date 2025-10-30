from app.schemas.discipline.disciplin_base import DisciplineBase
from pydantic import Field
import uuid
class DisciplineUpdate(DisciplineBase):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, alias="id")