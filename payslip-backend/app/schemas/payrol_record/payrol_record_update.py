from app. schemas.monthly_timecard.monthly_timecard_base import MonthlyTimecardBase
import uuid
from pydantic import Field

class PayrolRecordUpdate(MonthlyTimecardBase):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, alias="id")