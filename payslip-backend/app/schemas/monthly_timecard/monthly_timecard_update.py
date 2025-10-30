from app.schemas.monthly_timecard.monthly_timecard_base import MonthlyTimecardBase
from pydantic import Field
import uuid

class MonthlyTimecardUpdate(MonthlyTimecardBase):
    id : uuid.UUID = Field(..., alias="id")